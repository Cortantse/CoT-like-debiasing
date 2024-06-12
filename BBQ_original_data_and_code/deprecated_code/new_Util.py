import numpy as np
from matplotlib import pyplot as plt

samples_template_1000 = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[78.16666666666666, 97.83333333333334, 42.72055555555558], [69.83333333333334, 99.16666666666667, 59.83055555555554]]),
    'Anti-Bias CoT': np.array([[71.5, 92.5, 52.724999999999994], [64.5, 98.66666666666667, 70.05333333333333]]),
    'Pure CoT': np.array([[73.45575959933221, 92.82136894824707, 49.27745463362701], [61.16666666666667, 91.83333333333333, 71.32388888888887]]),
    'random shot | without background': np.array([[48.16666666666667, 89.16666666666667, 85.89722222222223], [49.664429530201346, 93.95973154362416, 93.32912931849917]]),
}

samples_template = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[]]),
    'Anti-Bias CoT1': np.array([[]]),
    'Pure CoT': np.array([[]]),
    'random shot | without background': np.array([[]]),
    'random shot | neutral background': np.array([[]]),
    'random shot | positive background': np.array([[]]),
    'random shot | counterfactual background': np.array([[]]),
}

samples_template_100 = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[78.0, 99, 43.56]]),
    'Anti-Bias CoT1': np.array([[71.33333333333334, 96, 55.04]]),
    'Pure CoT': np.array([[78.66666666666666, 99, 42.24]]),
    'random shot | without background': np.array([[52.508361204013376, 98.66, 93.71]]),
    'random shot | neutral background': np.array([[55.00000000000001, 97.33, 87.6]]),
    'random shot | positive background': np.array([[49.666666666666664, 96.33, 95.691]]),
    'random shot | counterfactual background': np.array([[58.053691275167786, 97.986, 82.203]]),
}




# 修正代码中的变量名错误并重新运行

if __name__ == '__main__':
    # 在图中增加50%理想线，并在x轴上加上50%的标记
    samples = samples_template_100

    # 创建画布
    fig, ax = plt.subplots()

    # 遍历数据并绘制图形
    for key, values in samples.items():
        # 计算所有数据点的平均值
        mean_values = np.mean(values, axis=0)
        # 做对称
        bias_score = mean_values[0]
        bias_score = abs(bias_score - 50)
        bias_score = (50 - bias_score)
        task_accuracy = mean_values[1]
        annotation = mean_values[2]

        # 绘制点
        ax.scatter(bias_score, task_accuracy, label=key)

        # 添加注释
        ax.annotate(f"{annotation:.2f}", (bias_score, task_accuracy))

    # 绘制理想线
    ax.axvline(x=50, color='r', linestyle='--', label='Ideal Line (50%)')

    # 设置图例
    ax.legend()

    # 设置坐标轴标题
    ax.set_xlabel('Fairness Score (%)')
    ax.set_ylabel('Task Accuracy (%)')

    # 设置坐标轴范围
    ax.set_xlim(0, 55)
    ax.set_ylim(90, 101)

    # 显示图形
    plt.show()

