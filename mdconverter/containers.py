from pylatex import Figure, Section,Subsection, Itemize,Enumerate, Tabular,Subsubsection,Document
from img_tools import transimg, image_downloader
from PIL import Image
from pylatex.utils import bold,italic
from .environments import CodeEnvironment,QuoteEnvironment,Center,Text
from .utils import *
from .parser import *
# line = re.sub(markBold,texbold,line)
# line = re.sub




class MarkContainer():
    content = ""
    def __init__(self):
        print(self.__repr__())
    def __repr__(self):
        return "{} {}".format(self.__class__.__name__,str(self.content))

    def toLatex(self):
        return "% not impl"

class MarkHLine(MarkContainer):
    def __init__(self,line = None):
        pass
    def toLatex(self):
        return NoEscape(r"{\vspace{\baselineskip}\color{gainsboro}\hrule\vspace{\baselineskip}}")

class MarkSection(MarkContainer):
    def __init__(self,s):
        result = re.search(markSection,s)
        self.content = result.group(2)
        self.level = len(result.group(1))

    def toLatex(self):
        if self.level == 1:
            return Section(self.content,label=False)
        elif self.level == 2:
            return Subsection(self.content,label=False)
        elif self.level == 3:
            return Subsubsection(self.content,label=False)
        elif self.level == 4:
            return NoEscape(r"\noindent{{\large\textbf{{{}}}}}".format(self.content))
        elif self.level == 5:
            return NoEscape(r"\noindent{{\textbf{{{}}}}}".format(self.content))


class MarkNewLine(MarkContainer):
    def __init__(self):
        pass
    def toLatex(self):
        return NoEscape("\n")
class MarkToc(MarkContainer):
    def __init__(self,line = None):
        pass

    def toLatex(self):
        return NoEscape(r"\maketitle")

class DumpsObject:
    def __init__(self,content):
        self.content = content
    def dumps(self):
        return self.content

class MarkImg(MarkContainer):

    def __init__(self,s):
        result = re.search(markImg,s)
        self.caption = result.group(1)
        self.content = result.group(2)


    def toLatex(self):
        f = Figure(position='h!')
        # f.add_caption(self.caption)
        self.content = image_downloader(self.content)
        self.content = transimg(self.content)
        try:
            Image.open(self.content).verify()
            t = Text()
            t.append(NoEscape(r"\vspace{{\baselineskip}}\includegraphics[width=0.8\textwidth]{{{}}}\vspace{{\baselineskip}}".format(self.content)))
            return t
        except:
            return NoEscape("% 图片损坏或者未下载")



markTableSplit = re.compile(r"^-+$")

class MarkTable(MarkContainer):

    def __init__(self,markRows):
        self.content = []
        self.max_col = 0
        for row in markRows:
            row_items = []


            matchiter = re.finditer(markTableContent, row)
            for i in matchiter:
                if re.search(markTableSplit,i.group(1)):
                    break

                row_items.append(i.group(1))
            # print(row_items)
            if len(row_items) != 0:
                self.content.append(row_items)
                self.max_col = max(self.max_col,len(row_items))


    def toLatex(self):
        self.max_col-=1

        option = "|"+r"p{{{:.1f}\textwidth}}<{{\centering}}|".format(1.0/self.max_col)*self.max_col
        t = Tabular(option)
        t.add_hline()
        for ii in self.content:
            for i in range(len(ii)):
                if re.search(mark2newline,ii[i]):
                    rows = excuInlineText(ii[i])
                    rows = [MarkNormal(r).toLatex().__str__() for r in rows]
                    ii[i] = NoEscape("".join(rows))
            ii = ii[:-1]
            t.add_row(ii)
            t.add_hline()
        c = Center()
        c.append(t)
        return c


class MarkQuote(MarkContainer):
    def __init__(self,quotes):
        quote = []
        for row in quotes:
            if re.search(markQuote, row):
                quote.append(re.search(markQuote,row).group(1))
            else:
                quote.append(row)

        self.content = quote
        # result = re.search(markQuote,quote)
        # if result:
        #     self.content = result.group(1)
        # else:
        #     self.content = quote

    def toLatex(self):
        q = QuoteEnvironment()
        items = parseforeach(self.content,True)

        for i in items:
            q.append(i.toLatex())
        return q

