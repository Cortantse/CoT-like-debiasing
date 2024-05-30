import json
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
import pandas as pd
from dashscope import Generation
from openai import OpenAI
from tqdm import tqdm


def check_validity(input_str):
    # 定义正则表达式匹配 [A], [B], [C]
    pattern = re.compile(r'\[([ABC])\]')

    # 从后向前查找匹配的 [A], [B], [C]
    matches = list(pattern.finditer(input_str))[::-1]

    for match in matches:
        # 获取匹配到的字母和位置
        letter = match.group(1)
        position = match.start()

        # 检查该位置前是否有其他的 [A], [B], [C]
        previous_text = input_str[:position]
        previous_matches = list(pattern.finditer(previous_text))

        if previous_matches:
            # 如果前面有 [A], [B], [C]，抛出错误
            raise ValueError(f"Error: Found {letter} at position {position}, but previous matches exist.")
        else:
            # 如果前面没有 [A], [B], [C]，返回该字母
            return letter

    # 如果没有找到任何 [A], [B], [C]，抛出错误
    raise ValueError("Error: No [A], [B], or [C] found in the input string.")

def color():
    import matplotlib.pyplot as plt
    import pandas as pd

    import matplotlib.pyplot as plt

    # Data
    methods = [
        "Baseline", "Pure CoT", "Anti-bias CoT", "Pro-bias CoT",
        "Pure SM 2A3R", "AB SM 2A3R", 'Role-play', "'BOC'+short CoT"
    ]
    acc_in_ambig = [48.7, 64.5, 76.4, 36.9, 71.0, 86.5, 84.8, 75.4]
    acc_in_disambig = [84.6, 72.1, 60.3, 55.9, 85.5, 63.7, 38, 87.3]

    # Plotting
    fig, ax = plt.subplots()
    scatter = ax.scatter(acc_in_ambig, acc_in_disambig, c=range(len(methods)), cmap='viridis', s=100, marker='o')

    # Labels and Titles
    ax.set_xlabel('Accuracy in Ambiguous (%)')
    ax.set_ylabel('Accuracy in Disambiguated (%)')
    ax.set_title('Accuracy Comparison across Methods')
    plt.grid(True)

    # Adding annotations for each point
    for i, txt in enumerate(methods):
        ax.annotate(txt, (acc_in_ambig[i], acc_in_disambig[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    # Color bar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Method Index')
    cbar.set_ticks(range(len(methods)))
    cbar.set_ticklabels(methods)

    plt.show()


def other():
    import matplotlib.pyplot as plt
    import pandas as pd

    # Data for the plot
    data = {
        "Method": ["B","'BOC' sCoT", "pure CoT", "anti-B CoT", "Role-play","SM2 3R", "AB SM2 3R"],
        "Generation Fee Ratio": [1, 19.31679688, 30.16542969, 49.17988281, 190, 183.2304688, 281.3488281, ],
        "Overall Fee Ratio": [1, 2.064284258, 3.301685893, 4.051197921, 17, 42.52985371, 60.95110167]
    }

    # Creating a DataFrame
    df = pd.DataFrame(data)

    # Plotting the data
    fig, ax = plt.subplots()
    width = 0.3  # Bar width

    # Bars for Generation Fee Ratio
    rects1 = ax.bar(df.index - width / 2, df["Generation Fee Ratio"], width, label='Generation Fee Ratio')

    # Bars for Overall Fee Ratio
    rects2 = ax.bar(df.index + width / 2 , df["Overall Fee Ratio"], width, label='Overall Fee Ratio')

    # Adding some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Method')
    ax.set_title('Fee Ratios Compared to Baseline')
    ax.set_xticks(df.index)
    ax.set_xticklabels(df["Method"])
    ax.legend()

    # Function to add labels on bars
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'x{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    add_labels(rects1)
    add_labels(rects2)

    # Displaying the plot
    plt.tight_layout()  # Adjust layout to make room for label rotation
    plt.show()

def monitor_progress(pbar, status_array, num_of_jsons):
    while True:
        processed = sum(status_array)
        pbar.n = processed
        pbar.refresh()
        if processed == num_of_jsons:
            break
        time.sleep(1)  # Update every 1 second

class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

class Choice:
    def __init__(self, finish_reason, message):
        self.finish_reason = finish_reason
        self.message = message

class Completion:
    def __init__(self, choices):
        self.choices = choices






import matplotlib.pyplot as plt
import numpy as np

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

samples = {
    'Baseline': np.array([
        ## 1
        #[0.09600000000000004, 0.914, 0.44],
        ## 2
        [0.09638554216867475, 0.9418837675350702, 0.3534136546184739],
        [0.08999999999999997, 0.848, 0.514],
        [0.030000000000000023, 0.85, 0.514],
        [0.07214428857715434, 0.9418837675350702, 0.3587174348697395]
    ]),
    'Anti-Bias CoT': np.array([
        ## 1
        #[0.078, 0.742, 0.634],
        ## 2
        [-0.00999999999999999, 0.5682730923694779, 0.774]
    ]),
    'Pure CoT': np.array([
        ## 1
        #[0.13827655310621242, 0.932, 0.6092184368737475],
        ## 2
        [0.1, 0.944, 0.596]
    ]),
    # 'Advice': np.array([
    #     [0.060344827586206906, 0.6367521367521367, 0.8060344827586207]
    # ]),
    # 'filtered in masking | without background': np.array([
    #     [0.03413654618473893, 0.845691382765531, 0.7048192771084337],
    # ]),
    'filtered in masking | with neutral background': np.array([
        ## 1
        #[0.03012048192771083, 0.8868686868686869, 0.7008032128514057],
        ## 2
        [0.1310483870967742, 0.9018036072144289, 0.6471774193548387]
    ]),
    'filtered in masking | with positive background': np.array([
        ## 1
        #[0.036000000000000004, 0.806, 0.82],
        ## 2
        [0.06412825651302607, 0.798, 0.7675350701402806]
    ]),
    'filtered in masking | with positive background Deep Seek': np.array([
        ## 1
        [0.08199999999999996, 0.7675350701402806, 0.798]
    ]),
    # 'not_filter in masking | without background': np.array([
    #     [0.007999999999999972, 0.8777555110220441, 0.688],
    # ]),
}

samples_sexual_orientation = {
    'Baseline': np.array([
        [0.018518518518518545, 0.7199074074074074, 0.75],
        [-0.013888888888888895, 0.691415313225058, 0.76],
        [0.020833333333333325, 0.6960556844547564, 0.76],
        [0.018518518518518504, 0.7013888888888888, 0.76],
        [0.02546296296296295, 0.6759259259259259, 0.76],
        [0.023201856148491906, 0.708, 0.7679814385150812],
        [0, 0.6898148148148148, 0.74],
        [0.03935185185185188, 0.6782407407407407, 0.76],
        [0.006944444444444458, 0.6944444444444444, 0.747],
        [0.006944444444444421, 0.7129629629629629, 0.7569444444444444],
        [0.050925925925925916, 0.7314814814814815, 0.7638888888888888],
    ]),
    'Anti-Bias CoT': np.array([
        [0.013888888888888881, 0.42592592592592593, 0.8],
        [-0.013888888888888881, 0.49074074074074076, 0.8],
        [0.006976744186046501, 0.4375, 0.83],
        [-0.006944444444444438, 0.43287037037037035, 0.79],
        [-0.00232018561484919, 0.4375, 0.765661252900232],
        [-0.0138888888888889, 0.4837962962962963, 0.8],
        [-0.016241299303944322, 0.45243619489559167, 0.81],
        [-0.011574074074074079, 0.46990740, 0.7986],
    ]),
    'Pure CoT': np.array([
        [0.0023201856148491904, 0.7129629629629629, 0.86],
        [-0.03051643192488263, 0.7314814814814815, 0.81],
        [0, 0.7523148148148148, 0.83],
        [0.006960556844547556, 0.7106481481481481, 0.84],
        [0.02093023255813953, 0.7447795823665894, 0.8441860465116279],
        [-0.009302325581395349, 0.7523148148148148, 0.84],
        [-0.011600928074245944, 0.7268518518518519, 0.84],
        [0.041666666666666664, 0.7337962962962963, 0.84],
        [0.018604651162790704, 0.7638888888888888, 0.8279],
        [0.009280742459396734, 0.7546296296296297, 0.8283062645011601],
    ]),
    # 'not plain text | with neutral background': np.array([
    #     [-0.0023201856148491943, 0.75, 0.87],
    # ]),
    # 'not plain text | with positive background': np.array([
    #     [0.030232558139534904, 0.7685185185185185, 0.89],
    # ]),
    # 'plain text | with neutral background': np.array([
    #     [0.023148148148148147, 0.7083333333333334, 0.85],
    #     [0.01388888888888888, 0.7037037037037037, 0.84],
    # ]),
    # 'plain text | with positive background': np.array([
    #     [-0.004629629629629624, 0.7610208816705336, 0.86],
    #     [0.002314814814814801, 0.7331786542923434, 0.87],
    # ]),
    'random shot | plain text | with neutral background': np.array([
        [0.016203703703703703, 0.7384259259259259, 0.84],
        [-0.03240740740740741, 0.777262180974478, 0.82],
        [0.023201856148491896, 0.7384259259259259, 0.85],
        [0.004640371229698386, 0.7361111111111112, 0.865],
        [0.016203703703703692, 0.7361111111111112, 0.8587962962962963],
    ]),
    'random shot | plain text | with positive background': np.array([
        [-0.03016241299303945, 0.7633410672853829, 0.87],
        [0.016203703703703706, 0.7430555555555556, 0.88],
        [0.027777777777777766, 0.7476851851851852, 0.884],
        [-0.004629629629629636, 0.7800925925925926, 0.875],
    ]),
    'random shot|without background': np.array([
        [0, 0.7754629629629629, 0.58],
        [0.034802784222737776, 0.7587006960556845, 0.58],
        [-0.004651162790697683, 0.802784222737819, 0.6],
        [-0.006944444444444459, 0.7962962962962963, 0.6273148148148148],
    ]),
}

samples_age = {
    'Baseline': np.array([[0.1375, 0.8652173913043478, 0.3418478260869565],[0.10652173913043472, 0.8543478260869565, 0.33369565217391306], [0.12717391304347833, 0.8521739130434782, 0.34891304347826085]]),
    'Anti-Bias CoT': np.array([[0.026086956521739146, 0.6152173913043478, 0.6793478260869565],[0.023394994559303595, 0.6010869565217392, 0.6991294885745375], [0.03425774877650895, 0.6010869565217392, 0.6982055464926591]]),
    'Pure CoT': np.array([[0.1273122959738847, 0.8467391304347827, 0.5375408052230686],[0.1353260869565218, 0.8694942903752039, 0.5103260869565217], [0.1483695652173913, 0.8728260869565218, 0.5222826086956521]]),
    'random shot | plain text | with neutral background': np.array([[0.06212534059945504, 0.817983651226158, 0.5040871934604905], [0.05111473626971176, 0.8058727569331158, 0.5290918977705275], [0.058823529411764656, 0.8111050626020686, 0.514161220043573]]),
    'random shot | plain text | with positive background': np.array([[0.03427638737758436, 0.8202614379084967, 0.6142546245919478],[0.05991285403050111, 0.8194217130387343, 0.5958605664488017]]),
    'random shot | without background': np.array([[0.011444141689373277, 0.8504622077215879 , 0.6561307901907357],[-0.00924415443175638, 0.833968426782798, 0.641653072321914]]),
}

samples_disability_DS = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[-0.05526992287917737, 0.9395886889460154, 0.7519280205655527],
[-0.06555269922879177, 0.9408740359897172, 0.7596401028277635],
[-0.05655526992287918, 0.9395886889460154, 0.7557840616966581],
[-0.06041131105398458, 0.9383033419023136, 0.7544987146529563],
[-0.06169665809768638, 0.9370179948586118, 0.7506426735218509],]),
    'Anti-Bias CoT': np.array([[0.0, 0.8920308483290489, 0.9948586118251928],
[0.0, 0.8920308483290489, 0.9897172236503856],
[0.0, 0.8933161953727506, 0.9948586118251928],
[0.0012853470437017567, 0.8997429305912596, 0.9987146529562982],
[-0.0025706940874035875, 0.8946015424164524, 0.9922879177377892],]),
    'Pure CoT': np.array([[-0.012853470437017985, 0.9473007712082262, 0.9151670951156813],
    [-0.0154241645244216, 0.9498714652956298, 0.9203084832904884],
    [-0.011568123393316195, 0.9473007712082262, 0.9190231362467867],
    [-0.0077120822622108, 0.9473007712082262, 0.9203084832904884],
    [-0.0064267352185089985, 0.9550128534704371, 0.9138817480719794],
    [-0.02570694087403598, 0.9550128534704371, 0.9125964010282777],
    [0.0025706940874036, 0.9485861182519281, 0.9357326478149101]]),
    'random shot | plain text | with neutral background': np.array([[-0.03217503217503219, 0.9768339768339769, 0.9034749034749034],
    [-0.02831402831402831, 0.9741267787839586, 0.9047619047619048]]),
    'random shot | plain text | with positive background': np.array([[-0.023285899094437245, 0.9713914174252276, 0.9275549805950841],
    [-0.015624999999999997, 0.9767141009055628, 0.9192708333333334]]),
    'random shot | without background': np.array([[-0.015483870967741953, 0.980719794344473, 0.9690322580645161]]),
    'random shot | plain text |counterfactual': np.array([[-0.04798962386511024, 0.9766536964980544, 0.8041504539559015]])
}

