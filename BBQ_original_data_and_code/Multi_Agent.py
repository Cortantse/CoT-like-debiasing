"""
本文件总结

使用Agent方法来对LLM生成结果进行去偏
主要需要实现的框架如下
1、定义Agent和 Multi-Agent框架
2、将输入传入Multi-Agent的框架
4、获取答案并将其转变为需要的格式
5、使用数据集比较
"""
import http
import random
import threading
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from dashscope import get_tokenizer  # dashscope版本 >= 1.14.0
import httpx
import tiktoken
import transformers
import logging
import pickle
from dashscope import Generation
import glob
logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)
from openai import OpenAI
from tqdm import tqdm
from dependency import monitor_progress
from dependency import read_jsonl
import dependency as dd
from dependency import construct_question_from_json
from dependency import FileSystem
import time
import config
import re
from collections import defaultdict
from prompts import  *

token_fee = [0.0]
generate_token_fee = [0.0]
dropping_num = [0]
not_perfect_context_masked = [0]
iter_time = [0]
dropping_num_due_to_background = [0]
not_perfect_background_generation = [0]
definite_dropping_num = [0]
bad_masking = [0]
bad_background = [0]

masking_actual_usage = [0]
back_ground_actual_usage = [0]
CoT_asking_actual_usage = [0]

DATA_LIST = []
MASKING_CONTEXT = {}
MASKING_NUM = [0]
DEADLY_SIGNAL = False
need_print_mask = False

need_print_background = False
NO_MASKING = False



