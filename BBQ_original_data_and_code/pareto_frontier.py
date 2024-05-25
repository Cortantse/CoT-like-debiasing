import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors


def is_pareto_efficient(costs):
    """
    Find the Pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :return: A boolean array of Pareto-efficient points
    """
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1)  # Keep any point with a lower cost
            is_efficient[i] = True  # And keep self
    return is_efficient


sample_d = {
    'Baseline': np.array([
        [0.066, 0.928],
        [0.07999999999999999, 0.94],
        [0.09200000000000003, 0.944],
        [0.09600000000000003, 0.912],
        [0.09200000000000003, 0.936],
        [0.10799999999999996, 0.924], #6
        [0.0943775100401606, 0.942], #7
        [0.09199999999999998, 0.938], #8
        [0.07200000000000004, 0.928], #9
    ]),
    'Anti-Bias CoT': np.array([
        [0.014000000000000014, 0.88],
        [0.014028056112224465, 0.874],
        [0.018000000000000016, 0.894],
        [0.026000000000000023, 0.884],
        [0.022000000000000023, 0.862]
    ]),
    'Pro-Bias CoT': np.array([
        [0.047999999999999994, 0.822],
        [0.07399999999999997, 0.834],
        [0.05399999999999998, 0.8316633266533067],
        [0.05799999999999996, 0.792],
        [0.023999999999999987, 0.778]
    ]),
    'Pure CoT': np.array([
        [0.06600000000000002, 0.934],
        [0.076, 0.92],
        [0.07999999999999997, 0.916],
        [0.09599999999999999, 0.938],
        [0.08599999999999997, 0.9218436873747495],
        [0.09400000000000003, 0.9378757515030061],
        [0.04400000000000001, 0.908],
        [0.05410821643286575, 0.9175050301810865],
        [0.13200000000000003, 0.93],
        [0.054000000000000006, 0.932],
        [0.08599999999999997, 0.946],
        [0.038, 0.922],
        [0.086, 0.926],
    ]),
    '2agents3round Debate': np.array([
        [0.062000000000000055, 0.946]
    ]),
    'Masking without Background': np.array([
        [0.020202020202020145, 0.9553752535496958]
    ]),
}

sample_qwen = {
    'Baseline': np.array([
        [0.04599999999999998, 0.718],
        [0.043999999999999984, 0.717434869739479],
        [0.050000000000000044, 0.686],
        [0.045999999999999985, 0.696],
        [0.03199999999999998, 0.704],
        [0.04599999999999998, 0.696],
        [0.04999999999999998, 0.71],
    ])
}

samples  = {
    'Baseline': np.array([
        [0.128, 0.892],
        [0.12800000000000003, 0.868],
        [0.11600000000000002, 0.852],
        [0.10000000000000002, 0.872],
        [0.07800000000000003, 0.876],
        [0.14400000000000002, 0.902],
        [0.12199999999999997, 0.854],
        [0.122, 0.858],
        [0.084, 0.87],
        [0.06600000000000003, 0.852]
    ]),
    'Anti-Bias CoT': np.array([
        [0.01004016064257029, 0.558],
        [0.02610441767068272, 0.55],
        [0.026104417670682712, 0.556],
        [0.10199999999999997, 0.6],
        [0.01807228915662652, 0.594],
        [-0.006000000000000009, 0.546],
        [-0.0060000000000000045, 0.562],
        [0.0, 0.578],
        [0.0020120724346076495, 0.586],
    ]),
    'Pro-Bias CoT': np.array([
        [0.11800000000000008, 0.556],
        [0.17999999999999997, 0.594],
        [0.09999999999999998, 0.596],
        [0.07399999999999995, 0.552],
        [0.14200000000000004, 0.578],
        [0.07399999999999994, 0.574],
        [0.11422845691382763, 0.591182364729459],
    ]),
    'Pure CoT': np.array([
        [0.074, 0.7935871743486974],
        [0.07615230460921844, 0.766],
        [0.08433734939759037, 0.758],
        [0.102, 0.752],
        [0.05000000000000003, 0.788],
        [0.078, 0.756],
        [0.033999999999999975, 0.77],
    ]),
    # # 'Instruction Following CoT': np.array([
    # #     [0.03999999999999999, 0.774],
    # #     [0.01999999999999999, 0.781563126252505],
    # #     [0.05600000000000001, 0.738],
    # #     [0.04200000000000001, 0.78],
    # #     [0.018072289156626502, 0.75],
    # #     [0.05999999999999999, 0.742],
    # #     [0.08416833667334671, 0.728],
    # # ]),
    # # 'Instruction Following CoT 2': np.array([
    # #     [0.09800000000000005, 0.802],
    # #     [0.05400000000000003, 0.806],
    # #     [0.07999999999999999, 0.786]
    # # ]),
    'Society of Mind': np.array([
        [0.062000000000000006, 0.858],
        [0.06425702811244983, 0.91]
    ]),
    'Advice': np.array([
        [0.0, 0.7424547283702213],
        [0.05112474437627815, 0.7303822937625755],
        [0.050709939148073015, 0.744466800804829],
        [0.040567951318458445, 0.7439516129032258],
        # more advice
        [-0.00814663951120163, 0.7139959432048681],
        [0.020242914979757103, 0.7449392712550608],
        # analysis on QA
        [0.004073319755600819, 0.7313131313131314],
        [0.006024096385542164, 0.74],
        [0.04887983706720981, 0.7208835341365462],
        [0.012219959266802456, 0.71],
        [0.028455284552845513, 0.762],
        [0.036144578313253004, 0.7108433734939759],
        [0.060606060606060615, 0.7454909819639278]
    ]),
    'Mask without background': np.array([
        [-0.006521739130434794, 0.8819875776397516],
        [-0.01583710407239818, 0.9112050739957717]
    ]),
    'Mask without rule': np.array([
        [0.012219959266802425, 0.8383838383838383],
        [0.042682926829268275, 0.8837675350701403]
    ]),
    'Mask with XY': np.array([
        [0.03532008830022077, 0.9023354564755839],
    ]),
    'Mask with XY gpt-3.5 main model, deep-seek mask model': np.array([
        [0.01008064516129032, 0.9336016096579477],
    ]),
    # 'Advice with Stereo': np.array([
    #     [0.015217391304347816, 0.6438923395445134],
    #     [0.044806517311608965, 0.658],
    # ]),
    # 'Ours with more advice': np.array([
    #     [-0.00814663951120163, 0.7139959432048681],
    #     [0.020242914979757103, 0.7449392712550608],
    # ]),
    # 'Ours with analysis on QA': np.array([
    #     [0.004073319755600819, 0.7313131313131314],
    #     [0.006024096385542164, 0.74],
    #     [0.04887983706720981, 0.7208835341365462],
    #     [0.012219959266802456, 0.71],
    #     [0.028455284552845513, 0.762],
    #     [0.036144578313253004, 0.7108433734939759],
    #     [0.060606060606060615, 0.7454909819639278]
    # ]),
    # 'gpt-4o Baseline': np.array([
    #     [0.03799999999999998, 0.82],
    #     [0.04600000000000004, 0.85],
    #     [0.03599999999999997, 0.828]
    # ]),
    # 'Deep Seek Baseline': np.array(sample_d['Baseline']),
    # 'Qianwen Baseline': np.array(sample_qwen['Baseline']),
}



