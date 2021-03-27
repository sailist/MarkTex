from marktex.util import cache, config, ImageTool, norm_path
from .base import (registed_env_decoder,
                   registed_line_decoder, registed_token_decoder, regist_decoder, sign_to_tex,
                   registed_line_xml_decoder)
import os

from typing import List
from pylatex.utils import bold, italic, escape_latex
from pylatex import NoEscape, Center
from pylatex import Section as TSection, Subsection, Subsubsection
from pylatex import Figure

from pylatex.section import Paragraph as TParagraph, Subparagraph
from pylatex import Itemize as TItem, Enumerate as TEnum, Tabular, Math
from marktex.markast import environments as env
from marktex.markast import lines
from marktex.markast import tokens

from . import texunit as tex
from marktex import re


@regist_decoder(registed_env_decoder, env.Paramgraph)
def de_paramgraph(s: env.Paramgraph):
    clines = [de_line(c) for c in s.children]
    t = tex.Text()

    empty = True
    for line in clines:
        t.append(line)
        empty = False

    if empty:
        return NoEscape("\n")
    return t


@regist_decoder(registed_env_decoder, env.IncludeMd)
def de_include_md(s: env.IncludeMd):
    clines = []
    for child in s.children:
        if isinstance(child, env.Environ):
            clines.append(de_env(child))
        else:
            clines.append(de_line(child))

    q = tex.Text()
    for envi in clines:
        q.append(envi)
        q.append(NoEscape("\n"))

    return q


@regist_decoder(registed_env_decoder, env.IncludeTex)
def de_include_tex(s: env.IncludeTex):
    clines = []
    for child in s.children:
        clines.append(de_line(child))
    q = tex.Text()
    for envi in clines:
        q.append(envi)
        q.append(NoEscape("\n"))

    return q


@regist_decoder(registed_env_decoder, env.Quote)
def de_quote(s: env.Quote):
    clines = []
    for child in s.children:
        if isinstance(child, env.Environ):
            clines.append(de_env(child))
        else:
            clines.append(de_line(child))

    q = tex.QuoteEnvironment()
    for envi in clines:
        q.append(envi)
        q.append(NoEscape("\n"))

    return q


@regist_decoder(registed_env_decoder, env.MultiBox)
def de_multiBox(s: env.MultiBox):
    clines = [de_line(c) for c in s.children]
    cl = tex.CheckList()
    for [ct, s] in zip(s.check_types, clines):
        cl.add_item(ct, s)
    return cl


@regist_decoder(registed_env_decoder, env.Itemize)
def de_itemize(s: env.Itemize):
    tokens = [de_line(c) for c in s.children]
    ui = TItem()
    for line in tokens:
        ui.add_item(line)
    return ui


@regist_decoder(registed_env_decoder, env.Enumerate)
def de_enumerate(s: env.Enumerate):
    tokens = [de_line(c) for c in s.children]
    ui = TEnum()
    for line in tokens:
        ui.add_item(line)
    return ui


@regist_decoder(registed_env_decoder, env.Formula)
def de_formula(s: env.Formula):
    code = [de_line(c) for c in s.children]
    chchar = re.compile("([^\x00-\xff]+)")
    data = []
    for line in code:
        line = re.sub(chchar, lambda x: r"\text{{{}}}".format(x.group(1)), line)
        data.append(NoEscape("{}\\\\".format(line)))

    m = Math(data=data)
    return m


@regist_decoder(registed_env_decoder, env.Code)
def de_code(s: env.Code):
    code = [de_line(c) for c in s.children]
    c = tex.CodeEnvironment(s.language)
    for line in code:
        line = line.replace("\t", "    ")  # 空格更舒适一些
        c.append(NoEscape(line))
    return c


@regist_decoder(registed_env_decoder, env.Table)
def de_table(s: env.Table):
    col, row = s.shape

    c = Center()
    # c.append(NoEscape(r"\newlength\q"))
    c.append(
        NoEscape(
            r"\setlength\tablewidth{{\dimexpr (\textwidth -{}\tabcolsep)}}".format(2 * col)))
    c.append(NoEscape(r"\arrayrulecolor{tablelinegray!75}"))
    c.append(NoEscape(r"\rowcolors{2}{tablerowgray}{white}"))

    ratios = s.cacu_col_ratio()
    format = "|".join([r"p{{{r}\tablewidth}}<{{\centering}}".format(r=r) for r in ratios])
    format = "|{format}|".format(format=format)

    t = Tabular(format)
    t.add_hline()
    for i, row in enumerate(s.iter_rows()):
        if i == 0:
            t.append(NoEscape(r"\rowcolor{tabletopgray}"))

        row = [de_line(c) for c in row]
        if i == 0:
            row = [bold(c) for c in row]

        t.add_row(row)
        t.add_hline()

    c.append(t)
    return c