class MaskSystem:
    def __init__(self, agents=None):
        if agents is None:
            agents = []
        self.agents = agents

    def initiate_mask_example(self, question) -> []:
        messages = []
        example1_question = mask_asking.copy()
        example1_question['context'] = example1_context
        example1_anwer = {
            "context": example1_context,
            # "task": f"{mask_prompt}",
            "attributes_involved": example1_attributes_involved,
            # "step1": example1_thinking_step1,
            # "step2": example1_thinking_step2,
            "context_masked": example1_context_masked,
        }

        example2_question = mask_asking.copy()
        example2_question['context'] = example2_context
        example2_anwer = {
            "context": example2_context,
            # "task": f"{mask_prompt}",
            "attributes_involved": example2_attributes_involved,
            # "step1": example2_thinking_step1,
            # "step2": example2_thinking_step2,
            "context_masked": example2_context_masked,
        }

        # example3_question = mask_asking.copy()
        # example3_question['context'] = example3_context
        # example3_anwer = {
        #     "context": example3_context,
        #     "task": f"{mask_prompt}",
        #     "attributes_involved": example3_attributes_involved,
        #     "step1": example3_thinking_step1,
        #     "context_masked": example3_context_masked,
        # }

        example4_question = mask_asking.copy()
        example4_question['context'] = example4_context
        example4_anwer = {
            "context": example4_context,
            # "task": f"{mask_prompt}",
            "attributes_involved": example4_attributes_involved,
            # "step1": example4_thinking_step1,
            # "step2": example4_thinking_step2,
            "context_masked": example4_context_masked,
        }

        example6_question = mask_asking.copy()
        example6_question['context'] = example6_context
        example6_anwer = {
            "context": example6_context,
            # "task": f"{mask_prompt}",
            "attributes_involved": example6_attributes_involved,
            # "step1": example6_thinking_step1,
            # "step2": example6_thinking_step2,
            "context_masked": example6_context_masked,
        }

        example7_question = mask_asking.copy()
        example7_question['context'] = example7_context
        example7_anwer = {
            "context": example7_context,
            # "task": f"{mask_prompt}",
            "attributes_involved": example7_attributes_involved,
            # "step1": example7_thinking_step1,
            # "step2": example7_thinking_step2,
            "context_masked": example7_context_masked,
        }

        example8_question = mask_asking.copy()
        example8_question['context'] = example8_context
        example8_answer = {
            "context": example8_context,
            # "task": f"{mask_prompt}",
            "attributes_involved": example8_attributes_involved,
            # "step1": example7_thinking_step1,
            # "step2": example7_thinking_step2,
            "context_masked": example8_context_masked,
        }

        messages_list = []
        messages_list.append((example1_question, example1_anwer))
        messages_list.append((example2_question, example2_anwer))
        messages_list.append((example4_question, example4_anwer))
        messages_list.append((example6_question, example6_anwer))
        messages_list.append((example7_question, example7_anwer))
        messages_list.append((example8_question, example8_answer))

        random.shuffle(messages_list)

        for item in messages_list:
            messages.append({'role': 'user', 'content': json.dumps(item[0])})
            messages.append({'role': 'assistant', 'content': json.dumps(item[1])})

        # messages.append({'role': 'user', 'content': json.dumps(example1_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example1_anwer)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example2_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example2_anwer)})
        #
        #
        # messages.append({'role': 'user', 'content': json.dumps(example4_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example4_anwer)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example6_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example6_anwer)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example7_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example7_anwer)})

        # 这里应该要设计随机打乱系统
        # !!!并且应该每次随机打乱


        asking_question = mask_asking.copy()
        asking_question['context'] = question
        messages.append({'role': 'user', 'content': json.dumps(asking_question)})

        return messages

    def normalize_context(self, text):
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        text = text.replace("""\'""", """\"""")

        # 将字符串转换为字典
        try:
            context_dict = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("Input string is not a valid JSON")

        # 连接所有值，并删除符号
        normalized_text = ' '.join(context_dict.values()).replace('[', '').replace(']', '').replace("(", "").replace(")", "")

        return normalized_text

    def initiate_background_example_counterfactual(self, masked_context, unmasked_context):
        messages = []

        example1_question = background_asking_counterfactual.copy()
        example1_question['unmasked_context'] = example1_background_unmasked_context.replace("""\'""", "")
        example1_question['masked_context'] = example1_background_masked_context.replace("""\'""", "")

        example2_question = background_asking_counterfactual.copy()
        example2_question['unmasked_context'] = example2_background_unmasked_context.replace("""\'""", "")
        example2_question['masked_context'] = example2_background_masked_context.replace("""\'""", "")

        example3_question = background_asking_counterfactual.copy()
        example3_question['unmasked_context'] = example3_background_unmasked_context.replace("""\'""", "")
        example3_question['masked_context'] = example3_background_masked_context.replace("""\'""", "")

        example4_question = background_asking_counterfactual.copy()
        example4_question['unmasked_context'] = example4_background_unmasked_context.replace("""\'""", "")
        example4_question['masked_context'] = example4_background_masked_context.replace("""\'""", "")


        example7_question = background_asking_counterfactual.copy()
        example7_question['unmasked_context'] = example7_background_unmasked_context.replace("""\'""", "")
        example7_question['masked_context'] = example7_background_masked_context.replace("""\'""", "")

        messages_list = []
        messages_list.append((example1_question, example1_background_response_counterfactual))
        messages_list.append((example2_question, example2_background_response_counterfactual))
        messages_list.append((example3_question, example3_background_response_counterfactual))
        messages_list.append((example4_question, example4_background_response_counterfactual))
        messages_list.append((example7_question, example7_background_response_counterfactual))

        random.shuffle(messages_list)

        for item in messages_list:
            messages.append({'role': 'user', 'content': json.dumps(item[0])})
            messages.append({'role': 'assistant', 'content': json.dumps(item[1])})


        asking_question = background_asking_counterfactual.copy()
        asking_question['unmasked_context'] = unmasked_context
        asking_question['masked_context'] = masked_context
        messages.append({'role': 'user', 'content': json.dumps(asking_question)})

        return messages


    def initiate_background_example_pure_join(self, masked_context, unmasked_context):
        messages = []

        example1_question = background_asking_neutral.copy()
        example1_question['unmasked_context'] = example1_background_unmasked_context.replace("""\'""", "")
        example1_question['masked_context'] =  example1_background_masked_context.replace("""\'""", "")

        example2_question = background_asking_neutral.copy()
        example2_question['unmasked_context'] = example2_background_unmasked_context.replace("""\'""", "")
        example2_question['masked_context'] =  example2_background_masked_context.replace("""\'""", "")

        example3_question = background_asking_neutral.copy()
        example3_question['unmasked_context'] = example3_background_unmasked_context.replace("""\'""", "")
        example3_question['masked_context'] =  example3_background_masked_context.replace("""\'""", "")

        example4_question = background_asking_neutral.copy()
        example4_question['unmasked_context'] = example4_background_unmasked_context.replace("""\'""", "")
        example4_question['masked_context'] =  example4_background_masked_context.replace("""\'""", "")

        example5_question = background_asking_neutral.copy()
        example5_question['unmasked_context'] = example5_background_unmasked_context.replace("""\'""", "")
        example5_question['masked_context'] =  example5_background_masked_context.replace("""\'""", "")

        example6_question = background_asking_neutral.copy()
        example6_question['unmasked_context'] = example6_background_unmasked_context.replace("""\'""", "")
        example6_question['masked_context'] =  example6_background_masked_context.replace("""\'""", "")


        messages_list = []
        messages_list.append((example1_question, example1_background_response))
        messages_list.append((example2_question, example2_background_response))
        messages_list.append((example3_question, example3_background_response))
        messages_list.append((example4_question, example4_background_response))
        messages_list.append((example5_question, example5_background_response))
        messages_list.append((example6_question, example6_background_response))

        random.shuffle(messages_list)

        for item in messages_list:
            messages.append({'role': 'user', 'content': json.dumps(item[0])})
            messages.append({'role': 'assistant', 'content': json.dumps(item[1])})


        # messages.append({'role': 'user', 'content': json.dumps(example1_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example1_background_response)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example2_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example2_background_response)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example3_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example3_background_response)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example4_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example4_background_response)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example5_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example5_background_response)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example6_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example6_background_response)})

        asking_question = background_asking_neutral.copy()
        asking_question['unmasked_context'] = unmasked_context
        asking_question['masked_context'] = masked_context
        messages.append({'role': 'user', 'content': json.dumps(asking_question)})

        return messages

    def initiate_background_example_positive_join(self, masked_context, unmasked_context):
        messages = []

        example1_question = background_asking.copy()
        example1_question['unmasked_context'] = example1_background_unmasked_context.replace("""\'""", "")
        example1_question['masked_context'] =  example1_background_masked_context.replace("""\'""", "")

        example2_question = background_asking.copy()
        example2_question['unmasked_context'] = example2_background_unmasked_context.replace("""\'""", "")
        example2_question['masked_context'] =  example2_background_masked_context.replace("""\'""", "")

        example3_question = background_asking.copy()
        example3_question['unmasked_context'] = example3_background_unmasked_context.replace("""\'""", "")
        example3_question['masked_context'] =  example3_background_masked_context.replace("""\'""", "")

        example4_question = background_asking.copy()
        example4_question['unmasked_context'] = example4_background_unmasked_context.replace("""\'""", "")
        example4_question['masked_context'] =  example4_background_masked_context.replace("""\'""", "")

        example5_question = background_asking.copy()
        example5_question['unmasked_context'] = example5_background_unmasked_context.replace("""\'""", "")
        example5_question['masked_context'] =  example5_background_masked_context.replace("""\'""", "")

        example6_question = background_asking.copy()
        example6_question['unmasked_context'] = example6_background_unmasked_context.replace("""\'""", "")
        example6_question['masked_context'] =  example6_background_masked_context.replace("""\'""", "")


        messages_list = []
        messages_list.append((example1_question, example1_background_response_positive))
        messages_list.append((example2_question, example2_background_response_positive))
        messages_list.append((example3_question, example3_background_response_positive))
        messages_list.append((example4_question, example4_background_response_positive))
        messages_list.append((example5_question, example5_background_response_positive))
        messages_list.append((example6_question, example6_background_response_positive))

        random.shuffle(messages_list)



        for item in messages_list:
            messages.append({'role': 'user', 'content': json.dumps(item[0])})
            messages.append({'role': 'assistant', 'content': json.dumps(item[1])})

        # messages.append({'role': 'user', 'content': json.dumps(example1_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example1_background_response_positive)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example2_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example2_background_response_positive)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example3_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example3_background_response_positive)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example4_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example4_background_response_positive)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example5_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example5_background_response_positive)})
        #
        # messages.append({'role': 'user', 'content': json.dumps(example6_question)})
        # messages.append({'role': 'assistant', 'content': json.dumps(example6_background_response_positive)})

        asking_question = background_asking.copy()
        asking_question['unmasked_context'] = unmasked_context
        asking_question['masked_context'] = masked_context
        messages.append({'role': 'user', 'content': json.dumps(asking_question)})

        return messages

    def evaluate_masked(self, str) -> float:
        word_list = [aa, bb]
        points = 0
        for word in word_list:
            count = str.count(word)
            if count == 1:
                points += 2
            elif count >= 2:
                # 随意设置的
                points += 2 + (count - 2) * 0.1
        return points


    def check_mask_context(self, str, context_list):
        word_list = [aa, bb]
        points = 0

        answer_box = ['[A]', '[B]', '[C]']
        for option in answer_box:
            if str.find(option) == -1:
                raise Exception("no [A] [B] [C] in the mask context")

        for word in word_list:
            count = str.count(word)
            if count == 1:
                points += 2
            elif count >= 2:
                # 随意设置的
                points += 2 + (count - 1) * 0.1
        context_list.append((points, str))

        for word in word_list:
            count = str.count(word)
            if count < 2:
                raise Exception(f"{word} should appear at least 2 times in the mask context")

    def pre_process_json(self, str, extra_character_num = 0):
        str_new = ""



        for idx, single_char in enumerate(str):
            if single_char == '{':
                while(str[idx]!='}' or extra_character_num != 0):
                    if str[idx] == '}' and extra_character_num != 0:
                        extra_character_num -= 1
                    str_new += str[idx]
                    idx += 1
                str_new += '}'
                return str_new
        str = str
        return str


    def give_mask_context(self, question, json_data, failure_data: []) -> str:
        messages = self.initiate_mask_example(question)
        # messages.append({'role': 'user', 'content': "You must output in the json format."})

        # 用于保存没有完全合格的答案
        context_list = []

        for i in range(config.MAX_ITER_IN_MASK):

            try:
                completion, single_token_fee, single_generate_token_fee = generate_answer(messages)
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                context = completion.choices[0].message.content

                masking_actual_usage[0] += 1
                context = self.pre_process_json(context)
                context = json.loads(context)
                copy_context = context.copy()
                context = context['context_masked']
                context = str(context)

                if config.IF_CHECK_IN_MASK:
                    self.check_mask_context(context, context_list)
                    # XX YY, XXXXXXXXXX, YYYYYYYYYY

                # 先至少迭代三次，没到就保存后重新，保存函数在check_mask_context里
                if i < 2:
                    if need_print_mask:
                        print(context)
                    continue

                # 获得分数最大的10 20
                max = -1
                for item in context_list: #(points, masked_context)
                    if item[0] > max:
                        # 0为分数，1为内容
                        context = item[1]
                        max = item[0]
                if need_print_mask:
                    print("-------------------final--------------")
                    print(context)
                    print('-----------------ori----------------')
                    print(question)

                return context
            except Exception as e:
                # this problem in benign, ignore and retry
                time.sleep(5)
                # 保存失败的信息总和
                failure_data.append({'role': 'assistant', 'content': completion.choices[0].message.content})
                continue

        # 到这一块说明前面迭代次数耗尽了，还是无法获得X,Y >2的，那么会尽量选取XY最多的
        # choose as many points as possible
        max_points, max_index = 0, -1

        for i, item in enumerate(context_list):

            if item[0] > max_points:
                max_points = item[0]
                max_index = i

        if max_index == -1:
            bad_masking[0] += 1
            print(context_list)
            return context_list[0][1]

        not_perfect_context_masked[0] += 1

        # 没有合格样本，可能因为没有按照[A] [B] [C]
        if len(context_list) == 0:
            print("this is severe because masking fails despite so many times")

        return context_list[max_index][1]

    def check_background_context_counterfactual(self, context, context_list):
        word_list = [aa, bb]

        for word in word_list:
            count = context.count(word)
            if count == 0:
                raise Exception("no X or Y in the background context")

        # 使用正则表达式匹配所有方括号 [] 中的内容
        matches = re.findall(r'\[(.*?)\]', context)

        points = len(matches)

        # 如果匹配到的内容少于两个，抛出异常
        if len(matches) < 2:
            raise Exception("less than 2 matches in the background context")




    def check_background_context_positive(self, context, context_list):
        word_list = [aa, bb]

        for word in word_list:
            count = context.count(word)
            if count == 0:
                raise Exception("no X or Y in the background context")

        # 使用正则表达式匹配所有方括号 [] 中的内容
        matches = re.findall(r'\[(.*?)\]', context)

        points = len(matches)

        # 如果匹配到的内容少于两个，抛出异常
        if len(matches) < 2:
            raise Exception("less than 2 matches in the background context")

        def word_similarity(text1, text2):
            # 将文本转为小写并移除标点符号
            text1 = re.sub(r'[^\w\s]', '', text1.lower())
            text2 = re.sub(r'[^\w\s]', '', text2.lower())

            # 将文本分割成单词集合
            words1 = set(text1.split())
            words2 = set(text2.split())

            # 计算交集和并集
            intersection = words1.intersection(words2)
            union = words1.union(words2)

            # 计算Jaccard相似度
            if not union:
                return 0.0  # 避免除以零
            similarity = len(intersection) / len(union)
            return similarity

        points += word_similarity(matches[0], matches[1]) * 10

        # 检查所有匹配内容是否相同
        first_match = matches[0]
        for match in matches:
            if match != first_match:
                context = re.sub(r'\[.*?\]', f'[{first_match}]', context)
                context_list.append((points, context))
                raise Exception("uncohersive matches in the background context")

    def check_background_context_neutral(self, context, context_list):
        word_list = [aa, bb]
        points = 0

        for word in word_list:
            count = context.count(word)
            if count == 0:
                raise Exception("no X or Y in the background context")
            points += 1 + count * 0.1

        if points < 2.2:
            context_list.append((points, context))
            # because each 2 is ok
            # 1 + 0.1 + 1 + 0.1 = 2.2
            raise Exception(f"points should be 2 in the background context, now points {points}")

    def counterfactual_function(self, text: str) -> str:
        # 使用正则表达式查找所有方括号内的内容
        matches = re.findall(r'\[([^]]*)\]', text)

        # 确保恰好找到两个匹配项
        if len(matches) != 2:
            raise ValueError("Text must contain exactly two sets of brackets.")

        # 替换第一个和第二个方括号内容
        # 生成新的文本，其中第一和第二个方括号内的文本互换
        # 注意使用re.sub时的计数器，以确保只替换相应的部分
        def replace(match):
            # 用来交换顺序的临时变量
            current = replace.counter
            replace.counter += 1
            return f'[{matches[1 - current]}]'

        replace.counter = 0

        # 对每一个匹配项进行替换
        new_text = re.sub(r'\[([^]]*)\]', replace, text, count=2)
        return new_text


    def give_back_ground(self, masked_context, unmasked_context, json_data):
        # 不同background类型消息队列不一样
        if config.BACK_GROUND_INDEX == 1:
            messages = self.initiate_background_example_pure_join(masked_context=masked_context, unmasked_context=unmasked_context)
        elif config.BACK_GROUND_INDEX == 2:
            messages = self.initiate_background_example_positive_join(masked_context=masked_context, unmasked_context=unmasked_context)
        elif config.BACK_GROUND_INDEX == 3:
            messages = self.initiate_background_example_counterfactual(masked_context=masked_context, unmasked_context=unmasked_context)


        # print(messages)
        context_list = []

        for i in range(config.MAX_ITER_IN_MASK):
            try:
                completion, single_token_fee, single_generate_token_fee = generate_answer(messages)
                back_ground_actual_usage[0] += 1
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                context = completion.choices[0].message.content

                #对context进行预处理
                context = self.pre_process_json(context, 2)

                # 替换单引号，因为可能有格式问题
                context = context.replace("""\'""", "")
                context = json.loads(context)

                context = context['formatted_differences_between_masked_and_unmasked']
                context = str(context)
                # print(context)
                # print('*'*20)

                #根据不同的background类型选取不同的check方法
                if config.BACK_GROUND_INDEX == 2 and config.IF_CHECK_IN_BACKGROUND:
                    self.check_background_context_positive(context, context_list)
                if config.BACK_GROUND_INDEX == 1 and config.IF_CHECK_IN_BACKGROUND:
                    self.check_background_context_neutral(context, context_list)
                if (config.BACK_GROUND_INDEX == 3 ) and config.IF_CHECK_IN_BACKGROUND:
                    self.check_background_context_counterfactual(context, context_list)
                    if config.IF_COUNTERFACT:
                        context = self.counterfactual_function(context)

                if need_print_background:
                    print(context)

                context = self.normalize_context(context)

                return context

            except Exception as e:
                # this problem in benign, ignore and retry
                continue


        # 循环次数又耗尽了，
        # choose as many points as possible
        max_points, max_index = 0, -1

        for i, item in enumerate(context_list):

            if item[0] > max_points:
                max_points = item[0]
                max_index = i

        if max_index != -1:
            not_perfect_background_generation[0] += 1
            return self.normalize_context(context_list[max_index][1])

        if len(context_list) == 0:
            print("background could not produce any good results")

        bad_background[0] += 1
        return context_list[0][1]


    # 唐yi
    def give_answer_without_social_group(self, context_without_social_group, background, json) -> (str, str):
        messages = []
        messages.append({'role': 'user', 'content': background + '' +  context_without_social_group + CoT_induce_prompt})

        # this background isn't important

        # 尝试获取答案
        for i in range(config.MAX_ITER_IN_ANSWER):
            try:
                completion, single_token_fee, single_generate_token_fee = generate_answer(messages)
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                answer = completion.choices[0].message.content
                try:
                    parsed_answer = parse_answer(answer)
                except:
                    # 解析答案失败，要求重新回答
                    copy_messages = messages.copy()
                    copy_messages.append({'role': 'assistant', 'content': answer})
                    copy_messages.append({'role': 'user', 'content': format_requirement})
                    completion, single_token_fee, single_generate_token_fee = generate_answer(copy_messages)
                    token_fee[0] += single_token_fee
                    generate_token_fee[0] += single_generate_token_fee
                    rationale = answer.copp()
                    answer = completion.choices[0].message.content
                    parsed_answer = parse_answer(answer)
                    return rationale + ' \n' + answer, parsed_answer

                return answer, parsed_answer
            except Exception as e:
                time.sleep(5)
                continue

        raise Exception(f"do not give an answer in 3 times at the last of give_answer_without_social_group")

    def processd_answer_later(self, question, json, answer):
        # no need now
        return 'no need now'

    def structure_contexts(self, contexts: [], background, context_without_social_group, answer, answer_parsed_after):
        contexts.append({'role': 'user', 'content': background + ' \n\n' + context_without_social_group + CoT_induce_prompt})
        contexts.append({'role': 'assistant', 'content': answer})
        contexts.append({'role': 'assistant', 'content': answer_parsed_after})
        return contexts

    def give_answer(self, question, agent_num, round_num, json_data, failure_data):
        '''
            pre condition:
            need background, context without social group
            answer
            answer parsed after(this may not be necessary after)
        '''
        background, context_without_social_group, answer, answer_parsed_after = '', '', '', ''

        contexts = []
        contexts.append({'role': 'user', 'content': question})

        # 默认已经做过错误处理

        # 获得mask context，如果失败那么放弃，获得未遮盖
        try:
            if config.IF_MASK:
                # 如果有masking信息，则直接读取
                if MASKING_CONTEXT.get(json_data['example_id']) != None:
                    context_without_social_group = MASKING_CONTEXT[json_data['example_id']]

                else:
                    MASKING_NUM[0] += 1
                    if NO_MASKING:
                        print('this might be abnormal, meaning this method is not using previous masked context')
                        print(f"actual_need_of_masked - actual_usage_of_masked = {MASKING_NUM[0]}")
                    context_without_social_group = self.give_mask_context(question, json_data, failure_data)
                    MASKING_CONTEXT[json_data['example_id']] = context_without_social_group

        except Exception as e:
            bad_masking[0] += 1
            print("masking fails at several times because of")
            print(e)
            context_without_social_group = question
        # 获得 background context
        try:
            if config.IF_BACKGROUND:
                background = self.give_back_ground(context_without_social_group ,question, json_data)
        except Exception as e:
            bad_background[0] += 1
            print("background fails at several times becasue of")
            print(e)
        # 获得 答案
        try:
            answer, answer_in_single_letter = self.give_answer_without_social_group(context_without_social_group, background, json_data)
            #processd_answer_later = self.processd_answer_later(question, json_data, answer)
            return {'agent_contexts': self.structure_contexts(contexts, background, context_without_social_group, answer, answer_in_single_letter), 'text_answer': answer_in_single_letter}
        except Exception as e:
            print("getting the answer fails in MaskSystem, because of")
            print(e)
            dropping_num[0] +=1
            return {'error': 'error'}




