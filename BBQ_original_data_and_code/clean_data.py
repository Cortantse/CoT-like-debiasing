import http.client
import json
import re
import config


def pre_process_json(input_str, extra_character_num=0):
    # Find the index of the first opening brace
    start_index = input_str.find('{')
    # Find the index of the last closing brace
    end_index = input_str.rfind('}')

    # If either start_index or end_index is -1, the braces are not found
    if start_index == -1 or end_index == -1:
        return None  # Or raise an exception, or handle the error as appropriate

    # Extract the substring from the first opening brace to the last closing brace
    processed_str = input_str[start_index:end_index + 1]

    # Check if extra characters need to be added and if they can be added
    if extra_character_num > 0 and len(processed_str) + extra_character_num <= len(input_str):
        # Append the specified number of extra characters from the original string after the last brace
        processed_str += input_str[end_index + 1:end_index + 1 + extra_character_num]

    return processed_str


def clean_string(input_string):
    # 用正则表达式找到所有被双引号包围的字符串
    quoted_strings = re.findall(r'"[^"]*"', input_string)

    # 将字符串中的 \n 和 \t 替换为空，除非它们在双引号中
    cleaned_string = re.sub(r'(?<!")(\n|\t)(?!")', '', input_string)

    # 将先前保存的双引号内字符串替换回去，保留原格式
    for quoted in quoted_strings:
        cleaned_string = cleaned_string.replace(quoted.replace('\n', '').replace('\t', ''), quoted)

    return cleaned_string







def give_background(unmasked_context, masked_context, background_type, ss):
    # override
    background_type = config.BACK_GROUND_INDEX
    # 针对masked_context, model要从masked_context给出相关信息
    # 如果有background风格，还要通过形容词级别的
    messages = []
    context_list = []
    failure = []

    for i in range(config.MAX_ITER_IN_MASK):
        try:

            context = ss
            failure.append(context)
            #对context进行预处理
            context = pre_process_json(context, 2)



            # 替换单引号，因为可能有格式问题
            context = context.replace("""\'""", "")
            context = clean_string(context)
            context = json.loads(context)

            context_copy = context.copy()
            context = context['formatted_differences_between_masked_and_unmasked']
            context = str(context)


            # print(context)
            # print('*'*20)

            #根据不同的background类型选取不同的check方法

            check_background_context_counterfactual(context, context_list, masked_context, context_copy)

            # print('====successfully generate background====')
            # print(context_copy)


            return context

        except Exception as e:
            # this problem in benign, ignore and retry
            # print('---problems in background---')
            # print(context_copy)
            # print(e)
            continue


    # 循环次数又耗尽了，
    # choose as many points as possible
    max_points, max_index = 0, -1

    for i, item in enumerate(context_list):

        if item[0] > max_points:
            max_points = item[0]
            max_index = i


    if len(context_list) == 0:
        print("background could not produce any good results")
        print(failure)
        raise Exception("no background is ever adopted")

    return context_list[0][1]




def check_background_context_counterfactual(context, context_list, masked_context, context_copy):
    context_copy = str(context_copy)
    # Define the regex patterns to match 'X', 'Y', 'Z' only as whole words
    word_list = [r'\bX\b', r'\bY\b', r'\bZ\b']

    # Check if 'X', 'Y', 'Z' are in the masked_context
    if_have_xx_yy_zz = [bool(re.search(word, masked_context)) for word in word_list]

    points = 0
    do_not_have = []
    should_raise = False

    for i, word_pattern in enumerate(word_list):
        if not if_have_xx_yy_zz[i]:
            continue
        if re.search(word_pattern, context) is None:
            should_raise = True
            # Extract single character X, Y, Z for the error message
            word = word_pattern[2]  # Grab the middle character from the pattern
            do_not_have.append(word)
        else:
            # Count occurrences in the context
            match_count = len(re.findall(word_pattern, context))
            points += 1 + match_count * 0.1

    if should_raise:
        context_list.append((points, context))
        raise Exception(f'do not have {", ".join(do_not_have)} in the background context')

    banned_list = ['[positive adjective]', '(entity\'s real name from unmasked context)']

    for item in banned_list:
        if context_copy.find(item) != -1:
            context_list.append((points - 0.5, context))
            raise Exception(f"contain {item}")


import requests
import json


def main():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=vq2NSZ2p6LI57yM1E6GloT3e&client_secret=EsY6R4TBgReQaIV3PNDelNbXBa0kb7Ts"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()

