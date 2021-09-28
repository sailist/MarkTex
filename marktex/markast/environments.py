from typing import List
from marktex.util import config
import os
from .base import MetaComparable, regist_func
from collections import namedtuple
import re
import bisect
import sys

registed_env = []

Match = namedtuple('match', ['matched', 'start', 'end'])


def format_parent(env, mem=None):
    if mem is None:
        mem = []
    mem.insert(0, '{}'.format(env.__class__.__name__))
    if env.parent is not None:
        return format_parent(env.parent, mem)
    else:
        return '->'.join(mem)


class ENV_FLAG:
    # 不需要任何处理
    none = 1

    # 指转换的时候直接通过该环境类进行转换，不再进行更细粒度（行级别）的处理，包括 Code，Formula
    directly = 2

    bound = 4  # 指需要在外围包裹环境，内部的各行按照行级别的粒度进行处理，包括 Quote，MultiBox 系列


class Environ(metaclass=MetaComparable):
    priority = 0  # 相同优先级下按顺序，不同优先级下优先级越大越靠前

    TYPE = ENV_FLAG.directly
    RE = re.compile('.*')
    END_RE = RE

    def __init__(self, raw, left, right, parent=None):
        self.raw = raw
        self.pos = (left, right)
        self.inner = self.raw[left:right]
        self.parent = parent
        self.children_flag = None
        self.children = []  # 装 Environ 类和 str 类，然后会通过进一步递归处理成 Environ 类和 Line 类

    def __lt__(self, other):
        return self.pos < other.pos

    def preprocess(self):
        raise NotImplementedError(self.__class__.__name__)

    def __iter__(self):
        from .lines import Line
        for child in self.children:
            if isinstance(child, Line):
                yield child
            elif isinstance(child, Environ):
                for cchild in child:
                    yield cchild

    def set_lines(self):
        pass

    @classmethod
    def match(cls, lines: List[str], start, end):
        for id in range(start, end):
            if re.search(cls.RE, lines[id]):
                eid = id + 1

                while eid < end and re.search(cls.END_RE, lines[eid]):
                    eid += 1
                return Match(True, id, eid)
        return Match(False, -1, -1)

    def __str__(self):
        pchain = format_parent(self)
        return '\\begin{{{name}}}\n' \
               '{content}\n' \
               '\\end{{{name}}}'.format(name=pchain,
                                        content='\n'.join(str(i) for i in self.children))

    def __repr__(self):
        return self.__str__()


class Paramgraph(Environ):
    TYPE = ENV_FLAG.directly

    def preprocess(self):
        self.children.extend(self.inner)


@regist_func(registed_env)
class YAML(Environ):
    # code:list[RawLine]
    """行内自行处理"""
    TYPE = ENV_FLAG.none

    ignore_line = True
    RE = re.compile("^---")  # code
    END_RE = re.compile("^---$")

    def __init__(self, raw, left, right, parent=None):
        super().__init__(raw, left, right, parent)
        self.children_flag = ''
        self.config = {}

    def preprocess(self):
        """去掉上下的 ``` 然后将 lang 额外进行记录"""
        self.children_flag = ''
        try:
            import yaml
            from pprint import pformat
            res = yaml.safe_load("\n".join(self.inner[1:-1]))
            self.children.append(pformat(res))
            self.config = res
        except Exception as e:
            print(e, file=sys.stderr)
            self.children.extend(self.inner[1:-1])

    @property
    def language(self):
        return self.children_flag

    @classmethod
    def match(cls, lines: List[str], start, end):
        for id in range(start, end):
            if id != 0:
                break
            if re.search(cls.RE, lines[id]):
                eid = id + 1

                while eid < end and (not re.search(cls.END_RE, lines[eid])):
                    eid += 1
                return Match(True, id, eid + 1)
        return Match(False, -1, -1)

    def __str__(self):
        pchain = format_parent(self)
        return '\\begin{{{name}}}\n' \
               '{content}\n' \
               '\\end{{{name}}}'.format(name=pchain,
                                        content='\n'.join(
                                            str(i) for i in self.children))


@regist_func(registed_env)
class Quote(Environ):
    """
    > ...
    > ...
    > ...
    """
    TYPE = ENV_FLAG.bound

    RE = re.compile("^ *>(.*)")
    END_RE = RE

    def preprocess(self):
        """去掉标识前缀，重parse一遍，生成嵌套环境"""
        lines = self.inner[:]
        lines = [re.match(self.RE, l).group(1) for l in lines]
        params = parse_env(lines, matchers=[Quote,
                                            MultiBox, Itemize, Enumerate,
                                            Table, Code, Formula])
        for param in params:
            if isinstance(param, Paramgraph):
                self.children.extend(param.inner)
            else:
                param.parent = self
                self.children.append(param)  # Quote

    # def __str__(self):


