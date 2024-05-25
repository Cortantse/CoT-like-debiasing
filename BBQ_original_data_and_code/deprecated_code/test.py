import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from dashscope import Generation
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


if __name__ == '__main__':
    import re


    def find_bracket_contents(text):
        # Find all occurrences of the pattern [xxx]
        matches = re.findall(r'\[(.*?)\]', text)

        if len(matches) >= 1:
            context = ''
            for i in matches:
                context += " " + i
            return context
        else:
            # If zero or more than one matches, raise an error
            raise ValueError("There should be exactly one [xxx] format in the text.")

    print(find_bracket_contents("ajenfgeajbnf [nihao] , [ that's great] "))







