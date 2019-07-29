# MarkTex
MarkTex是将Markdown内容转换为Latex文档的Python库。

## 项目结构
本项目将Markdown分为环境（Environment），行（Line），词（Token）

环境有段落（Paragraph）、引用（Quote）、列表（Itemize）、序号（Enumerate）、公式（Formula）、代码（Code）、表格（Table）

行有标题（Section）、图片（Image）、普通文本（TokenLine）、纯文本（RawLine）、空行（NewLine）

词有普通（Token）、粗体（Bold）、斜体（Italic）、行内公式（InFormula）、行内代码（InCode）、超链接（Hyperlink）、脚注（Footnote）、行内图片（InImage）

文档由环境组成，每个环境由多个"行"组成，每个“行”按不同的类别，嵌套其他的“行”或者“词”。


## TODOs
 [x] 删除线和下划线的添加
 [x] 复选框的识别
 [x] 表格的美化
 [x] 目录
 [] 封面
 [] 水印
 [] 正式支持四级和五级标题