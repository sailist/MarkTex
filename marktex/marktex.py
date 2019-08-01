import argparse,sys,os


APP_DESC="""
MarkTex is used to convert markdown document into tex format.
"""
print(APP_DESC)
if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser()
'''
输出位置可以选择：
- 在各自的md文件下 default，最低优先级
- 统一输出到一个目录下 -o "path" ，第二优先级
- 在各自给定的目录下 -e "",优先级最高
'''
parser.add_argument('mdfiles', metavar='mdfiles', type=str, nargs='+',
                    help='place markdown path')
parser.add_argument('-o','--output',type=str,default=None,help="download video quality : 1 for the standard-definition; 3 for the super-definition")
# parser.add_argument('-d','--dir', default=None,help="print more debuging information")
parser.add_argument('-e','--every',help="保存流媒体文件到指定位置",nargs="*")
# parser.add_argument('-c','--config',default=0,help="读取~/.danmu.fm配置,请~/.danmu.fm指定数据库")
# parser.add_argument('url',metavar='URL',nargs='+', help="zhubo page URL (http://www.douyutv.com/*/)")
args = parser.parse_args()
# 获取对应参数只需要args.quality,args.url之类.
# url = (args.url)[0]
# print(url)



every = args.every
mdfiles = args.mdfiles
output = args.output
print(args)
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
