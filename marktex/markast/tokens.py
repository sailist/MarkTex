import re
from . import lines
from . import environments
from .base import MetaComparable, regist_func
import bisect
from collections import namedtuple

MatchToken = namedtuple('MatchToken', ['matched', 'outer_pos', 'inner_pos', 'flag'])

registed_token = []


class Token(metaclass=MetaComparable):
    priority = 0
    ignore_nest = False
    RE = re.compile('.*')
    NEST_GROUP = None

    def __init__(self, token, out_pos, inner_pos, parent=None, flags=None):
        self.raw = token
        self.out_pos = out_pos
        self.inner_pos = inner_pos
        self.parent = parent
        self.token_flags = flags
        self.inner_token = [token[inner_pos[0]: inner_pos[1]]]

    def __lt__(self, other):
        return self.out_pos[0] < other.out_pos[0]

    @classmethod
    def match(cls, line, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = len(line)

        res = re.search(cls.RE, line[start:end])
        if res is not None:
            pos = (res.start() + start, res.end() + start)
            if cls.NEST_GROUP is None:
                inner_pos = pos[:]
            else:
                inner_pos = (res.start(cls.NEST_GROUP) + start, res.end(cls.NEST_GROUP) + start)
            gp = list(res.groups())
            if len(gp) == 0:
                gp = None
            if cls.NEST_GROUP is not None:
                gp.pop(cls.NEST_GROUP - 1)
            return MatchToken(True, pos, inner_pos, gp)
        else:
            return MatchToken(False, (-1, -1), (-1, -1), None)

    @property
    def token_str(self):
        return ''.join([str(token) for token in self.inner_token])

    def __str__(self):
        return "<{name}>{content}</{name}>".format(name=self.__class__.__name__,
                                                   content=self.token_str)

    def __repr__(self):
        return self.__str__()


class Raw(Token):
    ignore_nest = True


class Normal(Token):
    ignore_nest = True

    def __str__(self):
        return "{}".format(''.join(self.inner_token))


@regist_func(registed_token)
class InCode(Token):
    """
    `Text`
    """
    ignore_nest = True
    RE = re.compile("`([^`\n]+)`")
    NEST_GROUP = 1


@regist_func(registed_token)
class InFormula(Token):
    """
    $Text$
    """
    ignore_nest = True
    RE = re.compile("\$([^$\n]+)\$")
    NEST_GROUP = 1


@regist_func(registed_token)
class BoldItalic(Token):
    """
    **Text**
    """
    RE = re.compile(r"\*\*\*([^*\n]*)\*\*\*")
    NEST_GROUP = 1


@regist_func(registed_token)
class Bold(Token):
    """
    **Text**
    """
    RE = re.compile(r"\*\*([^*\n]*)\*\*")
    NEST_GROUP = 1


@regist_func(registed_token)
class Italic(Bold):
    """
    *Text*
    """
    RE = re.compile(r"\*([^*\n]+)\*")


@regist_func(registed_token)
class DeleteLine(Bold):
    """
    ~~text~~
    """
    RE = re.compile(r"~~([^~\n]+)~~")


@regist_func(registed_token)
class UnderLine(Bold):
    """
    __text__
    """
    RE = re.compile(r"__([^_\n]+)__")


@regist_func(registed_token)
class InlineImage(Token):
    RE = re.compile("!\[([^\[\n]*)\]\(([^(\n]+)\)")  # image
    NEST_GROUP = 1

    @property
    def link(self):
        return self.token_flags[0]

    @property
    def desc(self):
        return self.token_str

    def __str__(self):
        return '<{cls} src="{link}">{content}</{cls}>'.format(
            cls=self.__class__.__name__,
            link=self.token_flags[0],
            content=self.token_str)


@regist_func(registed_token)
class Hyperlink(InlineImage):
    """
    [text](link)
    """
    RE = re.compile("\[([^[\n]*)\]\(([^(\n]*)\)")  # link


@regist_func(registed_token)
class Footnote(Token):
    ignore_nest = True
    """
    [^text]
    """
    RE = re.compile(r"\[\^([^[^]+)\]")
    NEST_GROUP = 1

    @property
    def label(self):
        return self.token_str


@regist_func(registed_token)
class InXML(Token):
    RE = re.compile("<(.+)>(.+)<\/(.+)>")
    NEST_GROUP = 2

    @property
    def tag(self):
        return self.token_flags[0]

    def __str__(self):
        return '<Xml:{tag}>{content}</Xml:{tag}>'.format(tag=self.token_flags[0],
                                                         content=self.token_str)


@regist_func(registed_token)
class Sign(Token):
    ignore_nest = True
    RE = re.compile('([αβγδεζηθικλμνξοπρστυφχψω'
                    'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
                    '±×÷'
                    '∣∤⋅∘∗⊙⊕≤≥≠≈≡'
                    '∑∏∐∈∉'
                    '⊂⊃⊆⊇⊄∧∨'
                    '∩∪∃∀∇⊥∠∞∘′'
                    '∫∬∭↑↓←→↔↕])')
    NEST_GROUP = 1

    @property
    def tex_name(self):
        return 'latin'


@regist_func(registed_token)
class TeXSign(Token):
    ignore_nest = True
    RE = re.compile(r'(\\TeX)')


@regist_func(registed_token)
class LaTeXSign(Token):
    ignore_nest = True
    RE = re.compile(r'(\\LaTeX)')


def parse_tokens(params):
    for param in params:
        for line in param:
            line.children = parse_token(line)


def parse_token(line: lines.Line, istart=None, iend=None, matchers=None, parent=None):
    line.preprocess()
    if parent is None:
        parent = line

    if istart is None:
        istart = 0
    if iend is None:
        iend = len(line)

    if line.ignore_token:
        return [Raw(line.line, (istart, iend), (istart, iend), line)]

    if line.parent.TYPE == environments.ENV_FLAG.none:
        if isinstance(line.parent, environments.Formula):
            matchers = [Sign, Raw]
        else:
            return [Raw(line.line, (istart, iend), (istart, iend), line)]

    if matchers is None:
        matchers = registed_token

    clips = [[istart, iend]]

    params = []
    while len(clips) > 0:
        start, end = clips.pop(0)
        matched = False
        for matcher in matchers:
            res, pos, inner_pos, flags = matcher.match(line.line, start, end)
            if res:
                if pos[0] > start:
                    clips.append([start, pos[0]])
                if pos[1] < end:
                    clips.append([pos[1], end])

                token = matcher(line.line, pos, inner_pos, parent, flags)  # type:Token

                if not token.ignore_nest:
                    token.inner_token = parse_token(line, inner_pos[0], inner_pos[1], parent=token)
                elif isinstance(token, (InFormula, InCode)):
                    token.inner_token = parse_token(line, inner_pos[0], inner_pos[1],
                                                    matchers=[Sign, Raw],
                                                    parent=token)

                bisect.insort(params, token)
                matched = True
                break
        if not matched:
            bisect.insort(params, Normal(line.line, (start, end), (start, end), line))

    return params
