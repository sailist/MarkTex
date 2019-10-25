[TOC]

<title>MarkTex特性说明</title>
<author>sailist</author>

[maketitle]

# 特性<sub>下标在这里</sub>
- 支持目前主流的所有markdown语法（目前，脚注和xml标签暂时不支持）
- 额外添加了下划线语法（`__下划线__`）
- 表格自动调整列宽
- 复选框支持三种
- 无论是本地图片还是网络图片，都能够支持。

# 效果演示

本文用于演示和测试转换后的效果

## 普通文本
支持一般的文本和**加粗**，*斜体*，`行内代码`，和$InLine Formula$，[超链接](http://github.com)，注意公式暂时不支持中文。

~~删除线~~,__下划线__

## 二级标题

### 三级标题
目录最多支持到三级标题
#### 四级标题
##### 五级标题

## 脚注

可以支持脚注格式[^label]

[^label]:这里是脚注的内容


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

## 图片
和表格一样，取消了浮动，因此暂时不支持对图片的描述。不过本项目支持网络图片，会在转换的时候自动下载到本地，同时如果是非JPG或者PNG格式的图片，会转换为PNG格式。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)

相对路径：
![](./exampleimage.png)

## 公式
公式不支持中文，并且没有编号
$$
f(x_i)=ax_i+b
$$

## 代码
代码使用tcolorbox和minted，基本支持所有主流语言。支持的所有语言请参考 [Code Highlighting with minted](https://www.overleaf.com/learn/latex/Code_Highlighting_with_minted) 


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

# 新特性-引入其他Markdown文档

非常酷的特性！可以使用特殊的html标签来引入其他的MarkDown！

<include>./table_example.md</include>

<include>./formula_example.md</include>
