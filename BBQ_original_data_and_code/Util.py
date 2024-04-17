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
