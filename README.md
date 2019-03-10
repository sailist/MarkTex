# md2latex
- mdConverter now can convert text with markdown format to latex code, support quote ">",item "-" ,enum "1.",Table |||, splitline --- ,and mixing scene.
- use ctexart documentclass,support chinese language
- imageurl can both from local and web, mdConverter will download and rename(with abspath) and reformat it.

What is lacking now is not beautiful enough. In the next version,I will add more function and beautify it.

## dependency
```
pylatex
matplotlib
urllib
```

## how2use
```python 
from mdconverter.example import fullExample
from mdconverter import excu

doc = excu(fullExample.full)# type:str
print(doc)
```

## example
Full example is given in the file ./example/fullExample.py

```markdown
@[TOC]
# first title 大标题
## second title 二标题
### third title 三标题
#### forth title 四标题
##### fifth title 五标题

```

toLatex:
![标题示例](/title.png)


```markdown
|||||
|-|-|-|-|
|in table |**bold 加粗**|`行内代码 inline code`|$inline fomular$|

```

> fomular is not support now.

toLatex:
![表格示例](/table.png)

```markdown
1. enum型 **item**
2. enum型 `item`
3. enum型 *item*
4. enum型 item

- item型 **item**
- item型 `item`
- item型 item

```

toLatex:
![标题示例](/item.png)

```markdown
```c++
#include<stdio>
int main(){
    return 0;
}

```
> code language is only support c++ style,and is ugly.


toLatex:
![代码示例](/code.png)

```markdown
![示例本地图片 local image example]({})
![示例网络图片 web image example](https://img-blog.csdnimg.cn/20181031181035831.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
```


toLatex:
![图片示例](/image.png)


```markdown
> 1. enum型
> 2. enum型
>> - item 型
>> - item 型
> [示例链接](https://github.com/sailist/md2latex)

>![示例本地图片 local image]({})
>![示例网络图片 web image](https://img-blog.csdnimg.cn/20181031181035831.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)
```


toLatex:
![图片示例](/mix.png)
![图片示例](/mix2.png)



