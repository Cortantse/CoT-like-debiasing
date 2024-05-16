# 文件结构说明

本文件夹包含以下子文件夹和代码文件：

## 文件夹

- `anaylsis`：放分析图片和报告
- `deprecated`: 之前的实验数据，暂时用处不大
- `figure`: 保存一些画图的脚本
- `promot_design`: 放prompt内容
- `BBQ_original_data_and_code`：放BBQ原始问题，以及调用api的方法，以及部分模板，模板之后
会单独整理出来，以及实验数据都在里面
### `BBQ_original_data_and_code`文件夹内的文件
- `BBQ_jsons`: BBQ测试集json文件，以及固定的0.1倍采样率的随机问题集
- `deprecated_code`: 旧的代码
- `deprecated_data`: 旧的测试数据
- `log`: 实验日志，包括每一次实验的两个文件，json用于存取一些实验关键信息，pkl是二进制序列化文件，可以用reload_pkl_and_test.py打开，方便对之前的测试数据进行回看，查看是如何回答问题的
#### 代码文件

- `config`: 基础参数
- `dependency`: 一些辅助函数
- `Multi_Agent`: 主要py文件，用于跑benchmark
- `prompts`: 里面整理了Multi-Agent使用的Prompt
- `reload_pkl_and_test`: 里面可以实现对源程序 agent 回答问题的数组进行序列化，重新读取，进行逐条分析，顺带计数了不同错误类型的数量（这里可以修改筛选的参数，以展示不同错误的对象）