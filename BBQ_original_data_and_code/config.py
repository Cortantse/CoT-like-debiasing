API_KEY44 = 'sk-uIcWCOCDabGWyn4z70Ad81E746304a98922eE7D75050Fd94'
API_KEY4 = 'sk-5nYWyCJta7RrcjpuAcB126Bd05B449D38eAc10F735F0883f' # gpt4-o

MODEL = 'gpt-3.5-turbo'
MODEL2 = 'gpt-4o'

MODEL_deepseek = 'deepseek-chat'
API_KEY_deepseek = 'sk-dbfe46812522413b8a85f450bdba3525' # deep seek for simple
API_KEY3 = 'sk-644bf60b0a7f44b699a03640071750fa' # deep seek for complex

MODEL3 = 'qwen-turbo'
API_KEY33 = 'sk-966e81db7026452ebf145c625f3dbce0'

URL4444 = 'http://gtapi.xiaoerchaoren.com:8930/v1'
API_KEY333 = "sk-eZwnnHUSQKvAjLCBA539Db655a6c4f8cAfDbFd63Ed6f0dD0" # small num
API_KEY4444 = "sk-nRYt0Kt01XutBvWd611e96A8834c47BdB7F0A739F7A0F753" # old
API_KEY1 = ""
URL7 = "https://gtapi.xiaoerchaoren.com:8932/v1"
API_KEY7777 = "sk-Injj6rOQpuiBl827Cd98F0Ce03064d99825eE9D1F6356b64"

URL22 = 'https://jiekou.wlai.vip/v1'
URL_deepseek = 'https://api.deepseek.com'


URL = 'https://hk.xty.app/v1'

G_API_KEY = "sk-A0YFXovJ0KndKdqy1eE86883858c4b5c908b1aA8A22fB982"
G_API_KEY1 = "sk-S0cvUeH6nhTTkNB4C6388fF9Dc0d4e3590Ff7b5eEc8aF829"
G_API_KEY2 = "sk-gcXLegWOQUfDDeQr9d2289F69fCb4b8d97AbA45f5bB280B7"
G_API_KEY3 = "sk-HbfaQ1N1RniWcFy9387f559521Fd4eAdB22fB792Fb27C53d"





# URL = 'https://api.deepseek.com'
# API_KEY = 'sk-dbfe46812522413b8a85f450bdba3525' # deep seek for simple
# MODEL = 'deepseek-chat'

TEMPERATURE = 0

MAX_ITER_IN_MASK = 7
MAX_ITER_IN_ANSWER = 8
MAX_ITER_IN_BACKGROUND = 5
MAX_ITER_IN_MULTI_AGENT = 5

IF_MASK = True
IF_BACKGROUND = True

IF_CHECK_IN_MASK = True
IF_CHECK_IN_BACKGROUND = True

BACK_GROUND_INDEX = 1
IF_COUNTERFACT = True

REVERSE_X_Y = False

global_prompt = ""


def change():
    prompts.global_prompt = 1


if __name__ == '__main__':
    import prompts
    change()
    print(prompts.global_prompt)








