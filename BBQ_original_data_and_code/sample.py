import json
import random

all_files_ = ['Nationality.jsonl', 'Religion.jsonl', 'Disability_status.jsonl', 'Sexual_orientation.jsonl',
             'Age.jsonl', 'Gender_identity.jsonl', 'Race_ethnicity.jsonl', 'SES.jsonl',
             'Physical_appearance.jsonl' ]


def sample_jsons():
    NUM_OF_FILE = 1000
    quarter = NUM_OF_FILE // 4
    ambig_neg, ambig_nonneg, disambig_neg, disambig_nonneg = quarter, quarter, quarter, quarter

    # 读取所有json文件
    jsons = []
    for file_ in all_files_:
        with open("BBQ_jsons\\" + file_, 'r') as f:
            for line in f:
                json_obj = json.loads(line.strip())
                jsons.append(json_obj)

    # 将jsons随机打乱
    random.shuffle(jsons)

    # 初始化类别字典
    categories = {
        'ambig_neg': [],
        'ambig_nonneg': [],
        'disambig_neg': [],
        'disambig_nonneg': []
    }

    # 按照类别采样
    sampled_jsons = []
    for json_obj in jsons:
        question_polarity = json_obj.get("question_polarity")
        context_condition = json_obj.get("context_condition")

        if question_polarity == "neg" and context_condition == "ambig" and len(categories['ambig_neg']) < ambig_neg:
            categories['ambig_neg'].append(json_obj)
            sampled_jsons.append(json_obj)
        elif question_polarity == "nonneg" and context_condition == "ambig" and len(
                categories['ambig_nonneg']) < ambig_nonneg:
            categories['ambig_nonneg'].append(json_obj)
            sampled_jsons.append(json_obj)
        elif question_polarity == "neg" and context_condition == "disambig" and len(
                categories['disambig_neg']) < disambig_neg:
            categories['disambig_neg'].append(json_obj)
            sampled_jsons.append(json_obj)
        elif question_polarity == "nonneg" and context_condition == "disambig" and len(
                categories['disambig_nonneg']) < disambig_nonneg:
            categories['disambig_nonneg'].append(json_obj)
            sampled_jsons.append(json_obj)

        # 检查是否所有类别都已满足数量要求
        if (len(categories['ambig_neg']) == ambig_neg and
                len(categories['ambig_nonneg']) == ambig_nonneg and
                len(categories['disambig_neg']) == disambig_neg and
                len(categories['disambig_nonneg']) == disambig_nonneg):
            break

    return sampled_jsons


if  __name__ == '__main__':
    pass
