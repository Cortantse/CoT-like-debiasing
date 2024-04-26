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






if __name__ == '__main__':
    # 测试函数
    # 测试函数
    print(add_positive_word("the quick brown fox", "sad"))  # "the happy quick brown fox"
    print(add_positive_word("  quick brown fox", "sad"))