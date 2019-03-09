from pylatex import Figure,Document,Section,Subsection,Subsubsection,Package,Itemize,Enumerate,frames,Tabular,NoEscape
from pylatex.utils import bold,italic,dumps_list
from .environments import CodeEnvironment,QuoteEnvironment
from .utils import *


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

class MarkHLine:
    def toLatex(self):
        return NoEscape(r"\hrule\vspace{-0.4pt}").__str__()

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
            return Subsection(self.content,label=False)


class MarkToc(MarkContainer):
    def __init__(self,line = None):
        pass

    def toLatex(self):
        return NoEscape(r"\maketitle")


class MarkImg(MarkContainer):

    def __init__(self,s):
        result = re.search(markImg,s)
        self.caption = result.group(1)
        self.content = result.group(2)

    def toLatex(self):
        f = Figure(position='h!')
        f.add_caption(self.caption)
        f.add_image(self.content)
        return NoEscape("%not impl markImg")#TODO

markTableSplit = re.compile(r"^-+$")

class MarkTable(MarkContainer):

    def __init__(self,markRows):
        self.content = []
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


    def toLatex(self):
        t = Tabular('rc|cl')
        t.add_hline()
        for ii in self.content:
            for i in range(len(ii)):
                if re.search(mark2newline,i):
                    rows = excuInlineText(ii[i])
                    rows = [MarkNormal(r).toLatex().__str__() for r in rows]
                    ii[i] = NoEscape("".join(rows))

            t.add_row(ii)
            t.add_hline()
        return t


class MarkQuote(MarkContainer):
    def __init__(self,quotes):
        quote = [re.search(markQuote,q).group(1) for q in quotes]
        self.content = quote
        # result = re.search(markQuote,quote)
        # if result:
        #     self.content = result.group(1)
        # else:
        #     self.content = quote

    def toLatex(self):
        q = QuoteEnvironment()
        for i in self.content:
            if re.search(mark2newline,i):
                rows = excuInlineText(i)
                for j in rows:
                    q.append(MarkNormal(j).toLatex())
            else:
                q.append(i)
        return q

class MarkItem(MarkContainer):
    def __init__(self,rows):
        rows = [re.search(markItem,row).group(1) for row in rows]
        self.content = rows
        # print(rows)
    def toLatex(self):
        e = Itemize()
        for i in self.content:
            if re.search(mark2newline,i):
                rows = excuInlineText(i)
                rows = "".join([MarkNormal(j).toLatex() for j in rows])
                e.add_item(NoEscape(rows))
            else:
                e.add_item(NoEscape(i))
        return e

class MarkEnum(MarkContainer):
    def __init__(self,rows):
        rows = [re.search(markEnum,row).group(1) for row in rows]
        self.content = rows;

    def toLatex(self):
        e = Enumerate()
        for i in self.content:
            if re.search(mark2newline,i):
                rows = excuInlineText(i)
                for j in rows:
                    e.add_item(MarkNormal(j).toLatex())
            e.add_item(NoEscape(i))
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
        c = CodeEnvironment()
        for i in self.content:
            c.append(i)
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
        row = dumps_list([row])
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
            else:
                self.content.append(row)
                self.func.append(NoEscape)

    def toLatex(self):
        result = []
        for w,func in zip(self.content,self.func):
            result.append(func(w))
        return NoEscape("".join(result))

