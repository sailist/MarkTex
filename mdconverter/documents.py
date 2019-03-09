from pylatex import  Document,Package,NoEscape
from .utils import latexShortLine
from .param import *
import re




class MarkDocument:
    doc = Document(documentclass="ctexart",document_options="UTF8",inputenc=None,fontenc=None,lmodern=False,textcomp=False)
    content = []
    def __init__(self):
        for p in packages:
            self.doc.packages.append(p)

        for p in preambles:
            self.doc.preamble.append(p)
        self.doc.preamble.append(title)

    def toLabex(self):
        for i in self.content:
            self.doc.append(i.toLatex())
        result = self.doc.dumps()
        result = re.sub(latexShortLine,"-",result)
        return result


# def __init__(self, default_filepath='default_filepath', *,
#                  documentclass='article', document_options=None, fontenc='T1',
#                  inputenc='utf8', font_size="normalsize", lmodern=True,
#                  textcomp=True, microtype=None, page_numbers=True, indent=None,
#                  geometry_options=None, data=None):

class BaseDocument(Document):
    def __init__(self):
        # self.preamble.
        pass