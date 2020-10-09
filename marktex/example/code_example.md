
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