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
参考[example.md](./marktex/example/example.md)
其pdf输出效果可以参考
[example.pdf](./output/example.pdf)

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