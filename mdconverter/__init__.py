from .documents import MarkDocument
# from containers import *
from .containers import parseforeach

def excu(text):
    # text = excuInlineText(text)

    lines = text.split("\n")

    mdoc = MarkDocument()

    mdoc.content += parseforeach(lines)
    # lines = _sub_Bold_Itali(lines)
    print(mdoc.toLabex())
