from pylatex import NoEscape,Package,Command
from pylatex.base_classes import Environment
from marktex import config
from marktex.texrender import texparam


class Text(Environment):
    _latex_name = "marktext"

    def __init__(self, *, options=None, arguments=None, start_arguments=None, **kwargs):
        super().__init__(options=options, arguments=arguments, start_arguments=start_arguments, **kwargs)
        self.empty = True

    def append(self, item):
        super().append(item)
        if not isinstance(item,str):
            self.empty = False
        else:
            if len(item.strip())>0:
                self.empty = False


class Equation(Environment):
    _latex_name = "equation"

class CodeEnvironment(Environment):
    _latex_name = "lstlisting"
    packages = [Package("listings"),Package("xcolor")]

    cpp = "C++"

    code_style_dict = {
        "cpp": "C++"

    }


    def __init__(self,mode=None,texconfig = None,**kwargs):
        if texconfig is None:
            texconfig = config
        if mode is None or len(mode.strip()) == 0:
            mode = "Tex"

        if mode.lower() in CodeEnvironment.code_style_dict:
            mode = CodeEnvironment.code_style_dict[mode]

        options = [NoEscape(f"language={{{mode.capitalize()}}}"),
                   NoEscape(r"keywordstyle=\color{blue!70}"),
                   NoEscape(r"frame=shadowbox"),
                   NoEscape(r"showstringspaces=false"),
                   NoEscape(r"commentstyle=\color{red!50!green!50!blue!50}"),
                   NoEscape(r"escapeinside=``"),]

        options.extend(texparam.build_code_envi_options(texconfig))
        super().__init__(options=options, arguments=None, start_arguments=None, **kwargs)

class QuoteEnvironment(Environment):
    _latex_name = "shaded"
    packages = [Package("showframe","noframe"),Package("framed")]

class TColorBox(Environment):
    _latex_name = "tcolorbox"

class CheckList(Environment):
    """A base class that represents a list."""

    #: List environments cause compile errors when they do not contain items.
    #: This is why they are omitted fully if they are empty.
    omit_if_empty = True
    _latex_name = "itemize"

    def __init__(self, *, options=None, arguments=None, start_arguments=None, **kwargs):
        super().__init__(options=options, arguments=arguments, start_arguments=start_arguments, **kwargs)
        self.packages.add(Package("pifont"))

    uncheck_item = NoEscape("$\square$")
    check_item = NoEscape(r"\rlap{\raisebox{0.3ex}{\hspace{0.4ex}\tiny \ding{52}}}$\square$")
    nocheck_iteunm = NoEscape(r"\rlap{\raisebox{0.3ex}{\hspace{0.4ex}\scriptsize \ding{56}}}$\square$")

    def add_item(self,ct:int,s):
        """Add an item to the list.

        Args
        ----
        s: str or `~.LatexObject`
            The item itself.
        """
        if ct == 0:
            self.append(Command('item',options=CheckList.uncheck_item))
        elif ct == 1:
            self.append(Command('item',options=CheckList.check_item))
        elif ct == 2:
            self.append(Command('item',options=CheckList.nocheck_iteunm))

        self.append(s)


def tablecontent():
    return NoEscape("\\tableofcontents\n\\newpage")

def foo(s:[str])->list:
    s.append(1)
    return [s]

