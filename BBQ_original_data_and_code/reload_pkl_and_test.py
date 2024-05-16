import os
import pickle
import random

if  __name__ == '__main__':
    # 文件路径
    file_path = 'log/1agents_1rounds_based_on_contextfinal_results_20240516-112503_test.pkl'

    # 读取数据
    with open(file_path, 'rb') as file:
        data_list = pickle.load(file)

    print(data_list[0])
    sum_ambi = 0
    biased_ambi = 0
    for item in data_list:
        if item['type'] == 'ambig':
            sum_ambi += 1
            if item['if_bias']:
                biased_ambi += 1

    sum_disambig = 0
    biased_disambig = 0
    biased_disambig_wrong = 0
    for item in data_list:
        if item['type'] == 'disambig':
            sum_disambig += 1
            if item['if_bias']:
                biased_disambig += 1
                # testing for severe bias
                if item['answer'] != item['correct_answer']:
                    biased_disambig_wrong += 1

    print(f""""sum_ambi: {sum_ambi}, biased_ambi: {biased_ambi}, biased_ambi_rate: {biased_ambi / sum_ambi}""")

    # print(f""""sum_disambi: {sum_disambig}, biased_disambi: {biased_disambig}, biased_disambi_rate: {biased_disambig/sum_disambig}""")

    print(f""""biased_disambig_wrong: {biased_disambig_wrong}, biased_disambig_wrong_rate: {biased_disambig_wrong/sum_disambig}""")

    import pdb


    def f():
        index = random.randint(0, len(data_list) - 1)
        print(str(data_list[index]).encode('utf-8').decode("unicode_escape"))
        data_list.remove(data_list[index])
        print('--------------------')
        print('--------------------')
        print('--------------------')


    def g():
        for item in data_list:
            if item['answer'] != item['correct_answer']:
                print("this is an " + str(item['type']))
                for ite in item['rationale']:
                    print(ite)
                    print('--------------------')
                # 删除它
                data_list.remove(item)
                # 下次访问
                return






    pdb.set_trace()