@regist_func(registed_env)
class MultiBox(Environ):  # 复选框
    """
     - []
    """
    TYPE = ENV_FLAG.bound

    RE = re.compile(r"^( *)- \[([x√ ]?)\] ?(.*)")
    END_RE = RE

    def __init__(self, raw, left, right, parent=None):
        super().__init__(raw, left, right, parent)
        self.children_flag = []

    @property
    def check_levels(self):
        levels = []
        res = []
        for space, _ in self.children_flag:
            ss = len(space)
            while len(levels) > 0 and ss < levels[-1]:
                levels.pop()
            if len(levels) == 0:
                levels.append(ss)
            elif ss > levels[-1]:
                levels.append(ss)
            res.append(len(levels))
        return res

    @property
    def check_types(self):
        res = []
        for _, flag in self.children_flag:
            if flag == 'x':
                res.append(2)
            if flag == '√':
                res.append(1)
            else:
                res.append(0)
        return res

    def preprocess(self):
        """
        去掉标识前缀
        :return:
        """
        lines = self.inner[:]
        for line in lines:
            match = re.match(self.RE, line)
            if match is not None:
                self.children_flag.append([match.group(1), match.group(2)])
                self.children.append(match.group(3))
            else:
                match = re.match(Itemize.RE, line)
                if match is None:
                    match = re.match(Enumerate.RE, line)
                self.children_flag.append([match.group(1), None])
                self.children.append(match.group(2))

    @classmethod
    def match(cls, lines: List[str], start, end):
        for id in range(start, end):
            if re.search(cls.RE, lines[id]):
                eid = id + 1

                while eid < end and (re.search(cls.END_RE, lines[eid])):
                    eid += 1
                return Match(True, id, eid)
        return Match(False, -1, -1)


@regist_func(registed_env)
class Itemize(MultiBox):  # 包括Itemize和Enumerate
    """
    - ...
     - ...
    """
    RE = re.compile("^( *)[-+] *(.*)")
    END_RE = RE

    def preprocess(self):
        """
        去掉标识前缀
        :return:
        """
        lines = self.inner[:]
        matched = [re.match(self.RE, l) for l in lines]
        for match in matched:
            self.children_flag.append(match.group(1))
            self.children.append(match.group(2))


@regist_func(registed_env)
class Enumerate(Itemize):  # 包括Itemize和Enumerate
    """
    1. ...
    2....
     3. ...
    """
    RE = re.compile("^( *)[0-9]+\. *(.*)")
    END_RE = RE


@regist_func(registed_env)
class Formula(Environ):
    """行内自行处理"""
    TYPE = ENV_FLAG.none

    RE = re.compile("^ *\$\$")
    SAME_RE = re.compile("^ *\$\$.*\$\$")
    END_RE = re.compile("\$\$$")

    def preprocess(self):
        """
        去掉两侧的 $$
        :return:
        """
        lines = self.inner[:]
        lines = [re.sub(self.RE, '', l) for l in lines]
        lines = [re.sub(self.END_RE, '', l) for l in lines]
        lines = [line.strip() for line in lines if len(line.strip()) > 0]
        self.children.extend(lines)

    @classmethod
    def match(cls, lines: List[str], start, end):
        for id in range(start, end):
            if re.search(cls.SAME_RE, lines[id]):
                return Match(True, id, id + 1)
            if re.search(cls.RE, lines[id]):
                eid = id + 1
                while eid < end and (not re.search(cls.END_RE, lines[eid])):
                    eid += 1
                return Match(True, id, eid + 1)
        return Match(False, -1, -1)


@regist_func(registed_env)
class IncludeTex(Environ):
    RE = re.compile("^ *<include>(.+tex)<\/include>")
    TYPE = ENV_FLAG.none

    def preprocess(self):
        """去掉标识前缀，重parse一遍，生成嵌套环境"""
        raw = self.inner[0]
        filename = re.match(self.RE, raw).group(1)
        filename = os.path.join(config.input_dir, filename)
        with open(filename, 'r', encoding='utf-8') as r:
            lines = r.readlines()
            self.children.extend(lines)

    @classmethod
    def match(cls, lines: List[str], start, end):
        for id in range(start, end):
            if re.search(cls.RE, lines[id]):
                return Match(True, id, id + 1)
        return Match(False, -1, -1)


@regist_func(registed_env)
class IncludeMd(Environ):
    RE = re.compile("^ *<include>(.+md)<\/include>")

    def preprocess(self):
        """去掉标识前缀，重parse一遍，生成嵌套环境"""

        raw = self.inner[0]
        filename = re.match(self.RE, raw).group(1)
        filename = os.path.join(config.input_dir, filename)
        with open(filename, 'r', encoding='utf-8') as r:
            lines = r.readlines()
            lines = [i.strip() for i in lines]

        params = parse_env(lines)
        for param in params:
            param.parent = self
        self.children.extend(params)

    @classmethod
    def match(cls, lines: List[str], start, end):
        for id in range(start, end):
            if re.search(cls.RE, lines[id]):
                return Match(True, id, id + 1)
        return Match(False, -1, -1)