import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    samples = sample_d


    if_only_need_central_point = False

    if if_only_need_central_point:
        for item in samples:
            average_x, average_y = np.mean(samples[item][:, 0]), np.mean(samples[item][:, 1])
            samples[item] = np.array([[average_x, average_y]])


    # Convert bias_score to a scale that is closer to 1 is better
    for key, value in samples.items():
        # Modify the bias_score to be 1 - |bias_score|
        value[:, 0] = 1 - np.abs(value[:, 0])


    # Implementing the Pareto frontier function
    def is_pareto_efficient(costs):
        """
        Find the Pareto-efficient points
        :param costs: An (n_points, n_costs) array
        :return: A boolean array of Pareto-efficient points
        """
        is_efficient = np.ones(costs.shape[0], dtype=bool)
        for i, c in enumerate(costs):
            if is_efficient[i]:
                # All points that are worse on all costs
                is_efficient[is_efficient] = np.any(costs[is_efficient] >= c, axis=1)
                is_efficient[i] = True  # And keep self in
        return is_efficient


    # Finding and printing Pareto frontiers for each method
    pareto_frontiers = {}
    for key, value in samples.items():
        pareto_mask = is_pareto_efficient(value)
        pareto_frontiers[key] = value[pareto_mask]

    colors = ['blue', 'green', 'red', 'brown', 'orange', 'lime', 'pink', 'cyan', 'magenta', 'gray', 'lime']
    methods = list(samples.keys())


    # 实现计算密度的函数
    def calculate_density(X, n_neighbors=5):
        nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(X)
        distances, indices = nbrs.kneighbors(X)
        density = 1 / distances.mean(axis=1)  # 计算平均距离的倒数作为密度
        scaled_density = (density / density.max()) * 100  # 归一化并缩放到100作为最大大小
        return scaled_density


    # 将所有样本合并，用于计算密度
    all_samples = np.vstack(list(samples.values()))
    density = calculate_density(all_samples)

    # Replot the same scatter plot with density-based size adjustments and global Pareto points connected
    fig, ax = plt.subplots(figsize=(14, 10))

    start_idx = 0
    for idx, key in enumerate(samples):
        num_points = samples[key].shape[0]
        # Adjust point sizes based on density
        sizes = density[start_idx:start_idx + num_points]
        start_idx += num_points

        # Regular points with adjusted sizes
        ax.scatter(samples[key][:, 0], samples[key][:, 1], s=sizes+50, color=colors[idx], label=key)

        # Pareto frontier points
        pareto_mask = is_pareto_efficient(samples[key])


        # Connecting lines for the same method
        sorted_indices = np.argsort(samples[key][:, 1])
        ax.plot(samples[key][sorted_indices, 0], samples[key][sorted_indices, 1], color=colors[idx], linestyle='--')

    # Add global Pareto points with connection
    global_pareto_mask = is_pareto_efficient(all_samples)
    global_pareto_points = all_samples[global_pareto_mask]
    sorted_global_indices = np.argsort(global_pareto_points[:, 1])
    ax.plot(global_pareto_points[sorted_global_indices, 0], global_pareto_points[sorted_global_indices, 1],
            color='black', linestyle=':', linewidth=1.8, label='Global Pareto Frontier')

    # Enhance the plot
    ax.set_title('Pareto Frontiers for Various Methods with Global Frontier and Density-Adjusted Sizes')
    ax.set_xlabel('Bias Score (1 - |Ambig Bias Score|)')
    ax.set_ylabel('Accuracy (Disambiguous QA)')

    # Set the tick intervals for both axes
    x_ticks = np.arange(0.825, 1.01, 0.025)
    y_ticks = np.arange(0.5, 1.0, 0.05)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # Set the aspect ratio (compress y values and expand x values)
    ax.set_aspect(0.3)  # Adjust this value to compress y-axis and expand x-axis

    ax.legend()
    ax.grid(True)
    plt.show()

