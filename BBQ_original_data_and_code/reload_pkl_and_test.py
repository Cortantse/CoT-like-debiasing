import os
import pickle
import random


def k():
    index = 0
    print(str(data_list[index]).encode('utf-8').decode("unicode_escape"))
    data_list.remove(data_list[index])
    print('--------------------')
    print('--------------------')
    print('--------------------')


def f():
    index = random.randint(0, len(data_list) - 1)
    print(str(data_list[index]).encode('utf-8').decode("unicode_escape"))
    data_list.remove(data_list[index])
    print('--------------------')
    print('--------------------')
    print('--------------------')


def g():
    loop_num = 0
    while (True):
        loop_num += 1
        if loop_num > 100 * len(data_list):
            print('no more')
            return
        index = random.randint(0, len(data_list) - 1)
        item = data_list[index]
        if item['answer'] != item['correct_answer']:
            print("this is an " + str(item['type']))
            print(str(item).encode('utf-8').decode("unicode_escape"))
            data_list.remove(data_list[index])
            print('--------------------')
            print('--------------------')
            print('--------------------')
            # 删除它
            # 下次访问
            return


if  __name__ == '__main__':
    # 文件路径
    file_path = 'log/sample_1/4agents_0rounds_filtered_with_background_1_final_results_20240525-214307_test.pkl'
    file_path2 = 'log/2agents_1rounds_sample1_positive_background_1_final_results_20240526-101345_test.pkl'
    # 读取数据
    with open(file_path, 'rb') as file:
        data_list = pickle.load(file)

    # sum_ambi = 0
    # biased_ambi = 0
    # for item in data_list:
    #     if item['type'] == 'ambig':
    #         sum_ambi += 1
    #         if item['if_bias']:
    #             biased_ambi += 1
    #
    # sum_disambig = 0
    # biased_disambig = 0
    # biased_disambig_wrong = 0
    # for item in data_list:
    #     if item['type'] == 'disambig':
    #         sum_disambig += 1
    #         if item['if_bias']:
    #             biased_disambig += 1
    #             # testing for severe bias
    #             if item['answer'] != item['correct_answer']:
    #                 biased_disambig_wrong += 1
    #
    # print(f""""sum_ambi: {sum_ambi}, biased_ambi: {biased_ambi}, biased_ambi_rate: {biased_ambi / sum_ambi}""")
    #
    # # print(f""""sum_disambi: {sum_disambig}, biased_disambi: {biased_disambig}, biased_disambi_rate: {biased_disambig/sum_disambig}""")
    #
    # print(f""""biased_disambig_wrong: {biased_disambig_wrong}, biased_disambig_wrong_rate: {biased_disambig_wrong/sum_disambig}""")

    import pdb


    ## 使用须知
    ## f()函数随机取一个结果，g()函数随机取一个错误的情况
    pdb.set_trace()