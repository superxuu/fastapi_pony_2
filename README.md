# fastapi_pony_2

**Fastapi + pony 实践二**：使用自定义中间件，在每次请求之前，将db_session加载到全局的Request中，请求之后释放db_session。

需注意:

1. 在src/models中，每次增加一个库表模块，都需要在models的\__ini__t.py中import下。
2. 自定义中间件需要在utils/\__init__.py中import下

Fastapi + pony 另一种实现方法参见：**[Fastapi + pony 实践一](https://github.com/superxuu/fastapi_pony)**

