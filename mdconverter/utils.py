import re
from pylatex.utils import NoEscape,escape_latex

markToc = re.compile(r"(@\[[Tt][Oo][Cc]\])")
markSection = re.compile(r"^(#+) (.*)")

mark2newline = re.compile(r"(\*{2}.*?\*{2})|(\*{1}.*?\*{1})|(`.*?`)|(\!\[.*\]\(.*\))|(\[.*\]\(.*\))")

latexShortLine = re.compile(r"{-}+")


markBold = re.compile(r"\*{2}(.*?)\*{2}")
markItali = re.compile(r"\*{1}(.*)\*{1}")
markItem = re.compile(r"^[ ]*-[ ]*(.*)")
markEnum = re.compile(r"^[ ]*[1-9]+\.[ ]*(.*)")
markQuote = re.compile(r"^>[ ]*(.*)")

markTable = re.compile(r"^(\|.*\|+)")
markTableContent = re.compile(r"\|([^\|]*)")
markImg = re.compile(r"\!\[(.*)\]\((.*)\)")

markLine = re.compile("^-{2,}")

markInline = re.compile(r"`(.*)`")
markCode = re.compile(r"^```(.*)")

markLink = re.compile(r"\[(.*)\]\((.*)\)")


def newLine(match):
    '''
    把匹配到的东西前后加入换行符，用于对inline文本进行处理
    :param match:
    :return:
    '''
    return "\n{}\n".format(match.group())

def excuInlineText(text):# 这里不确定是否会有切割到图片的情况 TODO
    return re.sub(mark2newline, newLine, text).split("\n")

#\usepackage{xcolor}
def hignlight(s, *, escape=True):
    if escape:
        s = escape_latex(s)
    return NoEscape(r"\colorbox{aliceblue}{"+s+"}")

def herf(adict,*,escape = True):

    if escape:
        content = escape_latex(adict["content"])
    return NoEscape(r"\href{{{}}}{{{}}}".format(adict["url"],content))

