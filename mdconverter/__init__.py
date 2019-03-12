from .documents import MarkDocument
import os
# from containers import *
from .containers import parseforeach

def _excu(text):
    # text = excuInlineText(text)
    if type(text) == str:
        lines = text.split("\n")
    else:
        lines = [l.strip() for l in text]

    mdoc = MarkDocument()

    mdoc.content += parseforeach(lines)
    # lines = _sub_Bold_Itali(lines)
    return mdoc.toLabex()



def from_file(fname,tofile = None):
    if not os.path.exists(fname) or not os.path.isfile(fname):
        print("the first param must be a exist file, not {}".format(fname))
    if tofile is None:
        path,fn = os.path.split(fname)
        fn,_ = os.path.splitext(fn)
        tofile = path + "/" + fn + ".tex"


    with open(fname,encoding="utf-8") as f,open(tofile,"w",encoding="utf-8") as w:
        result = _excu(f.readlines())
        w.write(result)

    print("convert success.")

def from_files(fdir):
    if os.path.exists(fdir) and os.path.isdir(fdir):
        fs = os.listdir(fdir)
        for f in fs:
            from_file(fdir + f)
    else:
        print("the first param must be a exist dir,not {}".format(fdir))

