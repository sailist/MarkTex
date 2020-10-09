from marktex import api
import os

base = 'marktex/example'
fs = os.listdir(base)
fs = [os.path.join(base, f) for f in fs if f.endswith('.md')]

api.convert(*fs, output_dir='./outputs')  # 全部输出到该目录下 # 不推荐设置缓存图片目录
# api.convert(*fs)  # 根据各自的 md 文件所在的目录，输出到相应的 output 子目录下，图片缓存在 output/imgs 下

