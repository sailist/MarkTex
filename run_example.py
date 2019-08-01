from marktex.example import run_example

# run_example("./output/")


from marktex.texrender.toTex import MarkTex

from marktex.markast.parser import Scanner

doc = MarkTex.convert_file("./marktex/example/example.md")
# doc.generate_tex("test")


# doc = Scanner.analyse_file("./marktex/example/example.md")
# print(doc)