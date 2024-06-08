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
    file_path = 'log/test_final_results_20240608-220212_stereoset_result.pkl'
    # 读取数据
    with open(file_path, 'rb') as file:
        data_list = pickle.load(file)

    count = 0
    # for item in data_list:
    #     tem = item['answer']
    #     if tem != 'A' and tem != 'B' and tem != 'C':
    #         print('wrong answer exists')
    #     else:
    #         count += 1

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

    # for i in range(6):
    #     after_list.append([])
    #
    # for i, item in enumerate(list):
    #     after_list[i%6].append([item['bias_score_in_ambig'], item['acc_in_disambig'], item['acc_in_ambig']])
    #
    # for i in range(6):
    #     print(after_list[i])
    # list = [{'acc_in_ambig': 0.3521739130434783, 'bias_score_in_ambig': 0.14347826086956522, 'acc_in_disambig': 0.8510869565217392, 'bias_score_in_disambig': 0.0038610038610038533, 'token_fee': '0.8346499999999938', 'generate_token_fee': '0.032580000000000706', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5608695652173913, 'bias_score_in_ambig': 0.1282608695652174, 'acc_in_disambig': 0.8722826086956522, 'bias_score_in_disambig': -0.012145748987854255, 'token_fee': '1.7921820000000004', 'generate_token_fee': '0.956458', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 3916}, {'acc_in_ambig': 0.597574421168688, 'bias_score_in_ambig': 0.11576626240352814, 'acc_in_disambig': 0.9367502726281353, 'bias_score_in_disambig': -0.05353075170842825, 'token_fee': '1.4340760000000032', 'generate_token_fee': '0.6098419999999999', 'dropping_num': 32, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 4917}, {'acc_in_ambig': 0.5242242787152966, 'bias_score_in_ambig': 0.059880239520958056, 'acc_in_disambig': 0.8597926895799236, 'bias_score_in_disambig': -0.016018306636155555, 'token_fee': '42.681689999999925', 'generate_token_fee': '3.425664000000002', 'dropping_num': 13, 'iter_time': 0, 'not_perfect_num_in_mask': 2, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 3970, 'acutal_usage_in_background': 3693, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.2739651416122004, 'bias_score_in_ambig': -0.0038126361655773126, 'acc_in_disambig': 0.35932388222464556, 'bias_score_in_disambig': 0.02131018153117603, 'token_fee': '1.9488560000000026', 'generate_token_fee': '1.0045400000000002', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 141}, {'acc_in_ambig': 0.7940054495912806, 'bias_score_in_ambig': -0.006539509536784742, 'acc_in_disambig': 0.8911268372346217, 'bias_score_in_disambig': -0.03909348441926341, 'token_fee': '22.31414999999992', 'generate_token_fee': '2.4661740000000023', 'dropping_num': 10, 'iter_time': 0, 'not_perfect_num_in_mask': 6, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 3957, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.33042529989094876, 'bias_score_in_ambig': -0.04580152671755727, 'acc_in_disambig': 0.42529989094874593, 'bias_score_in_disambig': 0.0015151515151514694, 'token_fee': '1.908408000000003', 'generate_token_fee': '0.9995100000000031', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 140}, {'acc_in_ambig': 0.3456521739130435, 'bias_score_in_ambig': 0.13478260869565217, 'acc_in_disambig': 0.8521739130434782, 'bias_score_in_disambig': 0.010503040353786686, 'token_fee': '0.8274679999999947', 'generate_token_fee': '0.032270000000000736', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5451086956521739, 'bias_score_in_ambig': 0.11902173913043475, 'acc_in_disambig': 0.8760869565217392, 'bias_score_in_disambig': -0.037550548815713514, 'token_fee': '1.786568000000003', 'generate_token_fee': '0.9575719999999992', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 3883}, {'acc_in_ambig': 0.608529250956807, 'bias_score_in_ambig': 0.11591033351558228, 'acc_in_disambig': 0.9319542732716385, 'bias_score_in_disambig': -0.03240477544059128, 'token_fee': '1.439648000000001', 'generate_token_fee': '0.616178000000001', 'dropping_num': 14, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 4896}, {'acc_in_ambig': 0.5040783034257749, 'bias_score_in_ambig': 0.08700380641653077, 'acc_in_disambig': 0.8792165397170838, 'bias_score_in_disambig': -0.018223234624145768, 'token_fee': '42.49129199999996', 'generate_token_fee': '3.2359639999999903', 'dropping_num': 3, 'iter_time': 0, 'not_perfect_num_in_mask': 1, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 3969, 'acutal_usage_in_background': 3696, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.3385955362003266, 'bias_score_in_ambig': -0.03211758301578664, 'acc_in_disambig': 0.34967320261437906, 'bias_score_in_disambig': 0.03011583011583019, 'token_fee': '1.5661860000000063', 'generate_token_fee': '0.6320280000000031', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 107}, {'acc_in_ambig': 0.7685185185185185, 'bias_score_in_ambig': -0.0016339869281045798, 'acc_in_disambig': 0.8955386289445049, 'bias_score_in_disambig': -0.04190260475651186, 'token_fee': '22.280752000000028', 'generate_token_fee': '2.4017479999999987', 'dropping_num': 7, 'iter_time': 0, 'not_perfect_num_in_mask': 5, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 3970, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5078847199564981, 'bias_score_in_ambig': -0.04622077215878194, 'acc_in_disambig': 0.878804347826087, 'bias_score_in_disambig': -0.045892351274787524, 'token_fee': '46.95776399999994', 'generate_token_fee': '3.8727939999999736', 'dropping_num': 1, 'iter_time': 0, 'not_perfect_num_in_mask': 5, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 3945, 'acutal_usage_in_background': 3778, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.3099510603588907, 'bias_score_in_ambig': 0.16585100598151173, 'acc_in_disambig': 0.8847199564980968, 'bias_score_in_disambig': 0.0016528925619834212, 'token_fee': '0.8658279999999899', 'generate_token_fee': '0.03656600000000087', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5233695652173913, 'bias_score_in_ambig': 0.13097826086956524, 'acc_in_disambig': 0.9010869565217391, 'bias_score_in_disambig': -0.025900900900900914, 'token_fee': '1.5302959999999959', 'generate_token_fee': '0.7077100000000018', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 3848}, {'acc_in_ambig': 0.5060109289617486, 'bias_score_in_ambig': 0.11256830601092901, 'acc_in_disambig': 0.9194776931447225, 'bias_score_in_disambig': -0.02425267907501405, 'token_fee': '1.070149999999994', 'generate_token_fee': '0.34101400000000903', 'dropping_num': 12, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 4524}, {'acc_in_ambig': 0.49782608695652175, 'bias_score_in_ambig': 0.09673913043478265, 'acc_in_disambig': 0.8705114254624592, 'bias_score_in_disambig': -0.026136363636363624, 'token_fee': '42.26190999999962', 'generate_token_fee': '3.098899999999994', 'dropping_num': 3, 'iter_time': 0, 'not_perfect_num_in_mask': 1, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 3958, 'acutal_usage_in_background': 3692, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.3282442748091603, 'bias_score_in_ambig': -0.029443838604143912, 'acc_in_disambig': 0.4904632152588556, 'bias_score_in_disambig': 0.012381646030589888, 'token_fee': '1.6475800000000052', 'generate_token_fee': '0.7424800000000044', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 127}, {'acc_in_ambig': 0.6848121937942298, 'bias_score_in_ambig': 0.003810560696788208, 'acc_in_disambig': 0.9036996735582155, 'bias_score_in_disambig': -0.03977591036414563, 'token_fee': '22.03615799999994', 'generate_token_fee': '2.2605759999999964', 'dropping_num': 5, 'iter_time': 0, 'not_perfect_num_in_mask': 3, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 3964, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5095160413268081, 'bias_score_in_ambig': -0.040239260467645456, 'acc_in_disambig': 0.8771071234366503, 'bias_score_in_disambig': -0.04108047270680926, 'token_fee': '47.06672000000027', 'generate_token_fee': '3.9732780000000076', 'dropping_num': 3, 'iter_time': 0, 'not_perfect_num_in_mask': 3, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 3949, 'acutal_usage_in_background': 3775, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.34293478260869564, 'bias_score_in_ambig': 0.1255434782608695, 'acc_in_disambig': 0.8559782608695652, 'bias_score_in_disambig': 0.0022123893805310324, 'token_fee': '0.822777999999993', 'generate_token_fee': '0.0323800000000007', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 0}, {'acc_in_ambig': 0.5309782608695652, 'bias_score_in_ambig': 0.13532608695652176, 'acc_in_disambig': 0.878804347826087, 'bias_score_in_disambig': -0.04899135446685876, 'token_fee': '1.6502899999999965', 'generate_token_fee': '0.832155999999999', 'dropping_num': 0, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 3835}, {'acc_in_ambig': 0.5375754251234229, 'bias_score_in_ambig': 0.12342292923752053, 'acc_in_disambig': 0.9281828073993471, 'bias_score_in_disambig': -0.014590347923681302, 'token_fee': '1.2195839999999962', 'generate_token_fee': '0.4534660000000093', 'dropping_num': 19, 'iter_time': 0, 'not_perfect_num_in_mask': 0, 'not_perfect_num_in_background': 0, 'ensured_dropping num': 0, 'acutal_usage_in_mask': 0, 'acutal_usage_in_background': 0, 'CoT_actual_usage': 4697}]
    #
    # after_list = []
    #
    # base_num = 7
    #
    # for i in range(base_num):
    #     after_list.append([])
    #
    # for i, item in enumerate(list):
    #     after_list[i%base_num].append([item['bias_score_in_ambig'], item['acc_in_disambig'], item['acc_in_ambig']])
    #
    # for i in range(base_num):
    #     print(after_list[i])
    #     print()


    import pdb


    ## 使用须知
    ## f()函数随机取一个结果，g()函数随机取一个错误的情况
    pdb.set_trace()