from typing import Any

import re, os, shutil, imghdr
from hashlib import md5
import os

_request_headers_dict = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                         "Accept-Language": "en-us",
                         "Connection": "keep-alive",
                         "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"
                         }


def norm_path(path: str):
    return path.replace("\\", "/")


class ImageTool:
    @staticmethod
    def equal(a, b):
        return os.path.getsize(a) == os.path.getsize(b) and \
               os.path.getmtime(a) == os.path.getmtime(b)

    @staticmethod
    def hashmove(pref: str, fdir: str) -> str:
        pref = os.path.abspath(pref)
        size = os.path.getsize(pref)
        mtime = os.path.getmtime(pref)
        mmd = md5()
        mmd.update(str(size + mtime).encode())

        _, ext = os.path.splitext(pref)
        if ext.lower() not in ["jpg", "png"]:
            ext = "png"
            import matplotlib.pyplot as plt
            pimg = plt.imread(pref)
            newf = os.path.join(fdir, "{}.{}".format(mmd.hexdigest(), ext))
            newf = os.path.abspath(newf)
            plt.imsave(newf, pimg)
            newf = norm_path(newf)
            return newf

        newf = os.path.join(fdir, "{}{}".format(mmd.hexdigest(), ext))
        newf = os.path.abspath(newf)

        if os.path.exists(newf) and ImageTool.equal(pref, newf):
            print("Have cache, checked.")
            newf = norm_path(newf)
            return newf
        else:
            shutil.copy2(pref, newf)

        print("Image is local file, move it \tfrom:{}\tto:{}".format(pref, newf))
        newf = norm_path(newf)
        return newf

    @staticmethod
    def verify(url: str, fdir: str, retry=10):
        '''
        如果是本地图片，那么就将其hash后移动到fdir中，hash值与文件大小、修改时间有关
        如果是网络图片，那么直接根据url得到hash值，下载到fdir中
        :param url:
        :param fdir:
        :return:
        '''
        print("\rCheck Image:{}.".format(url))
        os.makedirs(fdir, exist_ok=True)
        path_like = os.path.join(config.input_dir, url)

        if os.path.exists(path_like) and os.path.isfile(path_like):
            return ImageTool.hashmove(path_like, fdir)

        import requests
        import matplotlib.pyplot as plt

        mmd = md5()
        mmd.update(url.encode())

        fpre = os.path.join("{}".format(mmd.hexdigest()))

        fs = os.listdir(fdir)
        prefs = [os.path.splitext(f)[0] for f in fs]

        # fname = os.path.abspath(fname)
        if fpre in prefs:
            print("Have cache, checked.")
            i = prefs.index(fpre)
            fname = os.path.join(fdir, fs[i])
            return fname
        else:
            print("Image have't download, downloading...")

        for i in range(retry):
            fs = os.listdir(fdir)
            prefs = [os.path.splitext(f)[0] for f in fs]
            if fpre in prefs:
                print("Have cache, checked.")
                i = prefs.index(fpre)
                fname = os.path.join(fdir, fs[i])
                return norm_path(fname)

            try:
                response = requests.get(url, headers=_request_headers_dict, timeout=5, stream=True)
                if response.status_code == 200:
                    ext = imghdr.what(None, response.content)
                    if ext not in ["jpg", "png"]:
                        tempf = os.path.join(fdir, "temp.{}".format(ext))
                        with open(tempf, "wb") as w:
                            w.write(response.content)

                        tmpi = plt.imread(tempf)

                        fname = os.path.join(fdir, "{}.png".format(fpre))
                        plt.imsave(fname, tmpi)
                        return norm_path(fname)
                    else:
                        fname = os.path.join(fdir, "{}.{}".format(fpre, ext))
                        with open(fname, "wb") as w:
                            w.write(response.content)

                        return norm_path(fname)
            except:
                print("\r\ttimeout retry {}/{}, "
                      "you can manually download and save it in {} with name {}.[ext]".format(
                    i + 1, retry, fdir, fpre),
                    end="\0",
                    flush=True)

        return None


class Config:
    _instance = None

    def __init__(self,
                 downimg_retry=10,
                 marktemp_path=None,
                 give_rele_path=True):
        if Config._instance is not None:
            self = Config._instance

        if marktemp_path is None:
            marktemp_path = os.path.join(os.path.dirname(__file__), 'markenv.tex')

        self._input_dir = os.getcwd()
        self.change_to_input_dir(self._input_dir)
        self.give_rele_path = give_rele_path
        self.downimg_retry = downimg_retry
        self.marktemp_path = marktemp_path
        self.fig_position = 'H'  # 图片排版位置； H 为强制当前位置， h 为尽量， t 为顶部，b 为底部，p 为单独附页
        Config._instance = self

    @property
    def input_dir(self):
        return self._input_dir

    @property
    def output_dir(self):
        os.makedirs(self._output_dir, exist_ok=True)
        return self._output_dir

    @property
    def cacheimg_dir(self):
        os.makedirs(self._cacheimg_dir, exist_ok=True)
        return self._cacheimg_dir

    @staticmethod
    def get_instance():
        if Config._instance is None:
            return Config()
        return Config._instance

    def change_to_input_dir(self, ipt_dir, output_dir=None, cache_dir=None):
        self._input_dir = ipt_dir
        if output_dir is None:
            output_dir = os.path.join(ipt_dir, 'outputs')
        self._output_dir = output_dir
        if cache_dir is None:
            cache_dir = os.path.join(self._output_dir, 'imgs')
        self._cacheimg_dir = cache_dir


class Cache:
    _instance = None

    def __new__(cls) -> Any:
        if Cache._instance is not None:
            return Cache._instance
        return super().__new__(cls)

    def __init__(self):
        if Cache._instance is not None:
            return

        self.title = None
        self.author = None

        # self.has_toc = False
        self.footnote = []
        Cache._instance = self

    def clear(self):
        self.title = None
        self.author = None
        # self.has_toc = False
        self.footnote = []

    def add_footnote(self, tag, line):
        self.footnote.append([tag, line])

    def get_footnote(self, tag):
        for i in range(len(self.footnote)):
            if self.footnote[i][0] == tag:
                res = self.footnote[i][1]
                self.footnote.pop(i)
                return res
        return []

    @staticmethod
    def get_instance():
        return Cache()


config = Config.get_instance()
chchar = re.compile("([^\x00-\xff]+)")

cache = Cache()
