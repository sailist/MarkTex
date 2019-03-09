from pylatex import  Document,Package,NoEscape
from .param import *
class MarkDocument:
    doc = Document(documentclass="ctexart",document_options="UTF8",inputenc=None,fontenc=None,lmodern=False,textcomp=False)
    content = []
    def __init__(self):
        for p in packages:
            self.doc.packages.append(p)

        for p in preambles:
            self.doc.preamble.append(p)
       
    def toLabex(self):
        for i in self.content:
            self.doc.append(i.toLatex())
        result = self.doc.dumps()
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