"""
This module helps to construct prompts like CoT or other potential Natural Language Debiasing prompts.

Also, it helps to extract the answers from the LLM, which may contain errors !!!!!

"""

import re




def delete_all_blanks_and_downcase(text):
    return text.replace(" ", "").lower()



def choose_answer_in_the_end(text):
    # 反转文本
    reversed_text = text[::-1]

    # 使用正则表达式匹配反转后的模式（点后跟随一个大写字母）
    match = re.search(r'\.([A-C])\b', reversed_text)

<<<<<<< Updated upstream
    if match:
        # 反转匹配结果以获取正确的答案
        return match.group(1)[::-1]
    else:
        return "error"


def extract_content(s: str):
    # 检测大括号的数量
    if s.count('{') != 1 or s.count('}') != 1:
        return 'error'

    # 尝试找到大括号内的内容
    try:
        start = s.index('{') + 1
        end = s.index('}')
        content = s[start:end].strip()  # 去除前后空格
        return content
    except ValueError:
        return 'error'


def add_positive_word(original_word, positive_word):
    # 检查单词中是否包含 "the "
    if "The " in original_word:
        # 找到 "the " 后第一个字符的位置
        index = original_word.index("The ") + 4
        # 在 "the " 后插入正面词汇和空格
        new_word = original_word[:index] + positive_word + " " + original_word[index:]
    elif "the " in original_word:
        index = original_word.index("the ") + 4
        # 在 "the " 后插入正面词汇和空格
        new_word = original_word[:index] + positive_word + " " + original_word[index:]
    else:
        # 如果没有 "the"，则在原单词前加入正面词汇和空格
        new_word = positive_word + " " + original_word

    return new_word




=======
# above are deprecated data

'''
samples_template = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[]]),
    'Anti-Bias CoT': np.array([[]]),
    'Pure CoT': np.array([[]]),
    'random shot | plain text | with neutral background': np.array([[]]),
    'random shot | plain text | with positive background': np.array([[]]),
    'random shot | without background': np.array([[]]),
    'random shot | plain text |counterfactual': np.array([[]]),
    'random shot | without background YX': np.array([[]])
}
'''


samples_template_sexual_oritentation = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[0.034965034965034926, 0.8298368298368298, 0.5920745920745921], [0.03480278422273778, 0.8263888888888888, 0.6218097447795824]]),
    'Anti-Bias CoT': np.array([[-0.00462962962962963, 0.2175925925925926, 0.9722222222222222], [0.0, 0.2569444444444444, 0.9722222222222222], [0.0, 0.2361111111111111, 0.9768518518518519]]),
    'Pure CoT': np.array([[-0.027777777777777783, 0.8263888888888888, 0.8194444444444444], [0.00925925925925926, 0.8379629629629629, 0.83]]),
    'random shot | plain text | with neutral background': np.array([[0.011574074074074079, 0.8888888888888888, 0.7986111111111112], [0.0, 0.8935185185185185, 0.80]]),
    'random shot | plain text | with positive background': np.array([[0.018518518518518528, 0.8587962962962963, 0.8425925925925926], [-0.004629629629629626, 0.8842592592592593, 0.847]]),
    'random shot | without background': np.array([[-0.07192575406032481, 0.8842592592592593, 0.6774941995359629], [0.011600928074245951, 0.9097222222222222, 0.65]]),
    'random shot | plain text |counterfactual': np.array([[0.03703703703703704, 0.8425925925925926, 0.6851851851851852], [-0.053240740740740734, 0.8703703703703703, 0.6689]]),
    'random shot | without background YX': np.array([[-0.05581395348837208, 0.8935185185185185, 0.7302325581395349], [0.0, 0.8796296296296297, 0.6435]])
}

