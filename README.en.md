# MarkTex
Parse markdown file to LaTeX-code file. Can be used to convert markdown to PDF if you want.

## Features
- support almost all features that used in markdown: section/code/quote/TOC/table/hyperlink...,
- support inline image, 
- beautify table, automaticly adjust column width,
- support diy your own LaTeX template file,
- support include other markdown and LaTeX file in one file,
- support Chinese,
- support diy your own markdown syntax
- astparser module is decoupled, you can reuse it to your own language

> All supported syntax can be previewed at [example.md](./marktex/example/example.md) and [all_example.pdf](./outputs/out/all_example.pdf)

# How to use
```shell
pip install marktex
```

or install directly from github
```shell
pip install git+https://github.com/sailist/marktex
```

```python
from marktex import api
api.convert('mdpath1','mdpath2',...,output_dir='output_dir')
```

run examples

```python
from marktex.api import run_example
run_example()
```

run by command line tool.

Output in one directory.
```bash
marktex a.md b.md ...
```

Output in the given directory.
```bash
marktex a.md b.md ... -o "path"
```

Output in given directories.
```bash
marktex a.md b.md ... -e "pathfora" "pathforb" ...
```



# Preview
see [example.md](./marktex/example/example.md) and [all_example.pdf](./outputs/out/all_example.pdf) for details.

## TOC
```bash
 [toc]
```
![在这里插入图片描述](./src/toc.png)

## Features
```bash
# 特性<sub>下标在这里</sub>
- 支持目前主流的所有markdown语法（目前，脚注和xml标签暂时不支持）
- 额外添加了下划线语法（`__下划线__`）
- 表格自动调整列宽
- 复选框支持三种
- 无论是本地图片还是网络图片，都能够支持。
```
![在这里插入图片描述](./src/feature.png)

## Text style
```bash
# 效果演示

本文用于演示和测试转换后的效果

## 普通文本
支持一般的文本和**加粗**，*斜体*，`行内代码`，和$InLine Formula$，[超链接](http://github.com)，注意公式暂时不支持中文。

~~删除线~~,__下划线__

## 二级标题

### 三级标题
目录编号支持到三级标题，可以通过修改latex文件或者直接更改模板来完成。

#### 四级标题
##### 五级标题
```

![在这里插入图片描述](./src/effect.png)

## Table
可以完美的自适应表格列宽（测试效果良好，不排除特例），不过暂时不支持表格内插入图片
```bash
## 表格
支持一般的文本格式，暂时不支持表格内图片。另外，表格取消了浮动（float），因此不支持对表格的描述（caption），不过在Markdown中也没有对表格的描述，因此也不算功能不完善。

|ColA| ColB |
|--|--|
| **Table Bold** |  *Table Italic*|
| `Table Code` |  $Table Formula$|
|[Table line](www.github.com)|Table Text|

|A|B|C|Long Text Sample Long Text Sample Long Text Sample Long Text Sample Long Text Sample Long Text Sample |
|--|--|--|--|
|A|B|C|D|
|A|B|C|D|
|A|B|C|D|
```
![在这里插入图片描述](./src/table.png)

## Itemize,Enumrate,MultiBox
```bash
## 列表和序号/itemize&enumerate
- 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)
- 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)
- 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)

1. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)
2. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)
3. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)

 [x] 支持
 [√] 三种
 [] 复选框格式
```
![在这里插入图片描述](./src/list.png)

## Image
图片支持网络图片和本地图片，会被统一的哈希命名后存放到自定义的图片目录下
```bash
## 图片
和表格一样，取消了浮动，因此暂时不支持对图片的描述。不过本项目支持网络图片，会在转换的时候自动下载到本地。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
```

![在这里插入图片描述](./src/img1.png)
![在这里插入图片描述](./src/img2.png)

## Formula

公式支持中文，但没有编号，如果要编号可以通过手动添加tag的方式

### Inline Formula
$f(x) = x_{1} 中文$ 

### Line Formula
$$
使用函数 f(x_i)=ax_i+b \tag{1} 
$$



### Sign Support
符号集在内部做了一个映射，可以将任意公式内外的符号均映射成为 LaTeX 中的符号。

原本的解决方案为添加一个额外的符号字体集来解决（来自于[stackoverflow](https://tex.stackexchange.com/questions/69901/how-to-typeset-greek-letters) ），目前的方案为两者优先采用映射方法，目前支持的符号列举如下（可能支持更多符号，但没有经过测试）：

#### Greece
αβγδεζηθικλμνξοπρστυφχψω

ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ


**αβγδεζηθικλμνξοπρστυφχψω**

`αβγδεζηθικλμνξοπρστυφχψω`

$αβγδεζηθικλμνξοπρστυφχψω$

$$αβγδεζηθικλμνξοπρστυφχψω$$

```
ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ
```

#### Operator
±×÷∣∤

⋅∘∗⊙⊕

≤≥≠≈≡

∑∏∐∈∉⊂⊃⊆⊇⊄

∧∨∩∪∃∀∇

⊥∠

∞∘′

∫∬∭

↑↓←→↔↕

![在这里插入图片描述](./src/fomular.png)
![在这里插入图片描述](./src/sign.png)


## Code

```bash
代码使用tcolorbox和minted，基本支持所有主流语言。支持的所有语言请参考 [Code Highlighting with minted](https://www.overleaf.com/learn/latex/Code_Highlighting_with_minted) 
```
```python
if __name__ == "__main__":
	print("hello world!")
```
```cpp
#include<stdio.h>
int main(){
	printf("hello world")
	return 0;
}
```

![](./src/code.png)

## Quote
```bash
## 引用
> 引用内环境和普通文本基本一致，但是不支持标题。
> 演示**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)
> - 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)
> 1. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)

> 表格：
> |ColA| ColB |
>|--|--|
>| **Table Bold** |  *Table Italic*|
>| `Table Code` |  $Table Formula$|
>|[Table line](www.github.com)|Table Text|
> 公式：
> $$F(x_i) = wx_i+b$$
> 图片：
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
> 
```
![在这里插入图片描述](./src/quote.png)

![在这里插入图片描述](./src/quote2.png)

## Include
```bash
# 新特性-引入其他Markdown文档

非常酷的特性！可以使用特殊的html标签来引入其他的MarkDown！

<include>./table_example.md</include>

<include>./formula_example.md</include>

```

![](./src/newf.png)

![](./src/newf2.png)


# TODOs
 - [ ] 多级嵌套存在优先级限制，仍然待解决
 - [ ] 列表的缩进支持
 - [ ] 表格列宽度比例的计算方式改进
 - [ ] 添加其他类型的 parser ？