@regist_decoder(registed_line_decoder, lines.Raw)
def de_raw_line(c: lines.Raw):
    return NoEscape(''.join([de_token(c) for c in c.children]))


@regist_decoder(registed_line_decoder, lines.Normal)
def de_normal(c: lines.Normal):
    content = NoEscape("".join([de_token(c) for c in c.children]))
    return content


@regist_decoder(registed_line_decoder, lines.Section)
def de_section(s: lines.Section):
    level, content = s.level, s.children
    content = NoEscape("".join([de_token(c) for c in content]))
    if s.level == 1:
        sec = TSection(content, label=False)
    elif level == 2:
        sec = Subsection(content, label=False)
    elif level == 3:
        sec = Subsubsection(content, label=False)
    elif level == 4:
        sec = TParagraph(content, label=False)
    elif level == 5:
        sec = Subparagraph(content, label=False)
    else:
        assert False

    return sec


@regist_decoder(registed_line_decoder, lines.Image)
def de_image(s: lines.Image):
    img_path = ImageTool.verify(s.link, config.cacheimg_dir)

    if img_path is None:
        c = Center()
        c.append(NoEscape('Link or path not found: {}'.format(s.link)))
        return c

    if config.give_rele_path:
        img_path = os.path.relpath(img_path, config.output_dir)
    img_path = norm_path(img_path)

    c = Center()
    if isinstance(s.parent, env.Quote):
        c.append(NoEscape(r"\includegraphics[width=0.8\textwidth]{{{img_path}}}".format(img_path=img_path)))
    else:
        fig = Figure(position=config.fig_position)
        fig.add_image(img_path, placement='')
        if len(s.desc.strip()) > 0:
            fig.add_caption(s.desc)
        c.append(fig)
    return c


@regist_decoder(registed_line_decoder, lines.Empty)
def de_empty(_):
    return NoEscape("\n")


@regist_decoder(registed_line_decoder, lines.TOC)
def de_toc(_):
    return tex.tablecontent()


@regist_decoder(registed_line_decoder, lines.FootnoteLine)
def de_footnote_line(s: lines.FootnoteLine):
    return ''
    # return NoEscape(r"\footnote{{{}}}".format(''.join(s)))


@regist_decoder(registed_line_decoder, lines.XML)
def de_xml(c: lines.XML):
    if c.tag == 'title':
        cache.title = NoEscape(r"\title{{{}}}".format(c.content))
    elif c.tag == 'author':
        cache.author = NoEscape(r"\author{{{}}}".format(c.content))
    return NoEscape('')


@regist_decoder(registed_token_decoder, tokens.Raw)
def de_raw(s: tokens.Raw):
    if isinstance(s.parent, (lines.Raw, tokens.InFormula)):
        return NoEscape(''.join(s.inner_token))
    elif isinstance(s.parent.parent, (env.Formula)):
        return NoEscape(''.join(s.inner_token))
    else:  # 当 父节点不是 lines.Raw 时， Raw 中的字符需要 escape，如 InFormula，InCode
        return escape_latex(''.join(s.inner_token))


@regist_decoder(registed_token_decoder, tokens.Normal)
def de_normal(s: tokens.Normal):
    return NoEscape(escape_latex(''.join(s.inner_token)))


@regist_decoder(registed_token_decoder, tokens.Bold)
def de_bold(s: tokens.Bold):
    return bold(NoEscape(''.join([de_token(c) for c in s.inner_token])), escape=False)


@regist_decoder(registed_token_decoder, tokens.Italic)
def de_italic(s: tokens.Italic):
    return italic(NoEscape(''.join([de_token(c) for c in s.inner_token])), escape=False)


@regist_decoder(registed_token_decoder, tokens.BoldItalic)
def de_bold_italic(s: tokens.BoldItalic):
    return bold(italic(NoEscape(''.join([de_token(c) for c in s.inner_token])), escape=False))