samples_template_age = {
    'Baseline': np.array([[0.16775956284152999, 0.9132821075740944, 0.285792349726776],[0.1647446457990116, 0.914881933003844, 0.23997803404722678]]),
    'Anti-Bias CoT': np.array([[0.021195652173913032, 0.5809782608695652, 0.8646739130434783], [-0.00869565217391304, 0.5869565217391305, 0.8706521739130435]]),
    'Pure CoT': np.array([[0.12173913043478266, 0.9222826086956522, 0.5358695652173913],[0.13757476889613918, 0.9135869565217392, 0.43610657966286026]]),
    'random shot | plain text | with neutral background': np.array([[0.058823529411764656, 0.8111050626020686, 0.514161220043573], [0.05869565217391307, 0.9173913043478261, 0.46195652173913043]]),
    'random shot | plain text | with positive background': np.array([[0.05991285403050111, 0.8194217130387343, 0.5958605664488017],[0.04945652173913041, 0.903804347826087, 0.5451086956521739]]),
    'random shot | without background': np.array([[-0.00924415443175638, 0.833968426782798, 0.641653072321914], [-0.0038084874863982404, 0.9326086956521739, 0.6131664853101197]]),
    'random shot | plain text |counterfactual': np.array([[-0.035422343324250705, 0.8723404255319149, 0.5340599455040872], [-0.04782608695652172, 0.9163043478260869, 0.42934782608695654]]),
    'random shot | without background YX': np.array([[-0.00924415443175638, 0.833968426782798, 0.641653072321914], [0.01468988030467899, 0.9402173913043478, 0.6088139281828074]])
}


samples_template_gender_identity = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[0.1301128349788435, 0.8653032440056417, 0.42348377997179126], [0.14209780297661231, 0.8902654867256637, 0.45038979447200567]]),
    'Anti-Bias CoT': np.array([[0.09203102961918198, 0.49823695345557123, 0.9199576868829337], [0.10401974612129765, 0.5334978843441467, 0.9122002820874471], [0.10260930888575458, 0.4947108603667137, 0.8967]]),
    'Pure CoT': np.array([[0.10366713681241187, 0.866361071932299, 0.8730606488011283], [0.11820748059280171, 0.8557827926657263, 0.76]]),
    'random shot | plain text | with neutral background': np.array([[0.09848217437345569, 0.8808180535966149, 0.7850335333568655], [0.0895943562610229, 0.8804654442877292, 0.81]]),
    'random shot | plain text | with positive background': np.array([[0.0942131263232181, 0.8325105782792666, 0.888849682427664], [0.09167842031029623, 0.8466149506346967, 0.885049365303244]]),
    'random shot | without background': np.array([[0.0823903818953324, 0.863091037402964, 0.8384016973125884], [0.07624426403106248, 0.8797602256699577, 0.7472643840451818]]),
    'random shot | plain text |counterfactual': np.array([[0.04165195905400637, 0.8215796897038082, 0.5848923402753265], [0.020803949224259564, 0.8437940761636107, 0.6054]]),
    'random shot | without background YX': np.array([[0.08309659090909093, 0.8416784203102962, 0.8579545454545454], [0.07094952347334985, 0.8787023977433004, 0.7526]])
}

samples_template_religion = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[0.05536912751677855, 0.825, 0.62248322147651]]),
    'Anti-Bias CoT': np.array([[0.021666666666666647, 0.43333333333333335, 0.9583333333333334]]),
    'Pure CoT': np.array([[0.08166666666666665, 0.81, 0.675]]),
    'random shot | plain text | with neutral background': np.array([[0.020000000000000014, 0.82, 0.8333333333333334]]),
    'random shot | plain text | with positive background': np.array([[0.03171953255425707, 0.795, 0.8480801335559266]]),
    'random shot | without background': np.array([[0.0100000000000000, 0.85, 0.75]]),
    'random shot | plain text |counterfactual': np.array([[0.026666666666666696, 0.82, 0.7166666666666667]]),
    'random shot | without background YX': np.array([[0.03500000000000001, 0.86, 0.7783333333333333]])
}

samples_template_disability = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[-0.06056701030927834, 0.8724226804123711, 0.3492268041237113]]),
    'Anti-Bias CoT': np.array([[-0.012853470437017992, 0.4254498714652956, 0.8226221079691517]]),
    'Pure CoT': np.array([[-0.016731016731016724, 0.7737789203084833, 0.5637065637065637]]),
    'random shot | plain text | with neutral background': np.array([[-0.005141388174807221, 0.8316195372750642, 0.5835]]),
    'random shot | plain text | with positive background': np.array([[-0.03341902313624679, 0.8239074550128535, 0.6143958868894601]]),
    'random shot | without background': np.array([[-0.05276705276705276, 0.8598971722365039, 0.5868725868725869]]),
    'random shot | plain text |counterfactual': np.array([[-0.0077120822622107725, 0.8187660668380463, 0.46786632390745503]]),
    'random shot | without background YX': np.array([[-0.019305019305019294, 0.8598971722365039, 0.60231]])
}



