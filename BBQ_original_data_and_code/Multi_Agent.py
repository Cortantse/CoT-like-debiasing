"""
本文件总结

使用Agent方法来对LLM生成结果进行去偏
主要需要实现的框架如下
1、定义Agent和 Multi-Agent框架
2、将输入传入Multi-Agent的框架
4、获取答案并将其转变为需要的格式
5、使用数据集比较
"""
import threading
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import tiktoken
from config import MODEL, API_KEY, URL
from openai import OpenAI
from tqdm import tqdm
from dependency import monitor_progress
import dependency as dd
from prompts import *
from dependency import construct_question_from_json
from dependency import FileSystem
import time
import config
import re

token_fee = [0.0]
generate_token_fee = [0.0]
dropping_num = [0]
iter_time = [0]


'''
定义Agent
Agent由短期记忆、长期记忆、Tools组成

'''
class Agent:

    def __init__(self, short_memory, long_memory, tools):
        self.short_memory = short_memory
        self.long_memory = long_memory
        self.tools = tools

    def long_memory_update(self, question):
        # 将问题输入到Agent中
        # 更新长期记忆
        pass

    def use_tools(self, question):
        # 将问题输入到Agent中
        # 使用工具
        pass

    def short_memory_update(self, question):
        # 将问题输入到Agent中
        # 更新短期记忆
        pass

    def give_answer(self, question):
        # 将问题输入到Agent中
        # 获取答案
        # 将答案转变为需要的格式
        # 返回答案
        pass

class Multi_Agent_in_Single_Agent:
    def __init__(self, agents=None):
        if agents is None:
            agents = []
        self.agents = agents

    def parse_answer(self, sentence: str) -> str:
        import re
        # 匹配所有的答案框
        answer_boxes = re.findall(r'\[([A-Z])\]', sentence)
        if not answer_boxes:
            raise ValueError("No answer box found")

        # 初始化一个空列表来存储连续的ABC答案
        consecutive_answers = []

        # 从后向前检查答案框
        for answer in reversed(answer_boxes):
            if answer in 'ABC':
                consecutive_answers.append(answer)
            else:
                break  # 遇到非ABC答案，停止记录

        # 检查是否有连续的答案并且是否一致
        if not consecutive_answers or len(set(consecutive_answers)) > 1:
            raise ValueError("Invalid or inconsistent answer box sequence")

        # 如果一致，返回最后记录的答案
        return consecutive_answers[-1]


    def give_answer(self, question, tocken_fee, generate_token_fee, agent_num, round_num, json) -> dict:
        group_a, group_b = '', ''
        answer_list = ['ans0', 'ans1', 'ans2']
        for item in answer_list:
            if json['answer_info'][item][1].lower() != 'unknown':
                if len(group_a) == 0:
                    group_a = json[item]
                else:
                    group_b = json[item]
        prompt = debate_prompt.format(question, group_a, group_a, group_a, group_b, group_b, group_b, group_a, group_b)

        agent_contexts = [{"role": "user", "content": prompt}]

        for i in range(3):
            try:
                completion, single_token_fee, single_generate_token_fee = generate_answer(agent_contexts)
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                assistant_message = dd.construct_assistant_message(completion)
                # 尝试解析答案 后 成功再添加
                try:
                    answer_to_be_parsed = assistant_message['content']


                    text_answer = self.parse_answer(answer_to_be_parsed)
                    # success
                    agent_contexts.append(assistant_message)
                    return {'agent_contexts': agent_contexts, 'text_answer': text_answer}
                except Exception as e:
                    # this is common
                    iter_time[0] += 1
                    continue

            except Exception as e:
                print("Error in having completion, this message comes from the give_answer_agents_debate function")
                print(e)
                time.sleep(20)
                continue

        dropping_num[0] += 1




