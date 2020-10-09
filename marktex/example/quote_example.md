
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