samples_template_nationality = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[0.13485342019543972, 0.9426710097719869, 0.3973941368078176]]),
    'Anti-Bias CoT': np.array([[-0.0019493177387914235, 0.4785714285714286, 0.897985]]),
    'Pure CoT': np.array([[0.11623376623376623, 0.9012987012987013, 0.6097]]),
    'random shot | plain text | with neutral background': np.array([[0.09155844155844158, 0.893506493506493, 0.60974]]),
    'random shot | plain text | with positive background': np.array([[0.03506493506493507, 0.8675324675324675, 0.7675]]),
    'random shot | without background': np.array([[-0.003255208333333315, 0.9012987012987013, 0.57747]]),
    'random shot | plain text |counterfactual': np.array([[-0.0012987012987013178, 0.8538961038961039, 0.512987]]),
    'random shot | without background YX': np.array([[-0.004548408057179971, 0.9168831168831169, 0.58609]])
}


samples_template_physical_appearace = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[0.0317662007623888, 0.7903430749682337, 0.4625]]),
    'Anti-Bias CoT': np.array([[-0.007614213197969542, 0.2906091370558376, 0.9517766497461929]]),
    'Pure CoT': np.array([[0.04822335025380709, 0.7461928934010152, 0.7944162436548223]]),
    'random shot | plain text | with neutral background': np.array([[0.041878172588832495, 0.7461928934010152, 0.7956852791878173]]),
    'random shot | plain text | with positive background': np.array([[0.01776649746192895, 0.7791878172588832, 0.8223350253807107]]),
    'random shot | without background': np.array([[-0.005076142131979692, 0.7639593908629442, 0.883248730964467]]),
    'random shot | plain text |counterfactual': np.array([[0.038071065989847705, 0.7626903553299492, 0.7030456852791879]]),
    'random shot | without background YX': np.array([[0.012820512820512822, 0.8274111675126904, 0.8487179487179487]])
}


samples_template_race_ethnicity = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[0.06341749853200235, 0.9535359438924605, 0.4809]]),
    'Anti-Bias CoT': np.array([[0.010465116279069767, 0.5380813953488373, 0.924419]]),
    'Pure CoT': np.array([[0.017441860465116248, 0.9165697674418605, 0.7244186046511628]]),
    'random shot | plain text | with neutral background': np.array([[0.013081395348837208, 0.9142441860465116, 0.8200581395348837]]),
    'random shot | plain text | with positive background': np.array([[0.002034883720930231, 0.8976744186046511, 0.8886627906976744]]),
    'random shot | without background': np.array([[0.004941860465116289, 0.9139284675777842, 0.8148255813953489]]),
    'random shot | plain text |counterfactual': np.array([[0.0029069767441860135, 0.8892441860465117, 0.6535]]),
    'random shot | without background YX': np.array([[-0.00785797438882421, 0.9151162790697674, 0.7668800931315483]])
}


samples_template_SES = {
    # 把模板打出来就好，不需要有数据
    'Baseline': np.array([[0.1699000587889476, 0.9306409130816505, 0.49088771310993534]]),
    'Anti-Bias CoT': np.array([[0.041083916083916074, 0.5203962703962703, 0.9157925407925408]]),
    'Pure CoT': np.array([[0.13461538461538464, 0.8974358974358975, 0.6614219114219114]]),
    'random shot | plain text | with neutral background': np.array([[0.13752913752913754, 0.8569347319347319, 0.6462703962703963]]),
    'random shot | plain text | with positive background': np.array([[0.08772952491984846, 0.8114801864801865, 0.753716117749927]]),
    'random shot | without background': np.array([[0.0011675423234092234, 0.8948135198135199, 0.8143607705779334]]),
    'random shot | plain text |counterfactual': np.array([[0.10139860139860135, 0.8554778554778555, 0.6328671328671329]]),
    'random shot | without background YX': np.array([[0.003242924528301879, 0.8703379953379954, 0.8935731132075472]])
}



