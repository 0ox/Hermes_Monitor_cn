import requests
import telegram
import random
import logging
import time
import re

# log handle
# logger = logging.getLogger('Hermes-Monitor-log')
# logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
#                               datefmt='%Y-%m-%d %H:%M:%S')
# fh = logging.FileHandler('Hermes-Monitor.log')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# ch.setFormatter(formatter)
# logger.addHandler(ch)
# logger.addHandler(fh)


def get_text(url):
    # Copy from your browser
    headers = {
        'user-agent': '***'
    }
    response = requests.get(url, headers=headers)
    text = response.text
    return text


def out_of_stock(bag_name):
    msg = bag_name + '未上架'
    send_message(msg)


def in_stock(num, text, bag_name):
    print('已上架')
    hrefs = re.findall('href=\"(/cn/zh/product/.*?)\"><div', text)
    file_name = bag_name + '(' + num + ').txt'
    f = open(file_name, 'a+')
    for href in hrefs:
        link = 'https://www.hermes.cn/' + href + '\n'
        f.write(link)
    f.close()
    msg = '{}第{}次链接已写入（未去重）'.format(bag_name, num)
    send_message(msg)


def send_message(msg):
    chat_id = '@***'  # Your telegram Channel name
    token = '***'  # Bot token
    bot = telegram.Bot(token=token)
    # logger.info(msg)
    bot.send_message(chat_id=chat_id, text=msg)


def main():
    key_words = ('**', '**')  # Keywords you want to monitor
    num = 1
    while True:
        for bag_name in key_words:
            url = 'https://www.hermes.cn/cn/zh/search/?s=' + bag_name + '#||'
            text = get_text(url)
            if 'Oops' in text:
                out_of_stock(bag_name)
            else:
                in_stock(num, text, bag_name)
                num += 1
            sec_link = random.randint(9, 21)
            time.sleep(sec_link)
        # Protect your ip
        sec_task = random.randint(1200, 1800)
        time.sleep(sec_task)


if __name__ == "__main__":
    main()