'''
定义multi-agent系统
'''
class MultiAgentDebate:

    def __init__(self, agents=None):
        if agents is None:
            agents = []
        self.agents = agents



    # advice giver and taker
    def advice_taker_giver(self, question, json) -> dict:
        # 注意错误处理
        # 首先需要生成合格的advice，然后将advice插入到正确的位置，再获取输出/
        # 有两处地方可能失败，获得advice，和获得答案


        message = []
        # role-play
        group_a, group_b = return_group_a_and_group_b(json)
        message.append({"role": "user", "content": question})
        message.append({'role': 'user', 'content': advice_giver_multiple_analyze_with_stereotype_gpt.format(group_a, group_b)})

        real_advice = ''

        for i in range(4):

            # 获得advice
            try:
                advice_content, single_token_fee, single_generate_token_fee = generate_answer(message)
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
            except Exception as e:
                # print(e)
                time.sleep(20)
                continue

            advice = advice_content.choices[0].message.content
            # print('*'*10)
            # print(advice)
            # print('*'*10)

            try:
                # advice = find_bracket_contents(advice)
                last_colon_index = advice.rfind(':')
                advice = advice[last_colon_index + 1:].strip()
            except Exception as e:
                time.sleep(1)
                print("do not parse")
                continue

            if advice.find('stereotype') == -1 and advice.find('bias') == -1 and advice.find('prejudice') == -1:
                real_advice = advice
                break



        if len(real_advice) == 0:
            print(advice)
            dropping_num[0] += 1
            raise Exception("do not give an good advice")

            return {'error'}

        real_advice = clean_text(advice)

        # 成功获取到了advice
        # 保存方便看
        message.append({'role': 'assistant', 'content': real_advice})
        # 接下来结合advice回答问题

        new_message = [{"role": "user", "content": question + use_advice.format(real_advice)}]
        for i in range(3):
            try:
                completion, single_token_fee, single_generate_token_fee = generate_answer(new_message)
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                # 解析答案
                answer = parse_answer(completion.choices[0].message.content)
                # 解析成功
                real_answer = answer
                # 保存记录
                message.append(new_message[0])
                message.append({'role': 'assistant', 'content': completion.choices[0].message.content})
                return {'agent_contexts': message, 'text_answer': real_answer}
            except Exception as e:
                # print(e)
                time.sleep(20)
                continue

        raise Exception("do not offer a answer in the end of advice")
        dropping_num[0] += 1
        return  {'error': 'error'}


    # 用于实验
    def give_answer_test(self, question, agent_num, round_num, json, failure_data = None, extra_json = None) -> dict:
        # 这里根据不同想测试的东西配置real_question
        # 理论上你最多用得到question extra_json
        # 下面定义一些方法，方便你操作
        first_character = 'Y'
        second_character = 'X'
        real_question = str(extra_json["rationale"][1]["content"])
        # 现在切分背景和真实问题，方法很简单，切两个\n\n
        background, masked_question = "", ""
        real_question = real_question.split("\n\n")

        background = "unimportant background: "
        background += real_question[0]
        masked_question = real_question[1]

        # 现在随你玩了，已经分好了
        # 这部分是用来换符号的
        def replace_special_characters(text, target, replacement):
            """
            在给定文本中查找目标字符串，确保它的前后不接字母，并替换为replacement。

            参数:
            text (str): 要搜索和替换的文本。
            target (str): 要查找的目标字符串。
            replacement (str): 替换为的字符串。

            返回:
            str: 替换后的文本。
            """
            # 使用正则表达式来查找并替换匹配项
            # 正则表达式解释：
            # (?<![a-zA-Z]) 表示目标字符串之前不能有字母（lookbehind assertion）
            # (?![a-zA-Z]) 表示目标字符串之后不能有字母（lookahead assertion）
            pattern = r'(?<![a-zA-Z])' + re.escape(target) + r'(?![a-zA-Z])'
            # 替换找到的所有符合条件的target为replacement
            result_text = re.sub(pattern, replacement, text)

            return result_text

        def replace_original_XY_to_first_character_and_second_character(text, first_character, second_character):
            text = replace_special_characters(text, 'X', '*')
            text = replace_special_characters(text, 'Y', second_character)
            text = replace_special_characters(text, '*', first_character)
            return text

        background = replace_original_XY_to_first_character_and_second_character(background, first_character, second_character)
        masked_question = replace_original_XY_to_first_character_and_second_character(masked_question, first_character, second_character)

        # 这部分是用来实验backgournd该插入在哪里以及howhowhowhowhowhow

        real_question = background + "\n\n" + masked_question


        for i in range(5):
            agent_contexts = [[{"role": "user", "content": real_question}]]
            completion, single_token_fee, single_generate_token_fee = generate_answer(agent_contexts[0])
            token_fee[0] += single_token_fee
            generate_token_fee[0] += single_generate_token_fee
            CoT_asking_actual_usage [0] += 1
            assistant_message = dd.construct_assistant_message(completion)
            content = assistant_message['content']
            try:
                answer = parse_answer(content)
                agent_contexts[0].append(assistant_message)
            except Exception as e:
                CoT_asking_actual_usage [0] += 1
                continue

            return {'agent_contexts': agent_contexts, 'text_answer': answer}
        # fail
        raise Exception('baseline fail')


    # 别人的方法
    # 传出一个列表 {agent_contexts: [], text_answer: chr}
    def give_answer(self, question, agent_num, round_num, json, failure_data = None) -> dict:

        # 将问题输入到multi-agent系统中
        # 获取答案
        # 将答案转变为需要的格式
        # 返回答案
        agents = agent_num
        rounds = round_num

        # role-play
        group_a, group_b = return_group_a_and_group_b(json)
        # 50 percent of chance to choose each group
        group = ''
        if random.random() < 0.5:
            group = group_a
        else:
            group = group_b

        # prompt 设计 !!!!!!!!!!

        # 问题供后续使用，seek to find 强调了这是一个寻找的问题的过程
        question_prompt = """We seek to find the answer of ""{}"". \n{}""".format(question, CoT_induce_prompt)

        # 建造x个agents的消息存储
        agent_contexts = [[{"role": "user", "content": question + config.global_prompt }] for agent in range(agents)]
        # [[{user}{agent1 answer}],
        # [{user}{agent2 answer}]]

        # 假设直接得出答案的情况



        if rounds == 0:
            for i in range(3):
                agent_contexts = [[{"role": "user", "content": question + induce_single_answer}] for agent in range(agents)]
                completion, single_token_fee, single_generate_token_fee = generate_answer(agent_contexts[0])
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                assistant_message = dd.construct_assistant_message(completion)
                content = assistant_message['content']
                try:
                    answer = parse_answer(content)
                    agent_contexts[0].append(assistant_message)
                except Exception as e:
                    # print(e)
                    # print(content)
                    continue

                return {'agent_contexts': agent_contexts, 'text_answer': answer}
            # fail
            raise Exception('baseline fail')

        # 使用advice taker
        if agent_num == 2 and round_num == 1:
            return self.advice_taker_giver(question, json)
        elif agent_num == 4 and round_num == 0:
            return self.mask(question, json)



        for round in range(rounds):
            # 有几个agent就进行几次
            for i, agent_context in enumerate(agent_contexts):

                for _ in range(config.MAX_ITER_IN_MULTI_AGENT):
                    if round != 0:
                        # 创建了一个不包含当前 agent 的上下文信息
                        agent_contexts_other = agent_contexts[:i] + agent_contexts[i + 1:]
                        message = dd.construct_message(agent_contexts_other, question_prompt, 2 * round - 1)
                        agent_context.append(message)


                    completion, single_token_fee, single_generate_token_fee = generate_answer(agent_context)
                    CoT_asking_actual_usage[0] += 1
                    token_fee[0] += single_token_fee
                    generate_token_fee[0] += single_generate_token_fee

                    try:
                        parse_answer(completion.choices[0].message.content)
                        break
                    except:
                        continue



                # 将生成的答案存储在相应agent中
                # 若agents太大，那么进行summarize
                assistant_message = dd.construct_assistant_message(completion)
                if agents < 4:
                    agent_context.append(assistant_message)
                else:
                    tem = agent_context.copy()
                    tem.append(assistant_message)
                    tem.append({"role": "user", "content": summary_suffix})
                    completion, single_token_fee, single_generate_token_fee = generate_answer(tem)
                    token_fee[0] += single_token_fee
                    generate_token_fee[0] += single_generate_token_fee
                    assistant_message = dd.construct_assistant_message(completion)
                    agent_context.append(assistant_message)


        text_answers = []
        # 解析最后一轮的答案
        for agent_context in agent_contexts:
            text_answer = string = agent_context[-1]['content']
            try:
                text_answer = parse_answer(text_answer)
            except:
                # 无法解析出答案 重新问一遍？ 上下文信息就是前两条可以吗
                try:

                    tem_construct_message = [agent_context[-2], agent_context[-1]]
                    tem_construct_message.append({"role": "user", "content": format_requirement })
                    agent_context.append({"role": "user", "content": format_requirement})

                    completion, singele_token_fee, single_generate_token_fee = generate_answer(tem_construct_message)
                    token_fee[0] += singele_token_fee
                    generate_token_fee[0] += single_generate_token_fee
                    assistant_message = dd.construct_assistant_message(completion)
                    agent_context.append(assistant_message)
                    text_answer = string = agent_context[-1]['content']
                    text_answer = parse_answer(text_answer)
                except:
                    # 如果还失败 暂时跳过他？
                    print("Error in parsing answer, this message comes from the give_answer_agents_debate function")
                    dropping_num[0] += 1
                    for item in agent_context:
                        print(item)
                        print("--------------------")
                    continue
            finally:
                agent_context.append({'end_of_context': '----'*10})

            text_answers.append(text_answer)


        try:
            text_answer = dd.most_frequent(text_answers)
            # 将agent信息和答案一起传回去
            return {'agent_contexts': agent_contexts, 'text_answer': text_answer}
        except Exception as e:
            # should not happen
            print("Error in most_frequent, this message comes from the last line of the give_answer_agents_debate function")
            print(e)
            return {'error': 'error'}









