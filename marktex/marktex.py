import argparse,sys,os


APP_DESC="""
MarkTex is used to convert markdown document into tex format.

输出位置可以选择：
- 在各自的md文件下 default，最低优先级
- 统一输出到一个目录下 -o "path" ，第二优先级
- 在各自给定的目录下 -e "",优先级最高

输出到对应文件的 "文件名" 所在的目录下：
    marktex a.md b.md ...

输出到一个同一的文件夹下：
    marktex a.md b.md ... -o "path"

指定输出到各自文件夹，必须保证路径个数和文件个数相同：
    marktex a.md b.md ... -e "pathfora" "pathforb" ...
    
"""
if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser()

parser.add_argument('mdfiles', metavar='mdfiles', type=str, nargs='+',
                    help='place markdown path')
parser.add_argument('-o','--output',type=str,default=None,help="指定统一路径")
parser.add_argument('-e','--every',help="为每个文件分配路径",nargs="*")
args = parser.parse_args()



every = args.every
mdfiles = args.mdfiles
output = args.output
output_paths = []

if every is not None:
    if len(every) != len(mdfiles):
        print("you ues -e option, the number of outputdirs must be equal to markdown files.")
        exit(1)
    output_paths = every
elif output is not None:
    output_paths = [output]*len(mdfiles)
else:
    for mdfile in mdfiles:
        mdfile = os.path.abspath(mdfile)
        mdpath,fname = os.path.splitext(mdfile)
        output_paths.append(mdpath)

from marktex.texrender.toTex import MarkTex
for mdfile,opath in zip(mdfiles,output_paths):
    _,fname = os.path.split(mdfile)
    fpre,_ = os.path.splitext(fname)
    doc = MarkTex.convert_file(mdfile,opath)
    doc.generate_tex(fpre)

print(f"[info*]convert finished.")
exit(0)
