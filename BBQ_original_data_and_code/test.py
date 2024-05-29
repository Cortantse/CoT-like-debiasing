"""
本文件总结

使用Agent方法来对LLM生成结果进行去偏
主要需要实现的框架如下
1、定义Agent和 Multi-Agent框架
2、将输入传入Multi-Agent的框架
4、获取答案并将其转变为需要的格式
5、使用数据集比较
"""
import random
import threading
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dashscope import get_tokenizer  # dashscope版本 >= 1.14.0
import httpx
import tiktoken
import transformers
import logging
import pickle
from dashscope import Generation

logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

from config import *
from openai import OpenAI
from tqdm import tqdm
from dependency import monitor_progress
from dependency import read_jsonl
import dependency as dd
from prompts import *
from dependency import construct_question_from_json
from dependency import FileSystem
import time
import config
import re
from collections import defaultdict

token_fee = [0.0]
generate_token_fee = [0.0]
dropping_num = [0]
not_perfect_context_masked = [0]
iter_time = [0]
dropping_num_due_to_background = [0]
not_perfect_background_generation = [0]
definite_dropping_num = [0]

masking_actual_usage = [0]
back_ground_actual_usage = [0]
CoT_asking_actual_usage = [0]

DATA_LIST = []
DEADLY_SIGNAL = False

