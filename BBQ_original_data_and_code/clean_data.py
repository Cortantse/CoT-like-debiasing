import http.client
import json
import re
import config
if __name__ == '__main__':
    from Multi_Agent import send_request_fast_api


    print(send_request_fast_api([{'role': 'user', 'content': 'Hi'}]).choices[0].message.content)