if __name__ == '__main__':
    import numpy as np


    # 定义加权调和平均数函数
    def weighted_harmonic_mean(values, weights):
        weighted_sum = sum(w / v for v, w in zip(values, weights) if v > 0)
        total_weight = sum(weights)
        return total_weight / weighted_sum if weighted_sum != 0 else 0


    # 数据集样本数量
    weights = {
        'sexual_orientation': [864],
        'age': [3080],
        'gender_identity': [5672],
        'religion': [1200],
        'disability': [1556],
        'nationality': [3680],
        'physical_appearance': [1576],
        'race_ethnicity': [6880],
        'social_economic_status': [6864]
    }

    # 生成模板中的数据，替换为实际数据
    samples = {
        'sexual_orientation': samples_template_sexual_oritentation,
        'age': samples_template_age,
        'gender_identity': samples_template_gender_identity,
        'religion': samples_template_religion,
        'disability': samples_template_disability,
        'nationality': samples_template_nationality,
        'physical_appearance': samples_template_physical_appearace,
        'race_ethnicity': samples_template_race_ethnicity,
        'social_economic_status': samples_template_SES
    }


    # 加权平均数计算函数
    def weighted_mean(values, weights):
        return np.sum(values * weights) / np.sum(weights)


    # 计算每种方法在所有数据集上的两个加权平均数
    results = {}
    for dataset, methods in samples.items():
        for method, data in methods.items():
            # 转换性能指标的第一个元素为绝对值
            data[:, 0] = np.abs(data[:, 0]) / len(data)
            # 处理第二个性能指标使其接近1的误差
            data[:, 1] = np.abs(data[:, 1]) / len(data)

            if method not in results:
                results[method] = [[], []]  # 分别存储两个性能指标的结果

            # 对每个性能指标计算加权平均数
            for i in range(2):
                result = weighted_mean(data[:, i], weights[dataset])
                results[method][i].append(result)

    # 格式化输出结果
    for method, metrics in results.items():
        metric1_avg = np.mean(metrics[0])
        metric2_avg = np.mean(metrics[1])
        print(f"{method}: Metric 1 (closer to 0 better): {metric1_avg}, Metric 2 (closer to 1 better): {metric2_avg}")


    # # 计算每种方法在所有数据集上的两个加权调和平均数
    # results = {}
    # for dataset, methods in samples.items():
    #     for method, data in methods.items():
    #         # 转换性能指标的第一个元素为绝对值
    #         data[:, 0] = np.abs(data[:, 0])
    #         # 处理第二个性能指标使其接近1的误差
    #         data[:, 1] = np.abs(data[:, 1])
    #
    #         if method not in results:
    #             results[method] = [[], []]  # 分别存储两个性能指标的结果
    #
    #         # 对每个性能指标计算加权调和平均数
    #         for i in range(2):
    #             result = weighted_harmonic_mean(data[:, i], weights[dataset])
    #             results[method][i].append(result)
    #
    # # 格式化输出结果
    # for method, metrics in results.items():
    #     metric1_avg = np.mean(metrics[0])
    #     metric2_avg = np.mean(metrics[1])
    #     print(f"{method}: Metric 1 (closer to 0 better): {metric1_avg}, Metric 2 (closer to 1 better): {metric2_avg}")

if __name__ == '__main__':
<<<<<<< Updated upstream
    # 测试函数
    # 测试函数
    print(add_positive_word("the quick brown fox", "sad"))  # "the happy quick brown fox"
    print(add_positive_word("  quick brown fox", "sad"))
=======

    samples = samples_template_SES
    data_set_name = 'social economic status'

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
            color='black', linestyle=':', linewidth=1.8, label='Cumulative Pareto Frontier')

    # Enhance the plot
    ax.set_title(data_set_name)
    ax.set_xlabel('Bias Score (1 - |Ambig Bias Score|)')
    ax.set_ylabel('Accuracy (Disambiguous QA)')

    # Set the tick intervals for both axes
    x_ticks = np.arange(0.80, 1.01, 0.01)
    y_ticks = np.arange(0.2, 1.01, 0.05)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # Set the aspect ratio (compress y values and expand x values)
    ax.set_aspect(0.25)  # Adjust this value to compress y-axis and expand x-axis

    ax.legend()
    ax.grid(True)
    plt.show()
>>>>>>> Stashed changes
