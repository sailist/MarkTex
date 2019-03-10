# -*- coding: UTF-8 -*-
import os

exampleimagepath = os.path.split(os.path.realpath(__file__))[0] + "/" + "exampleimage.png"


title = r'''

@[TOC]
# first title 大标题
## second title 二标题
### third title 三标题
#### forth title 四标题
##### fifth title 五标题



'''

table = r'''
|||||
|-|-|-|-|
|表格|**加粗**|`行内代码`|$inline fomular$|

'''

item = r'''
1. enum型 **item**
2. enum型 `item`
3. enum型 *item*
4. enum型 item

- item型 **item**
- item型 `item`
- item型 item

> 引用
> **引用**
> `引用`
'''


code = r'''
```c++
#include<stdio>
int main(){
    return 0;
}

```
'''


image = r'''
![示例本地图片 local image]({})
![示例网络图片 web image](https://img-blog.csdnimg.cn/20181031181035831.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)

'''.format(exampleimagepath)


href = r'''
[示例链接](https://github.com/sailist/md2latex)
'''


'''
暂不支持引用中混入标题，引用中混入表格等
'''
fixed = r'''

> 1. enum型
> 2. enum型
>> - item 型
>> - item 型
> [示例链接](https://github.com/sailist/md2latex)

>![示例本地图片 local image]({})
>![示例网络图片 web image](https://img-blog.csdnimg.cn/20181031181035831.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)



'''.format(exampleimagepath)



full = title + table + item + code + image + fixed