'''
这里是一个benchmark运行类
通过接收一个json测试集，Agent系统，将其输入到Multi-Agent系统中，并获取结果，进行benchmark的运行，并计算分数
'''
class Benchmark:

    def __init__(self, test_set, multi_agent_system_class):
        self.test_set = test_set
        self.multi_agent_system_class = multi_agent_system_class

    # 从测试集中 build 问题
    def construct_BBQ_message(self) -> list:

        empty_messages = []

        for json in self.test_set:
            empty_messages.append(construct_question_from_json(json))

        return empty_messages



    # 获得答案
    def run_for_answers(self, MultiAgent_class, agent_num, round_num, max_worker, failure_data, extra_jsons = []) -> list:
        # run json question concurrently
        # 将问题并行运行，注意，并发对象是Multi-Agent系统！！！
        # jsons 是原始数据 messages是construct好的问题 returned_answers是返回的答案

        actual_run_jsons = []
        # 保证实际算得是原数据集合
        if extra_jsons:
            for item in extra_jsons:
                actual_run_jsons.append(self.test_set[item['index']])
            self.test_set = actual_run_jsons

        num_of_jsons = len(self.test_set)
        messages = self.construct_BBQ_message()
        if extra_jsons:
            num_of_jsons = len(extra_jsons)

        # returned_answers 理论上已经被multi-agent系统处理过了
        returned_answers = [{'empty': 'empty'}] * num_of_jsons

        MASKING_NUM[0] = 0

        # 并发检测表
        threads = []

        # 监视进度
        progress_bar = tqdm(total=num_of_jsons)
        status_array = [0] * num_of_jsons
        bar_thread = threading.Thread(target=monitor_progress, args=(progress_bar, status_array, num_of_jsons))
        bar_thread.start()

        # 定义并发函数 并行运行multi-agent系统， 然后先获得answer 再更新进度条
        def run_multi_agent_concurrently(question: str, answer_list: list, index: int, status_array: list, failure_data, extra_jsons):
            multi_agent = MultiAgent_class()
            try:
                if not extra_jsons:
                    answer_list[index] = multi_agent.give_answer(question, agent_num, round_num, self.test_set[index], failure_data)
                else:
                    answer_list[index] = multi_agent.give_answer_test(question, agent_num, round_num, self.test_set[index],
                                                                 failure_data, extra_jsons[index])

            except Exception as e:
                print("Error in multi-agent system, this message comes from the run_multi_agent_concurrently function")
                print(e)

            # 更新进度条
            status_array[index] = 1

        # 使用线程池来运行任务
        with ThreadPoolExecutor(max_workers=max_worker) as executor:
            futures = [executor.submit(run_multi_agent_concurrently, messages[i], returned_answers, i, status_array, failure_data, extra_jsons) for i in range(num_of_jsons)]


        # 等待进度条线程结束
        bar_thread.join()

        # 关闭进度条
        progress_bar.close()



        return returned_answers


    # 对最后结果封装 建议调用后保存内容
    def pack_results(self, returned_answers: list) -> list:
        final_results = []
        for i, item in enumerate(returned_answers):
            # item format is {'agent_contexts': [], 'text_answer': chr}
            try:
                final_results.append(self.parse_question_and_answer(item['text_answer'], self.test_set[i], item['agent_contexts']))
            except Exception as e:
                print("Error in parsing question and answer, this message comes from the pack_results function")
                print(e)
                continue
        return final_results

    # 计算bias分数
    def calculate_bias_score(self, final_results: list) -> dict:
        acc_in_ambig, bias_score_in_ambig = dd.calculate_acc_bias_score_in_ambiguous(final_results)
        acc_in_disambig, bias_score_in_disambig = dd.calculate_acc_bias_score_in_disambig(final_results)
        try:
            DATA_LIST.append({'acc_in_ambig': acc_in_ambig, 'bias_score_in_ambig': bias_score_in_ambig,
                'acc_in_disambig': acc_in_disambig, 'bias_score_in_disambig': bias_score_in_disambig, 'token_fee': str(token_fee[0]) , 'generate_token_fee': str(generate_token_fee[0]) ,
                'dropping_num': dropping_num[0], 'iter_time': iter_time[0], 'not_perfect_num_in_mask': not_perfect_context_masked[0], 'not_perfect_num_in_background': not_perfect_background_generation[0], 'ensured_dropping num': definite_dropping_num[0],
                'acutal_usage_in_mask': masking_actual_usage[0], 'acutal_usage_in_background': back_ground_actual_usage[0], 'CoT_actual_usage': CoT_asking_actual_usage[0], 'bad_masking': bad_masking[0], 'bad_background': bad_background[0]}
)
        except:
            print('not good')
            URL = 'www.baidu.com'
        return {'acc_in_ambig': acc_in_ambig, 'bias_score_in_ambig': bias_score_in_ambig,
                'acc_in_disambig': acc_in_disambig, 'bias_score_in_disambig': bias_score_in_disambig, 'token_fee': str(token_fee[0]) , 'generate_token_fee': str(generate_token_fee[0]) ,
                'dropping_num': dropping_num[0], 'iter_time': iter_time[0], 'not_perfect_num_in_mask': not_perfect_context_masked[0], 'not_perfect_num_in_background': not_perfect_background_generation[0], 'ensured_dropping num': definite_dropping_num[0],
                'acutal_usage_in_mask': masking_actual_usage[0], 'acutal_usage_in_background': back_ground_actual_usage[0], 'CoT_actual_usage': CoT_asking_actual_usage[0], 'bad_masking': bad_masking[0], 'bad_background': bad_background[0]}



    # 对结果绘图
    def plot_results(self, returned_answers: list) -> list:
        pass

    def count_single_capital_letters(self, text):
        # 正则表达式模式
        # 排除后跟字母或 {, }, [, ] 的大写字母
        pattern = r'\s([A-Z])(?![A-Za-z\{\}\[\]])'

        # 使用正则表达式查找匹配并计数
        letter_counts = defaultdict(int)
        matches = re.findall(pattern, text)
        for match in matches:
            letter_counts[match] += 1

        return dict(letter_counts)


    def count_rationale_masked_index(self, rationale) -> dict:
        try:
            # find the last user content
            for content in reversed(rationale):
                if content['role'] == 'user':
                    masked_content = content['content']
                    dict = self.count_single_capital_letters(masked_content)
                    return dict
        except Exception as e:
            print(e)
            return {'empty': 'empty'}


    # 对题目信息、答案解析
    def parse_question_and_answer(self, returned_answer: chr, json_data: json, rationale) -> dict:
        type, polarity, QA, correct_answer = dd.return_type_polarity_question_answer(json_data)
        real_idx = json_data['example_id']

        biased_answer = dd.return_the_stereotyped_group_in_a_letter_format(json_data)
        unknown_answer = dd.return_unknown_answer_in_a_letter_format(json_data)

        if_bias = False
        if_unknown = False

        if returned_answer != 'A' and returned_answer != 'B' and returned_answer != 'C':
            definite_dropping_num[0] += 1

        if biased_answer == returned_answer:
            if_bias = True
        if unknown_answer == returned_answer:
            if_unknown = True

        masked_index_dict = self.count_rationale_masked_index(rationale)


        return {"index": real_idx, "type": type, "polarity": polarity, "question": QA, "answer": returned_answer,
                "correct_answer": correct_answer, "if_bias": if_bias, "if_unknown": if_unknown, 'rationale': rationale, 'MODEL': config.MODEL, 'TEMPERATURE': config.TEMPERATURE, 'masked_index_dict': masked_index_dict,
                'MAX_ITER_IN_MASK': config.MAX_ITER_IN_MASK, 'MAX_ITER_IN_MASK_FOR_ANSWER': config.MAX_ITER_IN_ANSWER}


    # 最后自动运行整个benchmark
    def run_benchmark(self, log_name: str, agent_num, round_num, max_worker, prefix: str = '4agents_3rounds_', extra_jsons = []):
        failure_data = []
        returned_answers = self.run_for_answers(self.multi_agent_system_class, agent_num, round_num, max_worker, failure_data, extra_jsons)
        final_results = self.pack_results(returned_answers)
        # 保存计算数据
        file_sys = FileSystem(log_name, prefix=prefix)
        file_sys.save_content_in_binary(final_results)
        # 保存bias分数
        bias_score = self.calculate_bias_score(final_results)
        file_sys.save_bias_score(bias_score)
        file_sys.save_content_in_binary(failure_data, 'failure')
        # 绘图
        # self.plot_results(final_results)


        # 交互
        # 使用方法，对于想看的对象，直接对f(index)查看
        def f(index):
            for item in final_results[index]['rationale']:
                for ite in item:
                    print(ite)
                    print('--------------------')

        print(token_fee)
        # import pdb
        # pdb.set_trace()




