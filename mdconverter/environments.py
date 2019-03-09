from pylatex import Package
from pylatex.base_classes import Environment
class QuoteEnvironment(Environment):
    _latex_name = "shaded"
    packages = [Package("showframe","noframe"),Package("framed")]


class CodeEnvironment(Environment):
    _latex_name = "lstlisting"
    packages = [Package("listings"),Package("xcolor")]

class Center(Environment):
    _latex_name = "center"


class Text(Environment):
    _latex_name = "text"