# 改变普通CoT和debias CoT的地方
global_prompt = debiased_CoT_induce_prompt_our





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
            "task": f"{mask_prompt}",
            "attributes_involved": example1_attributes_involved,
            "step1": example1_thinking_step1,
            "step2": example1_thinking_step2,
            "context_masked": example1_context_masked,
        }

        example2_question = mask_asking.copy()
        example2_question['context'] = example2_context
        example2_anwer = {
            "context": example2_context,
            "task": f"{mask_prompt}",
            "attributes_involved": example2_attributes_involved,
            "step1": example2_thinking_step1,
            "step2": example2_thinking_step2,
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
            "task": f"{mask_prompt}",
            "attributes_involved": example4_attributes_involved,
            "step1": example4_thinking_step1,
            "step2": example4_thinking_step2,
            "context_masked": example4_context_masked,
        }

        example6_question = mask_asking.copy()
        example6_question['context'] = example6_context
        example6_anwer = {
            "context": example6_context,
            "task": f"{mask_prompt}",
            "attributes_involved": example6_attributes_involved,
            "step1": example6_thinking_step1,
            "step2": example6_thinking_step2,
            "context_masked": example6_context_masked,
        }

        example7_question = mask_asking.copy()
        example7_question['context'] = example7_context
        example7_anwer = {
            "context": example7_context,
            "task": f"{mask_prompt}",
            "attributes_involved": example7_attributes_involved,
            "step1": example7_thinking_step1,
            "step2": example7_thinking_step2,
            "context_masked": example7_context_masked,
        }

        messages_list = []
        messages_list.append((example1_question, example1_anwer))
        messages_list.append((example2_question, example2_anwer))
        messages_list.append((example4_question, example4_anwer))
        messages_list.append((example6_question, example6_anwer))
        messages_list.append((example7_question, example7_anwer))

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
        normalized_text = ' '.join(context_dict.values()).replace('[', '').replace(']', '')

        return normalized_text


    def initiate_background_example_pure_join(self, masked_context, unmasked_context):
        messages = []

        example1_question = background_asking_neutral.copy()
        example1_question['unmasked_context'] = example1_background_unmasked_context
        example1_question['masked_context'] =  example1_background_masked_context

        example2_question = background_asking_neutral.copy()
        example2_question['unmasked_context'] = example2_background_unmasked_context
        example2_question['masked_context'] =  example2_background_masked_context

        example3_question = background_asking_neutral.copy()
        example3_question['unmasked_context'] = example3_background_unmasked_context
        example3_question['masked_context'] =  example3_background_masked_context

        example4_question = background_asking_neutral.copy()
        example4_question['unmasked_context'] = example4_background_unmasked_context
        example4_question['masked_context'] =  example4_background_masked_context

        example5_question = background_asking_neutral.copy()
        example5_question['unmasked_context'] = example5_background_unmasked_context
        example5_question['masked_context'] =  example5_background_masked_context

        example6_question = background_asking_neutral.copy()
        example6_question['unmasked_context'] = example6_background_unmasked_context
        example6_question['masked_context'] =  example6_background_masked_context


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
        example1_question['unmasked_context'] = example1_background_unmasked_context
        example1_question['masked_context'] =  example1_background_masked_context

        example2_question = background_asking.copy()
        example2_question['unmasked_context'] = example2_background_unmasked_context
        example2_question['masked_context'] =  example2_background_masked_context

        example3_question = background_asking.copy()
        example3_question['unmasked_context'] = example3_background_unmasked_context
        example3_question['masked_context'] =  example3_background_masked_context

        example4_question = background_asking.copy()
        example4_question['unmasked_context'] = example4_background_unmasked_context
        example4_question['masked_context'] =  example4_background_masked_context

        example5_question = background_asking.copy()
        example5_question['unmasked_context'] = example5_background_unmasked_context
        example5_question['masked_context'] =  example5_background_masked_context

        example6_question = background_asking.copy()
        example6_question['unmasked_context'] = example6_background_unmasked_context
        example6_question['masked_context'] =  example6_background_masked_context


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


    def check_mask_context(self, str, context_list):
        word_list = ['X', 'Y']
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
                points += 2 + (count - 2) * 0.1
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
        return str


    def give_mask_context(self, question, json_data, failure_data: []) -> str:
        messages = self.initiate_mask_example(question)
        messages.append({'role': 'user', 'content': "You must output in json."})

        context_list = []

        for i in range(MAX_ITER_IN_MASK):
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
                if IF_CHECK_IN_MASK:
                    self.check_mask_context(context, context_list)

                return context
            except Exception as e:
                # this problem in benign, ignore and retry
                time.sleep(5)
                if i > 1 and MODEL == "deepseek-chat":
                    print("encounting more than 2 times of error in give_mask_context, this is a mild warning for a powerful model like deepseek-chat")
                failure_data.append({'role': 'assistant', 'content': completion.choices[0].message.content})
                continue


        # choose as many points as possible
        max_points, max_index = 0, -1

        for i, item in enumerate(context_list):

            if item[0] > max_points:
                max_points = item[0]
                max_index = i

        if max_index == -1:
            dropping_num[0] += 1
            print(context_list)
            raise Exception("do not give a mask context")

        not_perfect_context_masked[0] += 1
        return context_list[max_index][1]

    def check_background_context_positive(self, context, context_list):
        word_list = ['X', 'Y']

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
        word_list = ['X', 'Y']
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



    def give_back_ground(self, masked_context, unmasked_context, json_data):
        if BACK_GROUND_INDEX == 1:
            messages = self.initiate_background_example_pure_join(masked_context=masked_context, unmasked_context=unmasked_context)
        elif BACK_GROUND_INDEX == 2:
            messages = self.initiate_background_example_positive_join(masked_context=masked_context, unmasked_context=unmasked_context)
        else:
            raise Exception("BACK_GROUND_INDEX should be 1 or 2")

        messages.append({'role': 'user', 'content': "You must output in json."})
        # print(messages)
        context_list = []

        for i in range(MAX_ITER_IN_MASK):
            try:
                completion, single_token_fee, single_generate_token_fee = generate_answer(messages)
                back_ground_actual_usage[0] += 1
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                context = completion.choices[0].message.content
                context = self.pre_process_json(context, 2)
                context = json.loads(context)
                # print('*'*20)
                # print(masked_context)
                # print('-'*15)
                # print(unmasked_context)
                # print('-' * 10)
                # print(context)
                # print('-' * 5)
                context = context['formatted_differences_between_masked_and_unmasked']
                context = str(context)
                # print(context)
                # print('*'*20)
                if BACK_GROUND_INDEX == 2 and IF_CHECK_IN_BACKGROUND:
                    self.check_background_context_positive(context, context_list)
                if BACK_GROUND_INDEX == 1 and IF_CHECK_IN_BACKGROUND:
                    self.check_background_context_neutral(context, context_list)
                context = self.normalize_context(context)


                return context

            except Exception as e:
                # this problem in benign, ignore and retry
                print('='*10)
                print(f'This data is not good, as {e}')
                print(context)
                continue

        # choose as many points as possible
        max_points, max_index = 0, -1

        for i, item in enumerate(context_list):

            if item[0] > max_points:
                max_points = item[0]
                max_index = i

        if max_index != -1:
            not_perfect_background_generation[0] += 1
            return self.normalize_context(context_list[max_index][1])

        print("do not give a good background")
        dropping_num[0] += 1
        if BACK_GROUND_INDEX == 2:
            dropping_num_due_to_background[0] += 1
        raise Exception("no good background")



    def give_answer_without_social_group(self, context_without_social_group, background, json) -> (str, str):
        messages = []
        messages.append({'role': 'user', 'content': background + '' +  context_without_social_group + CoT_induce_prompt})

        # 尝试获取答案
        for i in range(MAX_ITER_IN_ANSWER):
            try:
                completion, single_token_fee, single_generate_token_fee = generate_answer(messages)
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                answer = completion.choices[0].message.content
                try:
                    parsed_answer = parse_answer(answer)
                except:
                    # 解析答案失败，要求重新回答
                    messages.append({'role': 'assistant', 'content': answer})
                    messages.append({'role': 'user', 'content': format_requirement})
                    completion, single_token_fee, single_generate_token_fee = generate_answer(messages)
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
        try:
            if IF_MASK:
                context_without_social_group = self.give_mask_context(question, json_data, failure_data)
            if IF_BACKGROUND:
                background = self.give_back_ground(context_without_social_group ,question, json_data)
            answer, answer_in_single_letter = self.give_answer_without_social_group(context_without_social_group, background, json_data)
            #processd_answer_later = self.processd_answer_later(question, json_data, answer)
            return {'agent_contexts': self.structure_contexts(contexts, background, context_without_social_group, answer, answer_in_single_letter), 'text_answer': answer_in_single_letter}
        except Exception as e:
            print("This error should not be reached unless the question is already out of loop, dropping it")
            print(e)
            dropping_num[0] +=1
            return {'error': 'error'}