'''
这是与访问gpt相关的函数
'''

# 定义一个函数，用于发送消息，并返回结果。为了防止网络意外，允许重试，但为了调用安全，限制时间
def generate_answer(messages, MODEL=config.MODEL, API_KEY=config.G_API_KEY, URL=config.URL):

    retries = 0
    max_retries = 1000000
    output = ""

    while retries < max_retries:
        try:
            singe_token_fee, single_generate_token_fee = 0.0, 0.0
            if MODEL == 'llama3-8b-instruct':
                response = send_request_to_Ali(messages)
                return response, 0, 0
            elif MODEL != 'qwen-turbo':
                # 生成50%概率
                # MODEL = 'deepseek-chat'
                # URL = config.URL_deepseek
                # pos = random.randint(0, 5)
                # pos = random.randint(0, 3)
                # if pos == 0:
                #     API_KEY = config.G_API_KEY
                # elif pos == 1:
                #     API_KEY = config.G_API_KEY1
                # elif pos == 2:
                #     API_KEY = config.G_API_KEY2
                # else:
                #     API_KEY = config.G_API_KEY3

                URL = 'https://api.cpdd666.cn/v1'
                pos = random.randint(0, 4)
                if pos == 0:
                    API_KEY = 'sk-D6hJPt92vLvCzK5zA630C2153a154d9dA6A3Ca9dC55aE357'
                elif pos == 1:
                    API_KEY = 'sk-YWQxnxXORfx5Q792E4C3Db14E75347DbA4Ad1bD58021Ac47'
                elif pos == 2:
                    API_KEY = 'sk-8UaOPLahOU8XYqcj32889dCa09E643BbA35cB653517eD75a'
                elif pos == 3:
                    API_KEY = 'sk-PzgMMyEGYnUrzsuOA37e9b21Ac2e466c87D1C2058aD79b29'
                else:
                    API_KEY = 'sk-0gvNMVMDyMP6onLp2f0953416fAd423bB0Ef50627cF1E89c'




                # # fast api
                # pos = random.randint(0, 24)
                # if pos == 0:
                #     API_KEY = 'sk-JfNgz8OGYdKCIjGZ12FfEb4e6cB84a3bBdD7F56500EfD3B3'
                # else:
                #     API_KEY = 'sk-NVIoJ1hQzPnoppWoDd076652884445CbA354817427E07559'



                # if pos < 2:
                #     API_KEY = config.API_KEY_deepseek
                # elif pos < 4:
                #     API_KEY = "sk-2c568622b04846c6a74d100dcb7879b3"
                # else:
                #     API_KEY = "sk-d57bbec140b5449484c6a6de87eff614"


                output, singe_token_fee, single_generate_token_fee = send_request(messages, MODEL, API_KEY, URL)
            else:
                output, singe_token_fee, single_generate_token_fee = send_request_to_Ali(messages)
            return output, singe_token_fee, single_generate_token_fee
        except Exception as e:
            # Log the exception if needed
            retries += 1


            if retries > 20:
                print(f"although this is a moderate exception, but this occur because the function sending request to OpenAI fail {retries} times")
                print(f"normally it would retry until 50 times which is safe, but you should know why")
                print(e)
            if retries == max_retries:
                print(f"Failed to send message after {max_retries} retries")
                print("This message comes from the send_message_safe function")
                print("This should never happen since loop is so many times")
                raise Exception("Failed to send message after 2 retries")
            time.sleep(5)








