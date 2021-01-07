import os
import threading
from time import sleep
import requests
from dotenv import load_dotenv
from pathlib import Path
from commands import GET_ME, GET_UPDATES, ADDR
from queue import Queue

BASE_DIR = Path(__file__).resolve().parent
dot_env = os.path.join(BASE_DIR, '.env.sample')
load_dotenv(dotenv_path=dot_env)

TOKEN = os.getenv('TOKEN', default=None)
req_addr = 'https://api.telegram.org/bot'
# upd_offset = 304748497
# mess_bot = requests.get(req_addr + TOKEN + '/' + GET_ME)
# mess = requests.get(req_addr + TOKEN + '/' + GET_UPDATES) # + f'?offset={upd_offset}')
#
# ans = mess.json()
# print(ans)
# ans = ans['result']
#
# # print(mess.headers)
# # print(mess.status_code)
# print(mess.text)
# # print(mess_bot.text)
# # mess.raise_for_status()
# # print(mess.text)
# # print(ans)
# # for i in ans:
# #     print(i['message']['text'])
# chat_id = f'chat_id=920469995'
# text = f'&text=что хочешь, то и напиши'
#
# data = {
#     "message": {
#         "chat_id": 300793622,
#         "text": "hello!"}
#     }
#
# data_1 = {
#     "message": {
#         "chat_id": 920469995,
#         "text": "что хочешь, напиши"}
#     }
#
# # print(json.dumps(data))
#
# sending = requests.post(req_addr + TOKEN + '/' + 'sendMessage?' + chat_id + text)
# sending.raise_for_status()

messages = {}


class BotReceiver(threading.Thread):
    def __init__(self, queue):

        # self.daemon = True
        self.queue = queue
        self.offset = 0
        threading.Thread.__init__(self)

    def run(self):

        while True:
            try:
                self.new_message = requests.get(req_addr + TOKEN + '/' + GET_UPDATES + f'?offset={self.offset}')
                self.new_message = self.new_message.json()
                print(self.new_message)
                if self.new_message["result"]:
                    self.get_offset()
            except Exception as e:
                print(e)
            print(messages)
            sleep(1)

    def get_offset(self):
        self.join()
        for message in self.new_message["result"]:
            messages[message["message"]["from"]["id"]] = message["message"]["text"]
            new_offset = message["update_id"]
            if self.offset <= new_offset:
                self.offset = new_offset + 1


class BotSender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        while True:
            print('hey')
            if messages:
                for message in messages:
                    print(message)
            sleep(1)
                    # requests.post(req_addr + TOKEN + '/' + 'sendMessage?' + f'chat_id={message["id"]}' + f'&text={message}')


def main():
    queue = Queue()
    app_1 = BotReceiver(queue)
    app_1.daemon = True
    app_1.start()

    # app_2 = BotSender()
    # app_2.daemon = True
    # app_2.start()


if __name__ == '__main__':

    main()

