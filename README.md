# 文件结构说明

本文件夹包含以下子文件夹和代码文件：

## 文件夹

- `Failure_data`：用来记录不同方法在BBQ测试下错误的情况。
- `raw_data`：用于记录不同方法在BBQ测试下的所有结果。
- `anaylsis`：放分析图片和报告
- `BBQ_original_data_and_code`：放BBQ原始问题，以及调用api的方法，以及部分模板，模板之后会单独整理出来，以及代码部分目前的并发api、异步api做得不好，还有点bug QaQ

## 重要参数
- 发现sample = 0.1 就已经达到了比较好的程度，可以大概模拟出prompt的效果

## 代码文件

### `main.py`

- 功能：并发地发送请求给OpenAI API。

### `API.py`

- 功能：定义了一些API交互和接口交互的函数。

### `Util.py`

- 功能：定义一些辅助函数。