class YourSystem:
    def __init__(self, agents=None):
        if agents is None:
            agents = []
        self.agents = agents

    def give_answer(self, question: str, agent_num, round_num, json_data, failure_data):

        messages = [{'role': 'user', 'content': question + debiased_CoT_induce_prompt_our}]

        for i in range(3):

            completion, single_token_fee, single_generate_token_fee = generate_answer(messages)
            content = completion.choices[0].message.content
            messages.append({'role': 'assistant', 'content':content})



            try:
                answer = parse_answer(content)
                return {'agent_contexts': messages, 'text_answer': answer}
            except Exception as e:
                print(e)
                continue

        raise Exception("ieabfniaebfgikae")











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
        agent_contexts = [[{"role": "user", "content": question + global_prompt }] for agent in range(agents)]
        # [[{user}{agent1 answer}],
        # [{user}{agent2 answer}]]



        # 不用管




        # 假设直接得出答案的情况
        if rounds == 0:
            for i in range(3):
                agent_contexts = [[{"role": "user", "content": question + induce_single_answer}] for agent in range(agents)]
                completion, single_token_fee, single_generate_token_fee = generate_answer(agent_contexts[0])
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                assistant_message = dd.construct_assistant_message(completion)
                agent_contexts[0].append(assistant_message)
                content = assistant_message['content']
                try:
                    answer = parse_answer(content)
                except Exception as e:
                    print(e)
                    print(content)
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

                for _ in range(MAX_ITER_IN_MULTI_AGENT):
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
    def run_for_answers(self, MultiAgent_class, agent_num, round_num, max_worker, failure_data) -> list:
        # run json question concurrently
        # 将问题并行运行，注意，并发对象是Multi-Agent系统！！！
        # jsons 是原始数据 messages是construct好的问题 returned_answers是返回的答案
        num_of_jsons = len(self.test_set)
        messages = self.construct_BBQ_message()

        # returned_answers 理论上已经被multi-agent系统处理过了
        returned_answers = [{'empty': 'empty'}] * num_of_jsons

        # 并发检测表
        threads = []

        # 监视进度
        progress_bar = tqdm(total=num_of_jsons)
        status_array = [0] * num_of_jsons
        bar_thread = threading.Thread(target=monitor_progress, args=(progress_bar, status_array, num_of_jsons))
        bar_thread.start()

        # 定义并发函数 并行运行multi-agent系统， 然后先获得answer 再更新进度条
        def run_multi_agent_concurrently(question: str, answer_list: list, index: int, status_array: list, failure_data):
            multi_agent = MultiAgent_class()
            try:
                # 决定了，你调用的什么方法
                answer_list[index] = multi_agent.give_answer(question, agent_num, round_num, self.test_set[index], failure_data)

            except Exception as e:
                print("Error in multi-agent system, this message comes from the run_multi_agent_concurrently function")
                print(e)

            # 更新进度条
            status_array[index] = 1

        # 使用线程池来运行任务
        with ThreadPoolExecutor(max_workers=max_worker) as executor:
            futures = [executor.submit(run_multi_agent_concurrently, messages[i], returned_answers, i, status_array, failure_data) for i in range(num_of_jsons)]


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
                'acutal_usage_in_mask': masking_actual_usage[0], 'acutal_usage_in_background': back_ground_actual_usage[0], 'CoT_actual_usage': CoT_asking_actual_usage[0]}
)
        except:
            print('not good')
            URL = 'www.baidu.com'
        return {'acc_in_ambig': acc_in_ambig, 'bias_score_in_ambig': bias_score_in_ambig,
                'acc_in_disambig': acc_in_disambig, 'bias_score_in_disambig': bias_score_in_disambig, 'token_fee': str(token_fee[0]) , 'generate_token_fee': str(generate_token_fee[0]) ,
                'dropping_num': dropping_num[0], 'iter_time': iter_time[0], 'not_perfect_num_in_mask': not_perfect_context_masked[0], 'not_perfect_num_in_background': not_perfect_background_generation[0], 'ensured_dropping num': definite_dropping_num[0],
                'acutal_usage_in_mask': masking_actual_usage[0], 'acutal_usage_in_background': back_ground_actual_usage[0], 'CoT_actual_usage': CoT_asking_actual_usage[0]}



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
                "correct_answer": correct_answer, "if_bias": if_bias, "if_unknown": if_unknown, 'rationale': rationale, 'MODEL': MODEL, 'TEMPERATURE': TEMPERATURE, 'masked_index_dict': masked_index_dict,
                'MAX_ITER_IN_MASK': MAX_ITER_IN_MASK, 'MAX_ITER_IN_MASK_FOR_ANSWER': MAX_ITER_IN_ANSWER}

    # 最后自动运行整个benchmark
    def run_benchmark(self, log_name: str, agent_num, round_num, max_worker, prefix: str = '4agents_3rounds_'):
        failure_data = []
        returned_answers = self.run_for_answers(self.multi_agent_system_class, agent_num, round_num, max_worker, failure_data)
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
def generate_answer(messages, MODEL=MODEL, API_KEY=G_API_KEY, URL=URL):

    retries = 0
    max_retries = 50
    output = ""

    while retries < max_retries:
        try:
            singe_token_fee, single_generate_token_fee = 0.0, 0.0
            if MODEL != 'qwen-turbo':
                # 生成50%概率
                pos = random.randint(0, 10)
                if pos == 1:
                    API_KEY = G_API_KEY1
                elif pos == 2:
                    API_KEY = G_API_KEY
                elif pos < 6:
                    API_KEY = G_API_KEY2
                else:
                    API_KEY = G_API_KEY3
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
            time.sleep(20)




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
    pre = results[0]
    for item in results:
        if item[0] != pre:
            raise ValueError("Options differ in the answer. Options must be one of [A], [B], or [C].")
        elif item[0] != 'A' and item[0] != 'B' and item[0] != 'C':
            raise ValueError("Options must be one of [A], [B], or [C].")

    return pre


