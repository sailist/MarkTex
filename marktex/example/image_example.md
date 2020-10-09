
# 图片
支持网络图片，会在转换的时候自动下载到本地，同时对非 `JPG/PNG` 格式的图片，会将其转换为 `PNG` 格式。所有的图片会被 hash 后放置在 `cacheimg_dir` 下，默认该目录为 `<output_dir>/imgs`

## 行内图片

最新版本添加了行内图片，如果没有换行，那么该图片会被人为是行内图片，会自动调整高度适应一行：![在这里插入图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)

测试2：![](https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1572416129&di=c3174b1e8126d0aa7ffac4182118a743&src=http://b-ssl.duitang.com/uploads/item/201803/03/20180303113221_4YHwS.thumb.700_0.jpeg)图片之后

## 行间图片

![可以添加图片描述](https://img-blog.csdnimg.cn/20190726170401866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhaWxpc3Q=,size_16,color_FFFFFF,t_70)

相对路径：
![](./exampleimage.png)