class MarkItem(MarkContainer):
    def __init__(self,rows):
        rows = [re.search(markItem,row).group(1) for row in rows]
        self.content = rows
        # print(rows)
    def toLatex(self):
        e = Itemize()

        items = parseforeach(self.content,False)
        for i in items:
            e.add_item(i.toLatex())
        return e

class MarkEnum(MarkContainer):
    def __init__(self,rows):
        rows = [re.search(markEnum,row).group(1) for row in rows]
        self.content = rows;

    def toLatex(self):
        e = Enumerate()

        items = parseforeach(self.content, False)
        for i in items:
            e.add_item(i.toLatex())

        return e

class MarkFomula(MarkContainer):
    def __init__(self,fomula):
        self.content = fomula
    def toLatex(self):
        return NoEscape("%%not impl:{}".format(self.content))

class MarkCode(MarkContainer):
    def __init__(self,ctype,code):
        self.code_type = ctype
        self.content = code
    def toLatex(self):
        c = CodeEnvironment(options=[NoEscape("language={[ANSI]C++}"), NoEscape("keywordstyle=\color{blue!70}"), NoEscape("commentstyle=\color{red!50!green!50!blue!50}"), NoEscape("escapeinside=``"), NoEscape(r"basicstyle=\tiny")])

        c.append(NoEscape("\n"+"\n".join(self.content)))
        return c

class MarkNormal(MarkContainer):
    '''
    需要保证每次输入的只能是无inline命令的普通文本
    ** **文本
    * *文本
    ` `文本
    '''
    def __init__(self,row):
        self.content = []
        self.func = []
        # row = dumps_list([row])
        rows = excuInlineText(row)
        for row in rows:
        # print(row)
            if re.search(markBold,row):
                self.content.append(re.search(markBold,row).group(1))
                self.func.append(bold)
            elif re.search(markItali,row):
                self.content.append(re.search(markItali,row).group(1))
                self.func.append(italic)
            elif re.search(markInline,row):
                self.content.append(re.search(markInline,row).group(1))
                self.func.append(hignlight)
            elif re.search(markImg,row):
                self.content.append(row)
                self.func.append(toImg)
            elif re.search(markLink,row):
                thedict = {
                    "url":re.search(markLink,row).group(2),
                    "content":re.search(markLink,row).group(1),
                }
                self.content.append(thedict)
                self.func.append(herf)
            else:
                self.content.append(row)
                self.func.append(NoEscape)

    def toLatex(self):
        result = []
        for w,func in zip(self.content,self.func):
            result.append(func(w))
        return NoEscape("".join(result))


def toImg(row):
    return MarkImg(row).toLatex().dumps()


def parseforeach(lines,add_empty_line = False):
    line_index = 0
    line_len = len(lines)
    markItemlist = []
    while line_index<line_len:
        line = lines[line_index]
        # print(line)
        k = None
        # result = re.search(, line)
        if re.search(markToc,line):
            k = MarkToc(line)
            pass
        elif re.search(markSection,line):
            k = MarkSection(line)
            pass
        elif re.search(markLine,line):
            k = MarkHLine(line)
        elif re.search(markQuote,line):##TODO 对于连续的 >不会有层次
            start,end = findBound(markQuote,lines,line_index)
            k = MarkQuote(lines[start:end+1])
            line_index = end
            pass
        elif re.search(markImg,line):
            k = MarkImg(line)
            pass
        elif re.search(markTable,line):
            start, end = findBound(markTable, lines, line_index)
            k = MarkTable(lines[start:end+1])
            line_index = end
            pass
        elif re.search(markItem,line):
            start, end = findBound(markItem, lines, line_index)
            k = MarkItem(lines[start:end+1])
            line_index = end
            pass
        elif re.search(markEnum,line):
            start, end = findBound(markEnum, lines, line_index)
            k = MarkEnum(lines[start:end+1])
            line_index = end
            pass
        elif re.search(markCode,line):
            codeTemplate,start,end = findCodeBound(lines,line_index)
            # print("\n".join(lines[start+1:end]))
            k = MarkCode(codeTemplate,lines[start+1:end+1])
            line_index = end+1 #因为返回的是```的上一行
        else:
            k = MarkNormal(line)
        # print(k.toLatex())
        if len(line)>0:
            markItemlist.append(k)
            if add_empty_line:
                markItemlist.append(MarkNewLine())

        line_index += 1

    return markItemlist