def send_request(messages, MODEL=MODEL, API_KEY=G_API_KEY, URL=URL):
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
        temperature=TEMPERATURE,
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


def send_request_to_Ali(messages, need_print=False):
    token_fee_shadow = 0.0
    generate_token_fee_shadow = 0.0
    # 调用 API 获取响应
    responses = Generation.call("qwen-turbo",
                                messages=messages,
                                result_format='message',  # 设置输出为'message'格式
                                stream=False,  # 设置输出方式为流式输出
                                incremental_output=False,  # 增量式流式输出
                                api_key=G_API_KEY
                                )
    # 兼容之前的获取方式，将 responses 转换为 completion
    choices = [Choice(c['finish_reason'], Message(c['message']['role'], c['message']['content'])) for c in
               responses['output']['choices']]
    completion = Completion(choices)

    try:
        # 计算请求消息的 token 费用
        input_tokens_fee = sum(count_tokens_fee(msg['content'], if_input = True) for msg in messages)
        token_fee_shadow += input_tokens_fee  # 更新全局 token 费用
        token_fee_shadow += count_tokens_fee(completion.choices[0].message.content, if_input = False)
        generate_token_fee_shadow = count_tokens_fee(completion.choices[0].message.content, if_input = False)
    except:
        raise Exception("token_fee error")
    return completion, token_fee_shadow, generate_token_fee_shadow






