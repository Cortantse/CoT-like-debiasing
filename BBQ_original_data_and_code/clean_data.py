import glob
import pickle

def return_idx_jsons(jsons: list, idx: int):
    for item in jsons:
        if item['example_id'] == idx:
            return item
    print(f"requesting idx: {idx}")
    raise Exception("not found")




if __name__ == '__main__':
    # from dependency import read_jsonl
    #
    # jsons = read_jsonl('BBQ_jsons\\Age.jsonl')
    #
    # method = "ran_Positive"
    #
    # pattern = f'log\\1agents_1rounds_Age_{method}*final_results_*_test.pkl'
    #
    # # 使用 glob.glob() 查找所有匹配的文件
    # files = glob.glob(pattern)
    #
    # pattern = f'log\\Age\\1agents_1rounds_Age_{method}*final_results_*_test.pkl'
    #
    # files_ori = glob.glob(pattern)
    #
    # for i in range(len(files_ori)):
    #     with open(files_ori[i], 'rb') as file_1:
    #         extra_jsons = pickle.load(file_1)
    #
    #     with open(files[i], 'rb') as file_2:
    #         extra_jsons_2 = pickle.load(file_2)
    #
    #     print(len(extra_jsons_2), len(extra_jsons))
    #
    # from Multi_Agent import Benchmark
    # b = Benchmark(jsons, None)
    #
    # print(len(files))
    #
    # for file_path in files:
    #     with open(file_path, 'rb') as file:
    #         extra_jsons = pickle.load(file)
    #
    #     answers = []
    #     corr_jsons = []
    #
    #     b.parse_question_and_answer()
    import config
    print(config.BACK_GROUND_INDEX)
    config.BACK_GROUND_INDEX = 2
    print(config.BACK_GROUND_INDEX)