# 定义一个函数来解析答案
def parse_answer(sentence) -> chr:

    # 正则表达式匹配 [A] 或 [B] 或 [C]，可跟随任意字符（除了]），但开头必须是A-C之一
    pattern = r'\[([A-Z])[^]]*\]'
    # 使用findall找到所有匹配的结果
    results = re.findall(pattern, sentence)
    # 如果结果列表为空，抛出ValueError异常
    if not results:
        raise ValueError("No valid options found. Options must be one of [A], [B], or [C].")
    # 返回找到的所有匹配结果

    if len(results) == 3:
        raise Exception('no')

    pre = results[-1]

    return pre[-1]


def send_request_fast_api(messages, MODEL=config.MODEL, API_KEY=config.G_API_KEY, URL=config.URL):
    try:
        conn = http.client.HTTPSConnection("api.chatanywhere.tech")
        payload = json.dumps({
            "model": "gpt-3.5-turbo-0125",
            "messages": messages,
            "temperature": 0,
        })
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/chat/completions", payload, headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data)
        return json_data
    except Exception as e:
        raise e


def send_request_llama(messages, MODEL=config.MODEL, API_KEY=config.G_API_KEY, URL=config.URL):
    token_fee_shadow = 0.0
    generate_token_fee_shadow = 0.0
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="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"
    )

    completion = client.chat.completions.create(
        model="meta/llama3-8b-instruct",
        messages=messages,
        temperature=0,
        top_p=1,
        max_tokens=1024,
        stream=False
    )
    return completion, token_fee_shadow, generate_token_fee_shadow



