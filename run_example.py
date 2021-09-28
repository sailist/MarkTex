from marktex import api
import os

base = 'marktex/example'
fs = os.listdir(base)
fs = [os.path.join(base, f) for f in fs if f.endswith('.md')][0:1]

api.convert(*fs, output_dir='./outputs')  # 全部输出到该目录下 # 不推荐设置缓存图片目录
