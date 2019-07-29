from marktex.markast.utils import ExtractTool

class Token: #可以作为 行内的部分出现

    def __init__(self,s) -> None:
        super().__init__()
        self.string = s
        self.initial(s)

    def initial(self,s):
        pass

    def __str__(self) -> str:
        return self.string.__str__()

    def __len__(self):
        return len(self.string)

class Bold(Token):

    def initial(self, s):
        self.string = ExtractTool.bold(self.string)

    def __len__(self):
        return len(self.string)

    def __str__(self) -> str:
        return f"Bold({self.string})"

class Italic(Token):
    def initial(self, s):
        self.string = ExtractTool.italic(self.string)

    def __len__(self):
        return len(self.string)

    def __str__(self) -> str:
        return f"Italic({self.string})"

class InFormula(Token):
    def initial(self, s):
        self.string = ExtractTool.informula(self.string)

    def __str__(self) -> str:
        return f"InFormula({self.string})"

    def __len__(self):
        return len(self.string)

class InCode(Token):
    def initial(self, s):
        self.string = ExtractTool.incode(self.string)

    def __str__(self) -> str:
        return f"InCode({self.string})"

class Hyperlink(Token):

    def initial(self, s):
        self.desc,self.link = ExtractTool.hyperlink(self.string)

    def __str__(self) -> str:
        return f"Hyperlink({self.desc};{self.link})"

    def __len__(self):
        return len(self.desc)

class Footnote(Token):

    def initial(self, s):
        self.label = ExtractTool.footnote(self.string)

    def __str__(self) -> str:
        return f"Footnote({self.label})"

    def __len__(self):
        return 1

class InImage(Token):
    pass

class UnderLine(Token):
    def initial(self, s):
        self.string = ExtractTool.underline(self.string)

class DeleteLine(Token):
    def initial(self, s):
        self.string = ExtractTool.deleteline(self.string)