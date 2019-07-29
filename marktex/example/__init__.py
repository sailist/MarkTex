from marktex.texrender.toTex import MarkTex
import os

def run_example(output_dir,fname = None):
    path,_ = os.path.split(__file__)
    md_file = os.path.join(path,"example.md")

    os.makedirs(output_dir,exist_ok=True)
    image_dir = os.path.join(output_dir,"images")
    doc = MarkTex.convert_from_file(md_file,image_dir=image_dir)

    if fname is None:
        fname = "example"
    
    output_fpath = os.path.join(output_dir,fname)
    doc.generate_tex(output_fpath)
    
    