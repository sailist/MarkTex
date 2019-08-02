from marktex.example import run_example

# run_example("./output/")


from marktex.texrender.toTex import MarkTex

from marktex.markast.parser import Scanner

doc = MarkTex.convert_file("./marktex/example/example.md",output_dir="./output")
doc.generate_tex("example")


# doc = Scanner.analyse_file("./marktex/example/example.md")
# print(doc)