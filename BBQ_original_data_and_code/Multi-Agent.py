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

from tqdm import tqdm

from BBQ_original_data_and_code.main import monitor_progress

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



'''
定义multi-agent系统
'''
class MultiAgent:

    def __init__(self, agents: list = []):
        self.agents = agents

    def give_answer(self, question):
        # 将问题输入到multi-agent系统中
        # 获取答案
        # 将答案转变为需要的格式
        # 返回答案
        pass



'''
定义一个文件系统类，方便快速写入实验的数据
'''
class FileSystem:

    def __init__(self, file_name):
        self.file_name = file_name

    # 定义一个函数 用于对特定文件名打开（或者创建） 然后向该文件加入内容
    def add_content(self, content, file_name):
        pass





'''
这里是一个benchmark运行类
通过接收一个json测试集，Agent系统，将其输入到Multi-Agent系统中，并获取结果，进行benchmark的运行，并计算分数
'''
class Benchmark:

    def __init__(self, test_set, agent_system: Agent, multi_agent_system: MultiAgent):
        self.test_set = test_set
        self.agent_system = agent_system
        self.multi_agent_system = multi_agent_system

    # 从测试集中 build 问题
    def construct_BBQ_message(self) -> list:
        empty_messages = []

        for json in self.test_set:
            empty_messages.append(api.return_prompt(json))

        return empty_messages




    # 运行benchmark
    def run_for_answers(self) -> list:
        # run json question concurrently
        # 将问题并行运行，注意，并发对象是Multi-Agent系统！！！
        # jsons 是原始数据 messages是construct好的问题 returned_answers是返回的答案
        num_of_jsons = len(self.test_set)
        messages = self.construct_BBQ_message()

        # returned_answers 理论上已经被multi-agent系统处理过了
        returned_answers = [''] * num_of_jsons

        # 并发检测表
        threads = []

        # 监视进度
        progress_bar = tqdm(total=num_of_jsons)
        status_array = [0] * num_of_jsons
        bar_thread = threading.Thread(target=monitor_progress, args=(progress_bar, status_array, num_of_jsons))
        bar_thread.start()




        # 定义并发函数 并行运行multi-agent系统， 然后先获得answer 再更新进度条
        def run_multi_agent_concurrently(question: str, answer_list: list, index: int, status_array: list):
            multi_agent = MultiAgent()
            try:
                answer_list[index] = multi_agent.give_answer(question)

            except Exception as e:
                print("Error in multi-agent system, this message comes from the run_multi_agent_concurrently function")
                print(e)

            # 更新进度条
            status_array[index] = 1




        for i in range(num_of_jsons):

            # 定义一个线程，并将其添加到线程列表中
            thread = threading.Thread(target=run_multi_agent_concurrently, args=(messages[i], returned_answers, i, status_array))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 关闭进度条
        progress_bar.close()

        # 返回答案
        return returned_answers


    # 判断结果的正确与否
    def check_correctness(self, returned_answers: list) -> list:
        pass

    # 计算bias分数
    def calculate_bias_score(self, returned_answers: list) -> list:
        pass

    # 对结果绘图
    def plot_results(self, returned_answers: list) -> list:
        pass




'''
这是与访问gpt相关的函数
'''
import API as api
import time
# 定义一个函数，用于发送消息，并返回结果。为了防止网络意外，允许重试，但为了调用安全，限制时间
def send_message_safe(messages) -> str:
    retries = 0
    max_retries = 2
    output = ""

    while retries < max_retries:
        try:
            output = api.send_request(messages)

        except Exception as e:
            # Log the exception if needed
            retries += 1
            time.sleep(2)

        finally:
            return output

    if retries >= max_retries:
        print(f"Failed to send message after {max_retries} retries")
        print("This message comes from the send_message_safe function")

    return output





