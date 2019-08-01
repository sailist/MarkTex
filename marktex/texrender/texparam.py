from pylatex import NoEscape,Package
from marktex import config

def get_config(c = None):
    if c is None:
        c = config
    return c


def build_code_envi_options(c = None):
    c = get_config(c)
    options = []

    if c.has_number_left:
        options.append(NoEscape(r"numbers=left"))
        options.append(NoEscape(rf"numberstyle={c.code_number_size}"))
    options.append(NoEscape(rf"basicstyle={c.code_font_size}"))

    return options


def build_basic_package(c = None):
    c = get_config(c)

    packages = [Package("xcolor",["table"]),
                Package("lastpage"),
                Package("booktabs"),
                Package("pifont"),
                Package("fixltx2e"), #用于文本环境的下标
                Package("ulem"),
                Package("amssymb"),
                Package("colortbl"),
                Package("framed"),
                Package("color"),
                Package("adjustbox"),
                Package("array"),
                Package("titlesec"),
                Package("graphicx"),
                Package("graphics"),
                Package("showframe", "noframe"),
                _build_geometry(c),
                _build_hyperlink(c),
                ]

    return packages

def build_basic_preamble(c = None):
    c = get_config(c)
    preamble = [
        NoEscape(r"\newenvironment{marktext}{}{}"),# 用于 hline
        NoEscape(r'''\renewenvironment{shaded}{%
                     \def\FrameCommand{\fboxsep=\FrameSep \colorbox{shadecolor}}%
                     \MakeFramed{\advance\hsize-\width \FrameRestore\FrameRestore}}%
                    {\endMakeFramed}
                '''),
        NoEscape(r"\newlength\tablewidth"),
        _build_ctexset(c),
    ]
    preamble.extend(_build_sections_titleformat(c))
    preamble.extend(_build_newcolors(c))

    return preamble

def _build_geometry(c = None):
    c =get_config(c)
    unit = c.geometry_unit
    return Package("geometry",[f"left={c.geometry_border[0]}{unit}",
                               f"right={c.geometry_border[1]}{unit}",
                               f"top={c.geometry_border[2]}{unit}",
                               f"bottom={c.geometry_border[3]}{unit}",])

def _build_newcolors(c = None):
    c = get_config(c)
    preamble = []
    for k,[cs,v] in c.new_color_dict.items():
        if isinstance(v,float):
            v = f"{v}"
        elif isinstance(v,tuple):
            v = ",".join([str(i) for i in v])
        preamble.append(NoEscape(rf"\definecolor{{{k}}}{{{cs}}}{{{v}}}"))

    return preamble


def _build_hyperlink(c = None):
    c = get_config(c)

    # TODO hyperlink color setting
    return Package("hyperref", ["colorlinks",
                                "linkcolor=black",
                                "urlcolor=blue",
                                "anchorcolor=blue",
                                "citecolor=green"])

def _build_sections_titleformat(c = None):
    c = get_config(c)
    preamble = [
        # _build_section_titleformat(c),
        # _build_subsection_titleformat(c),
        # _build_subsubsection_titleformat(c),
    ]
    return preamble


def _build_ctexset(c = None):
    items = []
    items.extend(_build_toc_format(c))
    items.extend(_build_title_font(c))
    items = ",\n".join(items)
    return NoEscape(f"\ctexset{{\n{items}}}")

def _build_toc_format(c = None):
    '''
    \ctexset{
        section = {
            number = 第\chinese{section}章,
        },
        subsection = {
            number = \arabic{subsection},
        },
        subsubsection = {
            number = \arabic{subsection}-\arabic{subsubsection},
        }
    }
    :param c:
    :return:
    '''
    c = get_config(c)
    return [
        _build_section_titleformat(c,False),
        _build_subsection_titleformat(c,False),
        _build_subsubsection_titleformat(c,False),
    ]

def _build_title_font(c = None):
    c = get_config(c)
    return [
        rf"section/format = {c.section_font_size}\bfseries",
        rf"subsection/format = {c.subsection_font_size}\bfseries",
        rf"subsubsection/format = {c.subsubsection_font_size}\bfseries",
    ]

def _build_section_titleformat(c = None,fortitle = True):
    c = get_config(c)
    secf = c.section_format
    if c.section_mask[0] is not None:
        secf = secf.replace("{section}", f"{c.section_mask[0]}{{section}}")
    if c.section_mask[1] is not None:
        secf = secf.replace("{subsection}", f"{c.section_mask[1]}{{subsection}}")
    if c.section_mask[2] is not None:
        secf = secf.replace("{subsubsection}", f"{c.section_mask[2]}{{subsubsection}}")

    if fortitle:
        sect = r"\titleformat{\section}[block]" \
               r"{{section_font}\bfseries}" \
               r"{{section_format}}{1em}{}[]" \
            .replace("{section_font}", c.section_font_size) \
            .replace("{section_format}", secf)
        return NoEscape(sect)
    else: # for toc
        sect = f"section/number = {secf}"
        return NoEscape(sect) #作为ctexset的一个项出现 "section/number = 第\chinese{section}章,"

def _build_subsection_titleformat(c = None,fortitle = True):
    c = get_config(c)
    secf = c.subsection_format
    if c.subsection_mask[0] is not None:
        secf = secf.replace("{section}", f"{c.subsection_mask[0]}{{section}}")
    if c.subsection_mask[1] is not None:
        secf = secf.replace("{subsection}", f"{c.subsection_mask[1]}{{subsection}}")
    if c.subsection_mask[2] is not None:
        secf = secf.replace("{subsubsection}", f"{c.subsection_mask[2]}{{subsubsection}}")

    if fortitle:
        sect = r"\titleformat{\subsection}[block]" \
               r"{{subsection_font}\bfseries}" \
               r"{{subsection_format}}{1em}{}[]" \
            .replace("{subsection_font}", c.subsection_font_size) \
            .replace("{subsection_format}", secf)
        return NoEscape(sect)
    else:
        sect = f"subsection/number = {secf}"
        return NoEscape(sect)

def _build_subsubsection_titleformat(c = None,fortitle = True):
    c = get_config(c)
    secf = c.subsubsection_format
    if c.subsubsection_mask[0] is not None:
        secf = secf.replace("{section}", f"{c.subsubsection_mask[0]}{{section}}")
    if c.subsubsection_mask[1] is not None:
        secf = secf.replace("{subsection}", f"{c.subsubsection_mask[1]}{{subsection}}")
    if c.subsubsection_mask[2] is not None:
        secf = secf.replace("{subsubsection}", f"{c.subsubsection_mask[2]}{{subsubsection}}")
    if fortitle:
        sect = r"\titleformat{\subsubsection}[block]" \
               r"{{subsubsection_font}\bfseries}" \
               r"{{subsubsection_format}}{1em}{}[]" \
            .replace("{subsubsection_font}", c.subsubsection_font_size) \
            .replace("{subsubsection_format}", secf)
        return NoEscape(sect)
    else:
        sect = f"subsubsection/number = {secf}"
        return NoEscape(sect)