def count_tokens_fee(text, if_input = True) -> float:

    # 从 model_dict 字典中，根据 model_version 参数获取相应的语言模型
    model = MODEL

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



# 用于转换
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








if __name__ == '__main__':

    # 初始化一些到时候要打印的数据
    token_fee[0] = 0.0
    generate_token_fee[0] = 0.0
    dropping_num[0] = 0
    definite_dropping_num[0] = 0
    not_perfect_background_generation[0] = 0
    not_perfect_context_masked[0] = 0
    back_ground_actual_usage[0] = 0
    masking_actual_usage[0] = 0
    CoT_asking_actual_usage[0] = 0

    # MultiAgent
    agent_num = 1
    round_num = 1
    MAX_WORKER = 100

    # 核心：这一块决定了你用的什么类，就比如说我们的方法是MaskSystem，其它一般方法都放在了Multiagentdebate
    X = MultiAgentDebate
    # X = MaskSystem
    """
    agent = 1 round_num = 888 表示debate
    agent = 1 round_num = 0 表示直接采样，baseline
    agent = 1 round_num = 1 表示单次采样，有CoT
    agent > 1 round_num = 1 表示多次采样，Self-consistency CoT
    agent = 1 round_num > 1 表示单次采样后进行self-reflect
    agent = 2 round_num = 1 表示advice
    agent = 4 round_num = 0 indicates masking strategies
    """

    BACK_GROUND_INDEX = 1
    IF_BACKGROUND = True
    add = ""



    prefix = f"""{agent_num}agents_{round_num}rounds_Age_{add}_{i}_"""


    jsons = read_jsonl("BBQ_jsons\\Age.jsonl")


    bench = Benchmark(jsons, X)

    log_name = 'test'


    bench.run_benchmark(log_name=log_name, agent_num=agent_num, round_num=round_num, max_worker=MAX_WORKER, prefix=prefix)

    print(DATA_LIST)