@regist_decoder(registed_token_decoder, tokens.DeleteLine)
def de_delete_line(s: tokens.DeleteLine):
    return tex.delete_line(NoEscape(''.join([de_token(c) for c in s.inner_token])), escape=False)


@regist_decoder(registed_token_decoder, tokens.UnderLine)
def de_under_line(s: tokens.UnderLine):
    return tex.under_line(NoEscape(''.join([de_token(c) for c in s.inner_token])))


@regist_decoder(registed_token_decoder, tokens.InCode)
def de_in_code(s: tokens.InCode):
    return tex.in_code(NoEscape(''.join(de_token(c) for c in s.inner_token)))


@regist_decoder(registed_token_decoder, tokens.InFormula)
def de_in_formula(s: tokens.InFormula):
    return tex.in_formula(''.join(de_token(c) for c in s.inner_token))


@regist_decoder(registed_token_decoder, tokens.InlineImage)
def de_inlineImage(s: tokens.InlineImage):
    img_path = ImageTool.verify(s.link, config.cacheimg_dir)
    if config.give_rele_path:
        img_path = os.path.relpath(img_path, config.output_dir)
    img_path = norm_path(img_path)

    return NoEscape(r"\raisebox{{-0.5mm}}{{\includegraphics[height=1em]{{{}}}}}".format(img_path))


@regist_decoder(registed_token_decoder, tokens.Hyperlink)
def de_hyperlink(s: tokens.Hyperlink):
    from urllib.parse import urljoin
    desc, link = NoEscape(''.join([de_token(c) for c in s.inner_token])), s.link
    link = urljoin('http:', link)
    return NoEscape(r"\href{{{}}}{{{}}}".format(link, desc))


@regist_decoder(registed_token_decoder, tokens.Footnote)
def de_footnote(s: tokens.Footnote):
    line = cache.get_footnote(s.token_str)
    return NoEscape(r"\footnote{{{}}}".format(''.join([de_token(c) for c in line.children])))


@regist_decoder(registed_token_decoder, tokens.InXML)
def de_in_xml(s: tokens.InXML):
    # return NoEscape(s.)
    if s.tag == 'sub':
        return NoEscape(r"\textsubscript{{{}}}".format(s.token_str))
    elif s.tag == 'super' or s.tag == 'sup':
        return NoEscape(r"\textsuperscript{{{}}}".format(s.token_str))
    assert False, 'unsupport xml tag {}'.format(s.tag)


@regist_decoder(registed_token_decoder, tokens.Sign)
def de_sign(s: tokens.Sign):
    tex_sign = sign_to_tex.get(s.token_str, 'unknown')
    if isinstance(s.parent, tokens.InFormula) or isinstance(s.parent.parent, env.Formula):
        return NoEscape(tex_sign)
    return NoEscape('$' + tex_sign + '$')


@regist_decoder(registed_token_decoder, tokens.TeXSign)
def de_texsign(s: tokens.TeXSign):
    return NoEscape('\\TeX')


@regist_decoder(registed_token_decoder, tokens.LaTeXSign)
def de_latexsign(s: tokens.LaTeXSign):
    return NoEscape('\\LaTeX')


def de_env(param: env.Environ):
    decoder = registed_env_decoder.get(type(param), None)
    assert callable(decoder), type(param)
    res = decoder(param)
    return res


def de_line(line: lines.Line):
    decoder = registed_line_decoder.get(type(line), None)
    assert callable(decoder), type(line)
    res = decoder(line)
    return res


def de_token(token: tokens.Token):
    """返回由 pylatex 包裹的对象"""
    decoder = registed_token_decoder.get(type(token), None)
    assert callable(decoder), type(token)
    res = decoder(token)
    if res is None:
        print(decoder)
        return str(token)
    return res


def decode_ast(params: List[env.Environ], templete=None) -> tex.MarkTex:
    if templete is not None:
        templete = config.marktemp_path

    doc = tex.MarkTex()
    if templete is None:
        templete = config.marktemp_path
    with open(templete, encoding="utf-8") as f:
        doc.preamble.append(NoEscape("".join(f.readlines())))

    tex_code = []
    for param in params:
        res = de_env(param)
        tex_code.append(res)

    if cache.title is not None:
        doc.preamble.append(cache.title)
    if cache.author is not None:
        doc.preamble.append(cache.author)

    if cache.title is not None and cache.author is not None:
        doc.append(tex.maketitle())

    for code in tex_code:
        doc.append(code)

    return doc