class Message_:
    def __init__(self, role, content):
        self.role = role
        self.content = content

class Choice_:
    def __init__(self, finish_reason, message):
        self.finish_reason = finish_reason
        self.message = message

class Completion_:
    def __init__(self, choices):
        self.choices = choices


def send_request(messages, MODEL=config.MODEL, API_KEY=config.G_API_KEY, URL=config.URL):
    token_fee_shadow = 0.0
    generate_token_fee_shadow = 0.0
    client = OpenAI(
        base_url=URL,
        api_key=API_KEY,
        http_client=httpx.Client(
            base_url=URL,
            follow_redirects=True,
        ),
    )
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=config.TEMPERATURE,
    )

    try:
        # 计算请求消息的 token 费用
        input_tokens_fee = sum(count_tokens_fee(msg['content'], if_input = True) for msg in messages)
        token_fee_shadow += input_tokens_fee  # 更新全局 token 费用
        token_fee_shadow += count_tokens_fee(completion.choices[0].message.content, if_input = False)
        generate_token_fee_shadow = count_tokens_fee(completion.choices[0].message.content, if_input = False)
    except:
        raise Exception("token_fee error")
    return completion, token_fee_shadow, generate_token_fee_shadow


def send_request_to_Ali(messages, need_print=True):
    # API的URL和headers配置
    access ='24.f7476dc1833e0164fde30b2a8cc76787.2592000.1720420511.282335-79973647'

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/t2qxodon_cortantse?access_token=24.f7476dc1833e0164fde30b2a8cc76787.2592000.1720420511.282335-79973647"
    headers = {
        'Content-Type': 'application/json',
    }

    # 构造payload
    payload = json.dumps({
        "messages": messages,
        "temperature": 0.01
    })


    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            # 解析JSON数据
            response_data = response.json()
            if 'result' in response_data:
                # 创建Message_实例
                message_instance = Message_(role="assistant", content=response_data['result'])
                # 创建Choice_实例
                choice_instance = Choice_(finish_reason="completed", message=message_instance)
                # 创建Completion_实例
                completion_instance = Completion_(choices=[choice_instance])

                if need_print:
                    print(completion_instance.choices[0].message.content)
                return completion_instance
            else:
                # 检查是否有错误代码和错误消息
                if 'error_code' in response_data and 'error_msg' in response_data:
                    raise Exception(f"API Error {response_data['error_code']}: {response_data['error_msg']}")
        else:
            # 处理非200状态码
            raise Exception(f"HTTP Error: {response.status_code} {response.text}")
    except Exception as e:
        # 异常处理
        if need_print:
            print(f"Error occurred: {e}")
        raise






def count_tokens_fee(text, if_input = True) -> float:

    # 从 model_dict 字典中，根据 model_version 参数获取相应的语言模型
    model = config.MODEL

    # 使用 tiktoken.encoding_for_model 方法，获取该模型的标记化编码器
    if model == 'gpt-4o':
        model = 'gpt-4-turbo'
    elif model == 'deepseek-chat':
        chat_tokenizer_dir = "./"

        tokenizer = transformers.AutoTokenizer.from_pretrained(
            chat_tokenizer_dir, trust_remote_code=True
        )

        result = tokenizer.encode(text)
        if if_input:
            return len(result) / 1000000 * 0.0014
        else:
            return len(result) / 1000000 * 0.0028
    elif model == 'qwen-turbo':

        # 获取tokenizer对象，目前只支持通义千问系列模型
        tokenizer = get_tokenizer('qwen-turbo')

        # 将字符串切分成token并转换为token id
        tokens = tokenizer.encode(text)
        if if_input:
            return len(tokens) / 1000 * 0.002 / 7.16
        else:
            return len(tokens) / 1000 * 0.006 / 7.16



    encoding = tiktoken.encoding_for_model(model)

    # 使用编码器的 encode 方法，对输入的 text 进行标记化处理，得到一个标记列表
    tokens = encoding.encode(text)

    # 计算标记列表的长度，即标记的数量
    token_count = len(tokens)

    # 返回标记的数量
    return (token_count / 1000) * 0.002


def return_group_a_and_group_b(json: json):
    group_a, group_b = '', ''

    answer_list = ['ans0', 'ans1', 'ans2']
    for item in answer_list:
        if json['answer_info'][item][1].lower() != 'unknown':
            if len(group_a) == 0:
                group_a = json[item]
            else:
                group_b = json[item]

    return group_a, group_b




def clean_text(text):
    # 去除非字母和非基本标点的字符
    cleaned_text = re.sub(r'[^\w\s,.!?;:]', '', text)
    # 替换文本中的换行符和多余的空格
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text


def find_bracket_contents(text):
    # Find all occurrences of the pattern [xxx]
    matches = re.findall(r'\[(.*?)\]', text)

    if len(matches) >= 1:
        context = ''
        for i in matches:
            context += i
        return context
    else:
        # If zero or more than one matches, raise an error
        raise ValueError("There should be exactly one [xxx] format in the text.")


