from matplotlib import pyplot as plt
import os
from hashlib import md5





def transimg(img_path):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    # if IsValidImage(img_path):
    # try:
    mmd = md5()
    str = img_path.rsplit(".", 1)
    path,_ = os.path.split(img_path)
    output_img_path = str[0] + ".jpg"
    mmd.update(output_img_path.encode())
    output_img_path = path + "/" + mmd.hexdigest()+".jpg"
    # print(output_img_path)
    output_img_path = output_img_path.replace("\\", "/")
    if os.path.exists(output_img_path):
        return output_img_path

    img = plt.imread(img_path)
    plt.imsave(output_img_path,img)
    _remove(img_path)
    # im = Image.open()
    return output_img_path
    # except:
    #     return None

def _remove(fpath):
    os.remove(fpath)

# print(transimg(r"C:\E\jupyter_notebook\myTool\latexTool\img\9d9dbbca7fcc7dea8560db657ca70830.jpg"))