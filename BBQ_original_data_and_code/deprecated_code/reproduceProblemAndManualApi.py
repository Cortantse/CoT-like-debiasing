import json

from API import *
from Util import *
prefix_to_cot = ""
suffix_to_cot = ""
def construct_messages_given_cot_version(content: str, CoT: str):
    messages = []
    messages.append({"role": "user", "content": content})
    messages.append({"role": "assistant", "content": COT_GENERATE})
    messages.append({"role": "assistant", "content": prefix_to_cot + CoT + suffix_to_cot})
    messages.append({"role": "user", "content": LLM_MUST_ANSWER})

    return messages

def construct_messages_no_cot_version(content: str):
    messages = []
    messages.append({"role": "user", "content": content})
    messages.append({"role": "assistant", "content": COT_GENERATE})
    return messages


if __name__ == "__main__":
    def normalize_context(text):
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        text = text.replace("""\'""", """\"""")

        # 将字符串转换为字典
        try:
            context_dict = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("Input string is not a valid JSON")

        # 连接所有值，并删除符号
        normalized_text = ' '.join(context_dict.values()).replace('[', '').replace(']', '')

        return normalized_text


    text = "{'Couple X': 'Couple X is a bisexual couple.', 'Couple Y': 'Couple Y is a gay couple.'} "
    print(normalize_context(text))