'''
定义multi-agent系统
'''
class MultiAgentDebate:

    def __init__(self, agents=None):
        if agents is None:
            agents = []
        self.agents = agents


    # 别人的方法
    # 传出一个列表 {agent_contexts: [], text_answer: chr}
    def give_answer(self, question, tocken_fee, generate_token_fee, agent_num, round_num, json) -> dict:

        # 将问题输入到multi-agent系统中
        # 获取答案
        # 将答案转变为需要的格式
        # 返回答案
        agents = agent_num
        rounds = round_num

        # prompt 设计 !!!!!!!!!!

        # 问题供后续使用，seek to find 强调了这是一个寻找的问题的过程
        question_prompt = """We seek to find the answer of ""{}"". \n{}""".format(question, CoT_induce_prompt + no_short_cut )

        # 建造x个agents的消息存储
        agent_contexts = [[{"role": "user", "content": question + Based_on_context_prompt }] for agent in range(agents)]
        # [[{user}{agent1 answer}],
        # [{user}{agent2 answer}]]

        # 假设直接得出答案的情况
        if rounds == 0:
            agent_contexts = [[{"role": "user", "content": question + induce_single_answer}] for agent in range(agents)]
            completion, single_token_fee, single_generate_token_fee = generate_answer(agent_contexts[0])
            token_fee[0] += single_token_fee
            generate_token_fee[0] += single_generate_token_fee
            assistant_message = dd.construct_assistant_message(completion)
            agent_contexts[0].append(assistant_message)




        for round in range(rounds):
            # 有几个agent就进行几次
            for i, agent_context in enumerate(agent_contexts):

                if round != 0:
                    # 创建了一个不包含当前 agent 的上下文信息
                    agent_contexts_other = agent_contexts[:i] + agent_contexts[i + 1:]
                    message = dd.construct_message(agent_contexts_other, question_prompt, 2 * round - 1)
                    agent_context.append(message)


                completion, single_token_fee, single_generate_token_fee = generate_answer(agent_context)
                token_fee[0] += single_token_fee
                generate_token_fee[0] += single_generate_token_fee
                # 将生成的答案存储在相应agent中
                # 若agents太大，那么进行summarize
                assistant_message = dd.construct_assistant_message(completion)
                print(assistant_message)
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
    def run_for_answers(self, MultiAgent_class, agent_num, round_num, max_worker) -> list:
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
        def run_multi_agent_concurrently(question: str, answer_list: list, index: int, status_array: list):
            multi_agent = MultiAgent_class()
            try:
                answer_list[index] = multi_agent.give_answer(question, token_fee, generate_token_fee, agent_num, round_num, self.test_set[index])

            except Exception as e:
                print("Error in multi-agent system, this message comes from the run_multi_agent_concurrently function")
                print(e)

            # 更新进度条
            status_array[index] = 1

        # 使用线程池来运行任务
        with ThreadPoolExecutor(max_workers=max_worker) as executor:
            futures = [executor.submit(run_multi_agent_concurrently, messages[i], returned_answers, i, status_array) for i in range(num_of_jsons)]


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
        return {'acc_in_ambig': acc_in_ambig, 'bias_score_in_ambig': bias_score_in_ambig,
                'acc_in_disambig': acc_in_disambig, 'bias_score_in_disambig': bias_score_in_disambig, 'token_fee': str(token_fee[0]) , 'generate_token_fee': str(generate_token_fee[0]) ,
                'dropping_num': dropping_num[0], 'iter_time': iter_time[0]}


    # 对结果绘图
    def plot_results(self, returned_answers: list) -> list:
        pass

    # 对题目信息、答案解析
    def parse_question_and_answer(self, returned_answer: chr, json_data: json, rationale) -> dict:
        type, polarity, QA, correct_answer = dd.return_type_polarity_question_answer(json_data)
        real_idx = json_data['example_id']

        biased_answer = dd.return_the_stereotyped_group_in_a_letter_format(json_data)
        unknown_answer = dd.return_unknown_answer_in_a_letter_format(json_data)

        if_bias = False
        if_unknown = False

        if biased_answer == returned_answer:
            if_bias = True
        if unknown_answer == returned_answer:
            if_unknown = True

        return {"index": real_idx, "type": type, "polarity": polarity, "question": QA, "answer": returned_answer,
                "correct_answer": correct_answer, "if_bias": if_bias, "if_unknown": if_unknown, 'rationale': rationale}

    # 最后自动运行整个benchmark
    def run_benchmark(self, log_name: str, agent_num, round_num, max_worker, prefix: str = '4agents_3rounds_'):
        returned_answers = self.run_for_answers(self.multi_agent_system_class, agent_num, round_num, max_worker)
        final_results = self.pack_results(returned_answers)
        # 保存计算数据
        file_sys = FileSystem(log_name, prefix=prefix)
        file_sys.save_content_in_binary(final_results)
        # 保存bias分数
        bias_score = self.calculate_bias_score(final_results)
        file_sys.save_bias_score(bias_score)
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
        import pdb
        pdb.set_trace()




