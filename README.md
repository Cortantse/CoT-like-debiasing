# 文件结构说明

本文件夹包含以下子文件夹和代码文件：

## 文件夹

- `failure_data`：用来记录不同方法在BBQ测试下错误的情况。
- `outputs_jsonl`：存放由`main.py`并发生成的原始数据。
- `raw_data`：用于记录不同方法在BBQ测试下的所有结果。

## 代码文件

### `main.py`

- 功能：并发地发送请求给OpenAI API。

### `API.py`

- 功能：定义了一些API交互和接口交互的函数。

### `Util.py`

- 功能：定义一些辅助函数。
