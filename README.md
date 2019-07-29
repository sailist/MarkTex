# MarkTex
MarkTex是将Markdown内容转换为Latex文档的Python库。

## 使用方式
```bash
% 因为pip源刚上传，所以用国内源可能会找不到
pip install marktex -i https://pypi.python.org/pypi
```

```python
from marktex.texrender import MarkTex

doc = MarkTex.convert_from_file("path/of/markdownfile","path/of/output_image/dir")
doc.generate_tex()
```

目录`outoput/`下的例子可以通过以下代码生成
```python
from marktex.example import run_example
run_example("./output/")
```

## 特性介绍
具体可以参考[example.md](./marktex/example/example.md)
其pdf输出效果可以参考
[example.pdf](./output/example.pdf)

### 目录
```bash
 [toc]
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111128148.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
### 特性介绍
```bash
# 特性
- 支持目前主流的所有markdown语法（目前，脚注和xml标签暂时不支持）
- 额外添加了下划线语法（`__下划线__`）
- 表格自动调整列宽
- 复选框支持三种
- 无论是本地图片还是网络图片，都能够支持
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111240926.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
### 文字效果与五级标题
```bash
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
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111253193.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
### 表格
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
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111347680.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111401625.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
### 列表、序号、复选框
```bash
## 列表和序号/itemize&enumerate
- 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)

1. 支持**加粗**，*斜体*，`行内代码`,$Inline Formula$，[超链接](www.github.com)

 [x] 支持
 [√] 三种
 [] 复选框格式
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111436171.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
### 图片
图片支持网络图片和本地图片，会被统一的哈希命名后存放到自定义的图片目录下
```bash
## 图片
和表格一样，取消了浮动，因此暂时不支持对图片的描述。不过本项目支持网络图片，会在转换的时候自动下载到本地。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111446599.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
### 公式
```bash

## 公式
公式不支持中文，并且没有编号
$$
f(x_i)=ax_i+b
$$
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111522892.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)

### 代码
```bash
## 代码
代码使用Listings，按[wiki-Listings](https://en.wikibooks.org/wiki/LaTeX/Source_Code_Listings)的说法，主流的各种语言都支持。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019072617073535.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
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

### 引用
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
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111650548.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111702763.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)![在这里插入图片描述](https://img-blog.csdnimg.cn/20190729111713133.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)

## TODOs
 [x] 删除线和下划线的添加
 [x] 复选框的识别
 [x] 表格的美化
 [x] 目录
 [] 封面
 [] 水印
 [] 正式支持四级和五级标题
 [] 图片相对路径的优化
 [] 代码环境美化
 [] 可定制化