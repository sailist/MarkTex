[TOC]

<title>MarkTex特性说明</title>
<author>sailist</author>


本文用于演示和测试转换后的效果
# 基本特性<sub>下标在这里</sub>

- 支持目前主流的所有markdown语法，包括脚注、xml
- 额外添加了下划线语法（`__下划线__`）
- 表格自动调整列宽
- 复选框支持三种
- 无论是本地图片还是网络图片，都能够支持。


# 各类文本和标题级别
支持一般的文本和**加粗**，*斜体*，`行内代码`，和$InLine Formula$，[超链接](http://github.com/sailist/MarkTex2)。

同时，支持多级嵌套，包括***粗斜体***，**__粗体+下划线__**，*__斜体+下划线__*等等，***__粗斜体+下划线__***

~~删除线~~,__下划线__

## 二级标题

### 三级标题
目录编号支持到三级标题，可以通过修改latex文件或者直接更改模板来完成。

#### 四级标题
##### 五级标题

# 脚注

可以支持脚注格式[^label]

[^label]:这里是脚注的内容，新版支持在脚注中的部份字体，包括 **加粗**，*斜体*等


# 表格
支持一般的文本格式，暂时不支持表格内图片。另外，表格取消了浮动（float），因此不支持对表格的描述（caption），不过在Markdown中也没有对表格的描述，因此也不算功能不完善。

|ColA| ColB |
|--|--|
| **Table Bold** |  *Table Italic*|
| `Table Code` |  $Table Formula$|
|[Table line](www.github.com/sailist/MarkTex2)|Table Text|

|A|B|C|Long Text Sample Long Text Sample Long Text Sample Long Text Sample Long Text Sample Long Text Sample |
|--|--|--|--|
|A|B|C|D|
|A|B|C|D|
|A|B|C|D|

# 列表和序号/itemize&enumerate

支持无序号列表，序号列表，复选框

- 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)
- 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)
- 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)

1. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)
2. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)
3. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)

 - [x] 支持
 - [√] 三种
 - [ ] 复选框格式
 - [] 复选框格式

# 图片
支持网络图片，会在转换的时候自动下载到本地，同时对非 JPG/PNG 格式的图片，会将其转换为PNG格式。所有的图片会被hash 后放置在 cacheimg_dir 下，默认该目录为 <output_dir>/imgs

## 行内图片

最新版本添加了行内图片，如果没有换行，那么该图片会被人为是行内图片，会自动调整高度适应一行：![在这里插入图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)

测试2：![](https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1572416129&di=c3174b1e8126d0aa7ffac4182118a743&src=http://b-ssl.duitang.com/uploads/item/201803/03/20180303113221_4YHwS.thumb.700_0.jpeg)图片之后

## 行间图片

![可以添加图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)

相对路径：
![](./exampleimage.png)

# 公式
公式支持中文，但没有编号，如果要编号可以通过手动添加tag的方式

## 行内公式
$f(x) = x_{1} 中文$ 

## 行间公式
$$
使用函数 f(x_i)=ax_i+b \tag{1} 
$$



## 符号支持
符号集在内部做了一个映射，可以将任意公式内外的符号均映射成为 LaTeX 中的符号。

原本的解决方案为添加一个额外的符号字体集来解决（来自于[stackoverflow](https://tex.stackexchange.com/questions/69901/how-to-typeset-greek-letters)），目前的方案为两者优先采用映射方法，目前支持的符号列举如下（可能支持更多符号，但没有经过测试）：

### 希腊字母
αβγδεζηθικλμνξοπρστυφχψω

ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ

$αβγδεζηθικλμνξοπρστυφχψω$

$$αβγδεζηθικλμνξοπρστυφχψω$$
### 运算符号
±×÷∣∤

⋅∘∗⊙⊕

≤≥≠≈≡

∑∏∐∈∉⊂⊃⊆⊇⊄

∧∨∩∪∃∀∇

⊥∠

∞∘′

∫∬∭

↑↓←→↔↕

# 代码
代码使用tcolorbox和minted，基本支持所有主流语言。支持的所有语言请参考 [Code Highlighting with minted](https://www.overleaf.com/learn/latex/Code_Highlighting_with_minted) ，因此在添加代码环境的时候请注意标注在```后的代码语言和minted支持的相同，其中一部分minted和markdown中标识不相同的语言都做了映射（如markdown中是cpp但minted中是c++，以及javascrip和js），如果仍然存在转换错误，请手动调整语言类型或者提交错误给我由我来更新项目。

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

# 引用
> 引用内环境和普通文本基本一致，但是不支持标题，不支持代码。
> 不支持代码。由于LaTeX中环境嵌套导致过长的代码使得pdf无法换页，因此我取消了在引用中行间代码的支持，在引用中检测到代码环境会从引用环境中跳出跳出。
> 演示**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)
> - 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)
> 1. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com/sailist/MarkTex2)
>> 
>> 新版 MarkTex 终于支持多级嵌套引用了！
>>>>>> $ f(x) = ax+b$
>> 任意级别的嵌套完全没有问题！
>

> 表格：
> |ColA| ColB |
>|--|--|
>| **Table Bold** |  *Table Italic*|
>| `Table Code` |  $Table Formula$|
>|[Table line](www.github.com/sailist/MarkTex2)|Table Text|
> 公式：
> $$F(x_i) = wx_i+b$$
> 图片由于引用环境的问题，不支持浮动窗口，因此无法添加描述，描述会被忽略。
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
> 



# 新特性-include

非常酷的特性！可以使用特殊的html标签来引入其他的 MarkDown 或者 LaTeX 文件！
## 引入 Markdown 文档

<include>./table_example.md</include>

<include>./formula_example.md</include>

## 引入 LaTeX 文档
<include>texfile.tex</include>