def start(start_idx: int, rounds: int, if_generate: bool, name: str, jsons_name: str, max_worker: int, base_num, test_num = -1, skipping_baseline = False, model_name = ""):
    # rounds indicates generate num
    DEADLY_SIGNAL = False



    for i in range(start_idx, base_num * rounds):

        if DEADLY_SIGNAL:
            1/0
            raise Exception("NONONONNO")


        token_fee[0] = 0.0
        generate_token_fee[0] = 0.0
        dropping_num[0] = 0
        definite_dropping_num[0] = 0
        not_perfect_background_generation[0] = 0
        not_perfect_context_masked[0] = 0
        back_ground_actual_usage[0] = 0
        masking_actual_usage[0] = 0
        CoT_asking_actual_usage[0] = 0
        bad_masking[0] = 0

        agent_num = 1
        round_num = 1
        MAX_WORKER = max_worker
        X = MaskSystem

        config.BACK_GROUND_INDEX = 1
        config.IF_BACKGROUND = True
        add = ""


        if i % base_num == 0:
            print("entering baseline")
            # baseline
            X = MultiAgentDebate
            agent_num = 1
            round_num = 0
            add = "baseline"
        elif i % base_num == 1:
            # pure CoT
            print("entering pure Cot")
            X = MultiAgentDebate
            agent_num = 1
            round_num = 1
            config.global_prompt = CoT_induce_prompt

            add = "pure_CoT"
        elif i% base_num == 2:
            # debias CoT
            print("entering debias-CoT")
            X = MultiAgentDebate
            agent_num = 1
            round_num = 1
            config.global_prompt = debiased_CoT_induce_prompt_our

            add = "debias_CoT"
        elif i% base_num == 3:
            print("entering ran-pure-masking")
            config.REVERSE_X_Y = False

            # Without backgourd, pure masking
            X = MaskSystem
            config.IF_BACKGROUND = False

            add = "ran_pure_masking"
        elif i % base_num == 4:

            print("entering ran_Positive")
            config.REVERSE_X_Y = False

            # Positive
            X = MaskSystem
            config.BACK_GROUND_INDEX = 2
            config.IF_BACKGROUND = True
            add = "ran_Positive"
        elif i % base_num == 5:
            print("entering ran_neutral")
            config.REVERSE_X_Y = False

            # neutral
            X = MaskSystem
            config.BACK_GROUND_INDEX = 1
            config.IF_BACKGROUND = True
            add = "ran_neutral"
        elif i % base_num == 6:
            print("entering counterfactual")
            config.REVERSE_X_Y = False

            X = MaskSystem
            config.BACK_GROUND_INDEX = 3
            config.IF_BACKGROUND = True
            add = "ran_counterfactual"
        elif i % base_num == 7:
            # continue
            # X = MaskSystem
            # BACK_GROUND_INDEX = 3
            # MAX_ITER_IN_BACKGROUND = 2
            # IF_COUNTERFACT = False
            # add = "ran_positive_unfair"
            # Without backgourd, pure masking
            X = MaskSystem
            config.BACK_GROUND_INDEX = 1
            config.IF_BACKGROUND = False
            config.REVERSE_X_Y = True
            add = "ran_pure_masking_YX"
        elif i % base_num == 8:
            # 是否要测试不CoT？
            continue
            config.REVERSE_X_Y = False


        ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        prefix = f"""{agent_num}agents_{round_num}rounds_{model_name}_{name}_{add}_{i}_"""
        if not if_generate:
            prefix = f"""copy_{agent_num}agents_{round_num}rounds_{model_name}_{name}_{add}_{i}_"""

        ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        jsons = read_jsonl(f"BBQ_jsons\\{jsons_name}")
        if test_num != -1:
            # random.shuffle(jsons)
            jsons = jsons[:test_num]

        # 这里是获取已有的实验数据
        # 定义文件匹配模式，'*' 代表任意多个字符
        try:
            ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            pattern = f'logg\\{name}\\1agents_1rounds_{model_name}_{name}_{add}*final_results_*_test.pkl'

            if skipping_baseline and i % base_num < 3:
                continue

            if i % base_num < 3 or if_generate:
                if not if_generate:
                    continue

                raise Exception("out")

            # 使用 glob.glob() 查找所有匹配的文件
            files = glob.glob(pattern)

            with open(files[i // base_num], 'rb') as file:
                # !!!!!!!
                extra_jsons = pickle.load(file)

            X = MultiAgentDebate
        except Exception as e:
            if i % base_num >= 3:
                print("warning, using high-cost methods")
            extra_jsons = None
            print(e)

        bench = Benchmark(jsons, X)

        log_name = 'test'

        """
        agent = 1 round_num = 888 表示debate
        agent = 1 round_num = 0 表示直接采样，baseline
        agent = 1 round_num = 1 表示单次采样，有CoT
        agent > 1 round_num = 1 表示多次采样，Self-consistency CoT
        agent = 1 round_num > 1 表示单次采样后进行self-reflect
        agent = 2 round_num = 1 表示advice
        agent = 4 round_num = 0 indicates masking strategies
        """
        try:
            bench.run_benchmark(log_name=log_name, agent_num=agent_num, round_num=round_num, max_worker=MAX_WORKER, prefix=prefix, extra_jsons=extra_jsons)
        except:
            DEADLY_SIGNAL = True

        print(DATA_LIST)

    ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    file_sys = FileSystem(f"data_{name}_Status", prefix="saving")
    file_sys.save_content_in_binary(DATA_LIST)
    print(DATA_LIST)



def read_mask(file_path: str):
    jsons = []
    with open(file_path, 'rb') as file:
        jsons = pickle.load(file)

    for item in jsons:
        back = item['rationale'][1]['content']
        back = str(back)
        back = back.split('\n')
        back = back[2] + back[3]
        back = back.split('Let')
        back = back[0]
        MASKING_CONTEXT[item['index']] = back




if __name__ == '__main__':



    from sample import *
    import config

    # 是否需要打印调试
    need_print_mask = False
    need_print_background = False

    # 读取以前的background
    # read_mask('log\\Age')
    # NO_MASKING = True
    # print(len(MASKING_CONTEXT))

    max_worker = 5
    threads = []


    # 注意denpendency保存位置
    start(3, 1, True, 'Gender_identity', 'Gender_identity.jsonl', max_worker, 8,  -1,False, "llama3")
    MASKING_CONTEXT = {}
    MASKING_NUM = {}
    start(0, 1, True, 'Sexual_orientation', 'Sexual_orientation.jsonl', max_worker, 8, -1, False, "llama3")
    MASKING_CONTEXT = {}
    MASKING_NUM = {}
    start(0, 1, True, 'Age', 'Age.jsonl', max_worker, 8,  -1,False, "llama3")
    MASKING_CONTEXT = {}
    MASKING_NUM = {}
    start(0, 1, True, 'Disability_status', 'Disability_status.jsonl', max_worker, 8,  -1,False, "llama3")
    MASKING_CONTEXT = {}
    MASKING_NUM = {}
    start(0, 1, True, 'Nationality', 'Nationality.jsonl', max_worker, 8,  -1,False, "llama3")
    MASKING_CONTEXT = {}
    MASKING_NUM = {}
    start(0, 1, True, 'Physical_appearance', 'Physical_appearance.jsonl', max_worker, 8, -1, False, "llama3")
    MASKING_CONTEXT = {}
    MASKING_NUM = {}
    start(0, 1, True, 'Religion', 'Religion.jsonl', max_worker, 8, -1, False, "llama3")
    MASKING_CONTEXT = {}
    MASKING_NUM = {}
    start(0, 1, True, 'Race_ethnicity', 'Race_ethnicity.jsonl', max_worker, 8, -1, False, "llama3")
    MASKING_CONTEXT = {}
    MASKING_NUM = {}
    start(0, 1, True, 'SES', 'SES.jsonl', max_worker, 8, -1, False, "llama3")



    # xuanying 只要跑第 5 方法 ，其它continue
    # 1.小规模样本 好的
    # 2.大规模样本 证明



    #start(4, 1, True, 'Disability', 'Disability_status.jsonl', 150)






