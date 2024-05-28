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
    file_path5 = 'log/sample_1/4agents_0rounds_filtered_with_background_1_final_results_20240525-214307_test.pkl'
    file_path = 'log/1agents_1rounds_Age_pure_CoT_1_final_results_20240527-231908_test.pkl'
    # 读取数据
    with open(file_path, 'rb') as file:
        data_list = pickle.load(file)

    count = 0
    for item in data_list:
        tem = item['answer']
        if tem != 'A' and tem != 'B' and tem != 'C':
            raise Exception('wrong answer exists')
        else:
            count += 1

    print(count)

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

    list = [{'acc_in_ambig': 0.33369565217391306, 'bias_score_in_ambig': 0.10652173913043472, 'acc_in_disambig': 0.8543478260869565, 'bias_score_in_disambig': -0.009977827050997812, 'token_fee': '0.829409999999994', 'generate_token_fee': '0.03294200000000072', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5103260869565217, 'bias_score_in_ambig': 0.1353260869565218, 'acc_in_disambig': 0.8694942903752039, 'bias_score_in_disambig': -0.030724637681159406, 'token_fee': '2.629770000000003', 'generate_token_fee': '1.450274', 'dropping_num': 1, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 4866}, {'acc_in_ambig': 0.6991294885745375, 'bias_score_in_ambig': 0.023394994559303595, 'acc_in_disambig': 0.6010869565217392, 'bias_score_in_disambig': -0.05157813702848346, 'token_fee': '3.2933459999999926', 'generate_token_fee': '1.9817080000000016', 'dropping_num': 2, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 4570}, {'acc_in_ambig': 0.5290918977705275, 'bias_score_in_ambig': 0.05111473626971176, 'acc_in_disambig': 0.8058727569331158, 'bias_score_in_disambig': -0.042665108123904116, 'token_fee': '59.10240399999995', 'generate_token_fee': '6.326658000000047', 'dropping_num': 2, 'iter_time': 0, 'not_perfect_num_in_mask': 20, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 4484, 'acutal_usage_in_background': 3728, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5958605664488017, 'bias_score_in_ambig': 0.05991285403050111, 'acc_in_disambig': 0.8194217130387343, 'bias_score_in_disambig': -0.020576131687242816, 'token_fee': '106.58965800000064', 'generate_token_fee': '8.167984000000022', 'dropping_num': 11, 'iter_time': 0, 'not_perfect_num_in_mask': 25, 'not_perfect_num_in_background': 1331, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 4424, 'acutal_usage_in_background': 11074, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.641653072321914, 'bias_score_in_ambig': -0.00924415443175638, 'acc_in_disambig': 0.833968426782798, 'bias_score_in_disambig': -0.04207492795389045, 'token_fee': '38.60442999999985', 'generate_token_fee': '5.353521999999912', 'dropping_num': 4, 'iter_time': 0, 'not_perfect_num_in_mask': 19, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 4463, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.34891304347826085, 'bias_score_in_ambig': 0.12717391304347833, 'acc_in_disambig': 0.8521739130434782, 'bias_score_in_disambig': 0.01603095632946383, 'token_fee': '0.825833999999992', 'generate_token_fee': '0.032502000000000676', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5222826086956521, 'bias_score_in_ambig': 0.1483695652173913, 'acc_in_disambig': 0.8728260869565218, 'bias_score_in_disambig': -0.036311239193083544, 'token_fee': '2.5620639999999986', 'generate_token_fee': '1.4201959999999978', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 4796}, {'acc_in_ambig': 0.6982055464926591, 'bias_score_in_ambig': 0.03425774877650895, 'acc_in_disambig': 0.6010869565217392, 'bias_score_in_disambig': -0.03410852713178292, 'token_fee': '3.302597999999997', 'generate_token_fee': '1.9995519999999993', 'dropping_num': 1, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 4588}, {'acc_in_ambig': 0.514161220043573, 'bias_score_in_ambig': 0.058823529411764656, 'acc_in_disambig': 0.8111050626020686, 'bias_score_in_disambig': -0.03660662405578152, 'token_fee': '58.711437999999994', 'generate_token_fee': '6.389158', 'dropping_num': 7, 'iter_time': 0, 'not_perfect_num_in_mask': 13, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 4420, 'acutal_usage_in_background': 3723, 'CoT_actual_usage': 0}]
    after_list = []

    for i in range(6):
        after_list.append([])

    for i, item in enumerate(list):
        after_list[i%6].append([item['bias_score_in_ambig'], item['acc_in_disambig'], item['acc_in_ambig']])

    for i in range(6):
        print(after_list[i])

    import pdb


    ## 使用须知
    ## f()函数随机取一个结果，g()函数随机取一个错误的情况
    pdb.set_trace()