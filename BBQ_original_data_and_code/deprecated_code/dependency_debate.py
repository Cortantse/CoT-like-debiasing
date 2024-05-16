import pickle
import time

import numpy as np
from tqdm import tqdm

import API as api


def generate_answer(messages):
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


def construct_message(agents, question, idx):

    # Use introspection in the case in which there are no other agents.
    if len(agents) == 0:
        return {"role": "user", "content": "Can you verify that your answer is correct. Please reiterate your answer, making sure to state your answer at the end of the response."}

    prefix_string = "These are the recent/updated opinions from other agents: "

    for agent in agents:
        agent_response = agent[idx]["content"]
        response = "\n\n One agent response: ```{}```".format(agent_response)

        prefix_string = prefix_string + response

    prefix_string = prefix_string + "\n\n Use these opinions carefully as additional advice, can you provide an updated answer? Make sure to state your answer at the end of the response.".format(question)
    return {"role": "user", "content": prefix_string}


def construct_assistant_message(completion):
    content = completion["choices"][0]["message"]["content"]
    return {"role": "assistant", "content": content}

def parse_answer(sentence):
    parts = sentence.split(" ")

    for part in parts[::-1]:
        try:
            answer = float(part)
            return answer
        except:
            continue


def most_frequent(List) -> chr:
    counter = 0
    ch = List[0]

    for item in List:
        current_frequency = List.count(item)
        if current_frequency > counter:
            counter = current_frequency
            ch = item

    return ch


if __name__ == "__main__":
    answer = parse_answer("My answer is the same as the other agents and AI language model: the result of 12+28*19+6 is 550.")

    agents = 2
    rounds = 3
    np.random.seed(0)

    evaluation_round = 100
    scores = []

    generated_description = {}

    for round in tqdm(range(evaluation_round)):
        a, b, c, d, e, f = np.random.randint(0, 30, size=6)

        answer = a + b * c + d - e * f
        # 建造x个agents的消息存储
        agent_contexts = [[{"role": "user", "content": """What is the result of {}+{}*{}+{}-{}*{}? Make sure to state your answer at the end of the response.""".format(a, b, c, d, e, f)}] for agent in range(agents)]
        # [[{user}{agent1 answer}],
        # [{user}{agent2 answer}]]

        # 问题供后续使用，seek to find 强调了这是一个寻找的问题的过程
        question_prompt = "We seek to find the result of {}+{}*{}+{}-{}*{}?".format(a, b, c, d, e, f)

        for round in range(rounds):
            # 有几个agent就进行几次
            for i, agent_context in enumerate(agent_contexts):

                if round != 0:
                    # 创建了一个不包含当前 agent 的上下文信息
                    agent_contexts_other = agent_contexts[:i] + agent_contexts[i+1:]
                    message = construct_message(agent_contexts_other, question_prompt, 2*round - 1)
                    agent_context.append(message)

                    print("message: ", message)

                completion = generate_answer(agent_context)
                # 将生成的答案存储在相应agent中
                assistant_message = construct_assistant_message(completion)
                agent_context.append(assistant_message)
                # print(completion)

        text_answers = []

        for agent_context in agent_contexts:
            text_answer = string =  agent_context[-1]['content']
            text_answer = text_answer.replace(",", ".")
            text_answer = parse_answer(text_answer)

            if text_answer is None:
                continue

            text_answers.append(text_answer)

        generated_description[(a, b, c, d, e, f)] = (agent_contexts, answer)

        try:
            text_answer = most_frequent(text_answers)
            if text_answer == answer:
                scores.append(1)
            else:
                scores.append(0)
        except:
            continue

        print("performance:", np.mean(scores), np.std(scores) / (len(scores) ** 0.5))

    pickle.dump(generated_description, open("math_agents{}_rounds{}.p".format(agents, rounds), "wb"))
    import pdb
    pdb.set_trace()
    print(answer)
    print(agent_context)



