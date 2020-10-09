from .base import MetaComparable, regist_func
from marktex.util import Cache, cache
from typing import List
import re
from collections import namedtuple

MatchLine = namedtuple('MatchLine', ['matched', 'flags'])

registed_lines = []


class Line(metaclass=MetaComparable):
    priority = 0  # 相同优先级下按顺序，不同优先级下优先级越大越靠前

    ignore_token = False  # 将其内部内容转换为 RawToken 而不是进行额外的转换
    RE = re.compile('.*')

    def __init__(self, lines, id, parent, flag=None):
        self.raw = lines
        self.pos = (id, id + 1)
        self.inner = self.raw[id: id + 1]
        self.parent = parent
        self.children = []  # store tokens
        self.children_flag = flag

    def __len__(self):
        return len(self.line)

    def preprocess(self):
        pass

    @classmethod
    def match(cls, line):
        """按优先级顺序判断行类别"""
        res = re.search(cls.RE, line)
        if res is not None:
            gp = list(res.groups())
            return MatchLine(True, gp)
        else:
            return MatchLine(False, None)

    @property
    def line(self):
        return self.inner[0]

    def __str__(self):
        return '\\{tag}{{{content}}}'.format(tag=self.__class__.__name__,
                                             content=''.join(str(i) for i in self.children))


class Raw(Line):
    pass


class Normal(Line):
    """普通行，支持所有 Token 特性"""
    pass


@regist_func(registed_lines)
class Section(Line):
    """\section{} ，单独成行"""
    RE = re.compile(r"^(#+)(.*)")  # 章节

    @property
    def line(self):
        return self.content

    @property
    def level(self):
        return len(self.children_flag[0])

    @property
    def content(self):
        return self.children_flag[1].strip()


@regist_func(registed_lines)
class Image(Line):
    """![]() 单独成行"""
    RE = re.compile("^!\[([^[\n]*)\]\(([^(\n]*)\)")  # image
    ignore_token = True

    @property
    def link(self):
        return self.children_flag[1]

    @property
    def desc(self):
        return self.children_flag[0]


@regist_func(registed_lines)
class Empty(Line):
    """空行"""
    RE = re.compile("^ *$")


@regist_func(registed_lines)
class TOC(Line):
    """[toc]"""
    RE = re.compile(r"^@?\[[Tt][Oo][Cc]\]")  # 目录
    ignore_token = True


@regist_func(registed_lines)
class FootnoteLine(Line):
    """
    [^...]:...
    """
    RE = re.compile(r"^\[\^(.+)\]:(.*)")  # footnote
    ignore_token = False

    @property
    def line(self):
        return self.content

    def preprocess(self):
        # footnote[self.tag] = self
        cache.add_footnote(self.tag, self)
        # print(footnote)

    @property
    def tag(self):
        return self.children_flag[0]

    @property
    def content(self):
        return self.children_flag[1]


@regist_func(registed_lines)
class XML(Line):
    RE = re.compile("^ *<(.+)>(.+)<\/(.+)>")
    ignore_token = True
    RECO = ['author', 'title']

    @property
    def tag(self):
        return self.children_flag[0]

    @property
    def content(self):
        return self.children_flag[1]

    @classmethod
    def match(cls, line):
        """按优先级顺序判断行类别"""
        res = re.search(cls.RE, line)
        if res is not None:
            gp = list(res.groups())
            if gp[0] not in cls.RECO:
                return MatchLine(False, None)

            return MatchLine(True, gp)
        else:
            return MatchLine(False, None)


def parse_lines(params: list, matchers=None):
    """
    将每一个 Environment 中的 行 范围变成真的 Line

    其中 表格需要单独
    :param params:
    :param matchers:
    :return:
    """
    from . import environments as env
    if matchers is None:
        matchers = registed_lines

    from . import environments as env
    for param in params:  # type: env.Environ
        param.preprocess()
        for idx in range(len(param.children)):
            child = param.children[idx]
            if isinstance(child, str):
                if not (param.TYPE & env.ENV_FLAG.none):
                    matched = False
                    for match in matchers:
                        res = match.match(child)
                        if res[0]:
                            param.children[idx] = match(param.children, idx, param, res[1])
                            matched = True
                            break
                    if not matched:
                        param.children[idx] = Normal(param.children, idx, param)
                else:
                    param.children[idx] = Raw(param.children, idx, param)
            elif isinstance(child, env.Environ):
                parse_lines([child])
    return params
