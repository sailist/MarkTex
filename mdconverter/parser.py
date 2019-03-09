import re
from .containers import *
from .documents import MarkDocument
from .utils import excuInlineText


def texSection(match):
    sharpstr = match.group(1)
    if len(sharpstr) == 1:
        return Section(match.group(2), label=False).dumps()
    elif len(sharpstr) == 2:
        return Subsection(match.group(2), label=False).dumps()
    elif len(sharpstr) == 3:
        return Subsubsection(match.group(2), label=False).dumps()



def findBound(pattern, lines, start_index,expand = False):
    end_index = start_index
    max_line = len(lines)
    while True:
        if end_index + 1 == max_line:
            return start_index, end_index
        if (expand and len(lines[end_index+1]) > 0 ) or re.search(pattern, lines[end_index + 1]):
            end_index += 1
        else:
            return start_index, end_index

def findCodeBound(lines,start_index):
    end_index = start_index
    line_num = len(lines)
    codeTemplate = re.search(markCode,lines[start_index]).group(1)
    while end_index+1<line_num:
        # print(lines[end_index+1])
        if re.search(markCode,lines[end_index+1]):
            return codeTemplate,start_index,end_index
        else:
            pass
            # print(lines[end_index+1])
        end_index+=1

    # return codeTemplate,start_index,end_index
    assert end_index+1 < line_num



def excu(text):
    # text = excuInlineText(text)
    lines = text.split("\n")
    line_index = 0
    line_len = len(lines)
    mdoc = MarkDocument()
    # lines = _sub_Bold_Itali(lines)
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
        elif re.search(markLine,line):
            k = MarkHLine(line)
        else:
            k = MarkNormal(line)
        # print(k.toLatex())
        if len(line)>0:
            mdoc.content.append(k)
            mdoc.content.append(MarkNewLine())

        line_index += 1
    print(mdoc.toLabex())
