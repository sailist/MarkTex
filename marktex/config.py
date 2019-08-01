'''Don't change the basic param'''
'''latex unit'''
mm = "mm"
pt = "pt"
bp = "bp"
dd = "dd"
pc = "pc"
sp = "sp"
cm = "cm"
cc = "cc"
inch = "in"
ex = "ex"
em = "em"

'''Font size'''
tiny = r"\tiny"
scriptsize = r"\scriptsize"
footnotesize = r"\footnotesize"
small = r"\small"
normalsize = r"\normalsize"
large = r"\large"
Large = r"\Large"
LARGE = r"\LARGE"
huge = r"\huge"
Huge = r"\Huge"

# 可选项：±0,±1,±2,±3,±4,±5,±6,7,8,分别对应（小）初、一...六，七号，八号，其中负数为"小"
zihao = lambda x:f"\zihao{{{x}}}"

'''the section index style'''
section_style_dict = {
    "arabic":r"\arabic", #阿拉伯数字
    "roman":r"\roman", #小写罗马数字
    "Roman":r"\Roman", #大写罗马数字
    "alph":r"\alph", #小写字母
    "Alph":r"\alph", #大写字母
    "chinese":r"\chinese", #中文汉字（部分情况可用）
}
sec_arabic = section_style_dict["arabic"]
sec_roman = section_style_dict["roman"]
sec_Roman = section_style_dict["Roman"]
sec_alph = section_style_dict["alph"]
sec_Alph = section_style_dict["Alph"]
sec_chinese = section_style_dict["chinese"]


'''the param below can be changed'''
# define new color
# will create line like "\definecolor{aliceblue}{rgb}{0.94, 0.97, 1.0}"
new_color_dict = dict(
    aliceblue=["rgb",(0.94, 0.97, 1.0)],
    linkblue=["rgb",(0.4, 0.67,0.87)],
    shadecolor=["rgb",(0.93,0.94,0.95)],
    gainsboro=["rgb",(0.86, 0.86, 0.86)],
    bordergray=["gray",(0.87)],
    tabletopgray=["rgb",(0.937,0.952,0.96)],
    tablerowgray=["gray",(0.968)],
    tablelinegray=["gray",(0.827)],
)

'''Paragraph Environment'''
incode_font_size = small
# hyperlink color
hyperlink_color = "linkblue"


'''section setting'''
section_font_size = LARGE # 一级标题的字体
subsection_font_size = zihao(3)
subsubsection_font_size = Large
# paragraph_font_size = large  #TODO
# subparagraph_font_size = large #TODO

section_format = r"第{section}章" # 一级标题的格式
subsection_format = r"{subsection}"
subsubsection_format = r"{subsection}.{subsubsection}"
paragraph_format = r"{subsection}.{subsubsection}"
subparagraph_format = r"{subsection}.{subsubsection}"

# 一级标题的序号格式，为一个列表，注意分别和section/subsection/subsubsection的序号格式对应，为None表示没有
section_mask = (sec_chinese,None,None)
subsection_mask = (None,sec_arabic,None)
subsubsection_mask = (None,sec_arabic,sec_arabic)
paragraph_mask = (None,sec_arabic,sec_arabic)
subparagraph_mask = (None,sec_arabic,sec_arabic)


'''document setting'''
# 设置文档边距
geometry_border = [3.17,3.17,2.54,2.54] # left,right,top,bottom
# 文档边距数字对应的单位
geometry_unit = cm


'''Code Environment'''
# 代码字体大小
code_font_size = small
#左侧是否有序号
has_number_left = True
#序号的字体大小
code_number_size = small


'''tools setting'''
image_download_retry_time = 10
# 在尝试重试次数达到上限后，是否等待手动下载该文件放到目录
# wait_manully_if_all_failed = False
# 在tex文件里添加图片的时候，使用相对路径还是绝对路径
give_rele_path = True