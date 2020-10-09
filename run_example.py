from marktex.example import run_example

# run_example("./output/")


from marktex.texrender.toTex import MarkTex

from marktex.markast.parser import Scanner

doc = MarkTex.convert_file("./marktex/example/example.md",output_dir="./output")
# doc = MarkTex.convert_file(r"C:\Users\saili\Desktop\机器学习\chap3_线性回归\chap3_线性回归.md")
# doc = MarkTex.convert_file(r"C:\Users\saili\Desktop\机器学习\chap3_线性回归\数据结构-数组和矩阵.md",templete=r"E:\si智库\知识见解LaTeX模板-2019年11月6日\markenv.tex")
doc.generate_tex("example")


# doc = Scanner.analyse_file("./marktex/example/example.md")
# print(doc)