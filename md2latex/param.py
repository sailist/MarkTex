from pylatex import Package,NoEscape
packages = [Package("xcolor"),
            Package("lastpage"),
            Package("framed"),
            Package("color"),
            Package("showframe","noframe"),
            ]


preambles = [NoEscape(r"\definecolor{shadecolor}{gray}{0.9}"),#> 用于这个>
             NoEscape(r"\definecolor{aliceblue}{rgb}{0.94, 0.97, 1.0}"),# 用于 ` `
             NoEscape(r'''\renewenvironment{shaded}{%
                     \def\FrameCommand{\fboxsep=\FrameSep \colorbox{shadecolor}}%
                     \MakeFramed{\advance\hsize-\width \FrameRestore\FrameRestore}}%
                    {\endMakeFramed}
                '''),
             ]