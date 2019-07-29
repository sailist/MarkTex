from marktex.markast.parser import Scanner
from marktex.texrender.toTex import MarkTex
from pylatex import Command,NoEscape


# st = '''
# $$F(X_i)=K+\\frac{a}{b}$$
#
# '''.split("\n")
#
# doc = Scanner().analyse(st)
# print(doc)
# mark = MarkTex(doc)
# mark.convert()
#
# strings = mark.dumps()
#
# with open("t.tex","w",encoding="utf-8") as w:
#     w.write(strings)
#
#

print(Command("item",options=NoEscape("$\squeare$")).dumps())