from pylatex import  Document,Package,NoEscape,Command
from pylatex.base_classes import Arguments
from .utils import latexShortLine
from .param import *
import re
from pylatex.utils import dumps_list


class NoTokenDocument(Document):
    def dumps(self):
        head = self.documentclass.dumps() + '\n'
        head += self.dumps_packages() + '\n'
        head += dumps_list(self.variables,token='\n') + '\n'
        head += dumps_list(self.preamble,token='\n') + '\n'

        return head + '\n' + self.content_dumps()

    def dumps_content(self, **kwargs):
        return dumps_list(self, escape=self.escape,
                          token="\n", **kwargs)

    def content_dumps(self):
        """Represent the environment as a string in LaTeX syntax.

        Returns
        -------
        str
            A LaTeX string representing the environment.
        """

        content = self.dumps_content()
        if not content.strip() and self.omit_if_empty:
            return ''

        string = ''

        # Something other than None needs to be used as extra arguments, that
        # way the options end up behind the latex_name argument.
        if self.arguments is None:
            extra_arguments = Arguments()
        else:
            extra_arguments = self.arguments

        begin = Command('begin', self.start_arguments, self.options,
                        extra_arguments=extra_arguments)
        begin.arguments._positional_args.insert(0, self.latex_name)
        string += begin.dumps() + self.content_separator

        string += content + self.content_separator

        string += Command('end', self.latex_name).dumps()

        return string

class MarkDocument:
    doc = NoTokenDocument(documentclass="ctexart",document_options="UTF8",inputenc=None,fontenc=None,lmodern=False,textcomp=False)
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