'''
这是与访问gpt相关的函数
'''

# 定义一个函数，用于发送消息，并返回结果。为了防止网络意外，允许重试，但为了调用安全，限制时间
def generate_answer(messages):

    retries = 0
    max_retries = 2
    output = ""

    while retries < max_retries:
        try:
            output, singe_token_fee, single_generate_token_fee = send_request(messages)
            return output, singe_token_fee, single_generate_token_fee
        except Exception as e:
            # Log the exception if needed
            retries += 1
            time.sleep(2)
            print(f"Exception occur in generate_answer function, with exception {e}")

    if retries >= max_retries:
        print(f"Failed to send message after {max_retries} retries")
        print("This message comes from the send_message_safe function")

    raise Exception("Failed to send message after 2 retries")


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


def send_request(messages, need_print=False):
    token_fee = 0.0
    generate_token_fee = 0.0
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
        temperature=0.7
    )
    if need_print:
        print(completion.choices[0].message.content)
        # print("The length of the rationale is: ", str(len(completion.choices[0].message.content)))
    try:
        # 计算请求消息的 token 费用
        input_tokens_fee = sum(count_tokens_fee(msg['content']) for msg in messages)
        token_fee += input_tokens_fee  # 更新全局 token 费用
        token_fee += count_tokens_fee(completion.choices[0].message.content)
        generate_token_fee = count_tokens_fee(completion.choices[0].message.content)
    except:
        raise Exception("tocken_fee error")
    return completion, token_fee, generate_token_fee



def count_tokens_fee(text) -> float:

    # 从 model_dict 字典中，根据 model_version 参数获取相应的语言模型
    model = MODEL

    # 使用 tiktoken.encoding_for_model 方法，获取该模型的标记化编码器
    encoding = tiktoken.encoding_for_model(model)

    # 使用编码器的 encode 方法，对输入的 text 进行标记化处理，得到一个标记列表
    tokens = encoding.encode(text)

    # 计算标记列表的长度，即标记的数量
    token_count = len(tokens)

    # 返回标记的数量
    return (token_count / 1000) * 0.002



if __name__ == '__main__':
    file = 'BBQ_jsons/mixed_sample_on_mixed_sample_raw.jsonl'

    jsons = dd.read_jsonl(file)
    jsons = jsons[:1000]
    bench = Benchmark(jsons, MultiAgentDebate)

    agent_num = 1
    round_num = 1
    MAX_WORKER = 130
    prefix = f"""{agent_num}agents_{round_num}rounds_based_on_context"""
    log_name = 'test'

    """
    agent = 1 round_num = 888 表示debate
    agent = 1 round_num = 0 表示直接采样，无CoT
    agent = 1 round_num = 1 表示单次采样，有CoT
    agent > 1 round_num = 1 表示多次采样，Self-consistency CoT
    agent = 1 round_num > 1 表示单次采样后进行self-reflect
    """

    bench.run_benchmark(log_name=log_name, agent_num=agent_num, round_num=round_num, max_worker=MAX_WORKER, prefix=prefix)

