"""
用于 debug
"""
from marktex import api
import os

base = 'marktex/example'
fs = os.listdir(base)
fs = [os.path.join(base, f) for f in fs if f.endswith('.md')]

parser = api.Parser()
ast = parser.parse_md_ast_from_file('marktex/example/yaml_head.md')
# ast = parser.parse_md_ast_from_file('marktex/example/form.md')

print(ast[4].check_levels)
parser.print_ast(ast)
# doc = parser.ast_to_texdoc(ast)
# print(doc.dumps())
# api.convert(*fs, output_dir='./outputs')  # 全部输出到该目录下 # 不推荐设置缓存图片目录
# api.convert(*fs)  # 根据各自的 md 文件所在的目录，输出到相应的 output 子目录下，图片缓存在 output/imgs 下