@regist_func(registed_env)
class Code(Environ):
    # code:list[RawLine]
    """行内自行处理"""
    TYPE = ENV_FLAG.none

    ignore_line = True
    RE = re.compile("^ *```(.*)")  # code
    END_RE = re.compile("^.*```")

    def __init__(self, raw, left, right, parent=None):
        super().__init__(raw, left, right, parent)
        self.children_flag = ''

    def preprocess(self):
        """去掉上下的 ``` 然后将 lang 额外进行记录"""

        self.children_flag = re.match(self.RE, self.inner[0]).group(1)
        self.children.extend(self.inner[1:-1])

    @property
    def language(self):
        return self.children_flag

    @classmethod
    def match(cls, lines: List[str], start, end):
        for id in range(start, end):
            if re.search(cls.RE, lines[id]):
                eid = id + 1

                while eid < end and (not re.search(cls.END_RE, lines[eid])):
                    eid += 1
                return Match(True, id, eid + 1)
        return Match(False, -1, -1)

    def __str__(self):
        pchain = format_parent(self)
        return '\\begin{{{name}}}[lang={flag}]\n' \
               '{content}\n' \
               '\\end{{{name}}}'.format(name=pchain,
                                        flag=self.children_flag,
                                        content='\n'.join(
                                            str(i) for i in self.children))


@regist_func(registed_env)
class Table(Environ):
    """行内自行处理"""
    # TYPE = ENV_FLAG
    ignore_line = True
    RE = re.compile("^\|(.*\|)+")  # table
    SEC_RE = re.compile("^\|(:?-+:?\|)+")
    ROW_RE = re.compile(r"(?=\|([^|\n]*)\|)")
    END_RE = RE

    def preprocess(self):
        """获取到相应的表格"""
        col_num = None
        col_max_lens = None
        for i, line in enumerate(self.inner):
            if i == 1:  # 略过第二行
                continue

            cols = re.findall(self.ROW_RE, line)
            if col_num is None:
                col_num = len(cols)
            elif col_num != len(cols):
                raise Exception("Tabel's column num must be equal,but {}".format(len(cols)))

            if col_max_lens is None:
                col_max_lens = [len(i) for i in cols]
            else:
                col_max_lens = [max(i, len(j)) for i, j in zip(col_max_lens, cols)]

            self.children.extend(cols)
        self.children_flag = (col_num, len(self.inner) - 1, col_max_lens)
        # self.shape =
        # self.col_max_lens = col_max_lens

    @property
    def shape(self):
        return self.children_flag[0], self.children_flag[1]

    @property
    def col_max_lens(self):
        return self.children_flag[-1]

    @classmethod
    def match(cls, lines: List[str], start, end):
        for id in range(start, end):
            if re.search(cls.RE, lines[id]):
                eid = id + 1
                if eid < end and re.search(cls.SEC_RE, lines[eid]):
                    eid += 1
                else:
                    break
                while eid < end and re.search(cls.END_RE, lines[eid]):
                    eid += 1
                return Match(True, id, eid)
        return Match(False, -1, -1)

    def __str__(self):
        pchain = format_parent(self)
        col, row = self.shape
        _res = []
        for left in range(0, col * row, col):
            _res.append('|'.join([str(i) for i in self.children[left:left + col]]))
        return '\\begin{{{name}}}\n' \
               '{content}\n' \
               '\\end{{{name}}}'.format(name=pchain,
                                        flag=self.children_flag,
                                        content='\n'.join(_res))

    def iter_rows(self):
        col, row = self.shape
        _res = []
        for left in range(0, col * row, col):
            yield self.children[left:left + col]

    def cacu_col_ratio(self):
        col_max_lens = [min(i, 10) for i in self.col_max_lens]
        ratio = [i / sum(col_max_lens) for i in col_max_lens]

        return ["{:.3f}".format(i) for i in ratio]


def parse_env(lines, istart=None, iend=None, matchers=None):
    """将行划分为段落，最终返回一个 List[Environ]"""
    if istart is None:
        istart = 0
    if iend is None:
        iend = len(lines)
    if matchers is None:
        matchers = registed_env
    clips = [[istart, iend]]

    lines = [line.rstrip() for line in lines]

    params = []
    while len(clips) > 0:
        start, end = clips.pop(0)
        matched = False
        for matcher in matchers:
            res = matcher.match(lines, start, end)
            if res[0]:
                if res[1] > start:
                    clips.append([start, res[1]])
                if res[2] < end:
                    clips.append([res[2], end])
                bisect.insort(params, matcher(lines, res[1], res[2]))
                matched = True
                break
        if not matched:
            bisect.insort(params, Paramgraph(lines, start, end))

    return params