samples_age_DS = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[0.1282608695652174, 0.9880434782608696, 0.5804347826086956]]),
    'Anti-Bias CoT': np.array([[0.026630434782608712, 0.9358695652173913, 0.9614130434782608]]),
    'Pure CoT': np.array([[0.0967391304347826, 0.9869565217391304, 0.725]]),
    # 'random shot | plain text | with neutral background': np.array([]),
    'random shot | plain text | with positive background': np.array([[0.052717391304347834, 0.9538043478260869, 0.8494565217391304]]),
    'random shot | without background': np.array([[0.0010869565217391283, 0.9875, 0.9641304347826087]]),
    # 'random shot | plain text |counterfactual': np.array([])
}

# samples_template = {
#     # 把模板打出来就好，不需要有数据
#     'Baseline': np.array([[ambiguo_bias_score, disab_acc, ambig_acc], [], []]),
#     'Anti-Bias CoT': np.array(),
#     'Pure CoT': np.array([]),
#     'random shot | plain text | with neutral background': np.array([]),
#     'random shot | plain text | with positive background': np.array([]),
#     'random shot | without background': np.array([]),
#     'random shot | plain text |counterfactual': np.array([])
# }




import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    samples = samples_age

    if_only_need_central_point = False

    if if_only_need_central_point:
        for item in samples:
            average_x, average_y, average_acc = np.mean(samples[item][:, 0]), np.mean(samples[item][:, 1]), np.mean(samples[item][:, 2])
            samples[item] = np.array([[average_x, average_y, average_acc]])

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

        # Annotate each point with its extra_acc value
        for i, txt in enumerate(samples[key][:, 2]):
            ax.annotate(f'{txt:.2f}', (samples[key][i, 0], samples[key][i, 1]), fontsize=9)

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
    x_ticks = np.arange(0.80, 1.01, 0.01)
    y_ticks = np.arange(0.3, 1.01, 0.05)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # Set the aspect ratio (compress y values and expand x values)
    ax.set_aspect(0.25)  # Adjust this value to compress y-axis and expand x-axis

    ax.legend()
    ax.grid(True)
    plt.show()