import json
import os
import time
import urllib
import requests

TOKEN = "481861352:AAHC418jtyRpkSh1TLFGvk97xqHOVHX6MN0"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

COMMANDS = {"/reboot": "shutdown -r now",
            "/temp": "/opt/vc/bin/vcgencmd measure_temp > temp",
            "/cpuinfo": "less /proc/cpuinfo > cpuinfo"
            }


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            for command_name, command_value in COMMANDS.items():
                if text == command_name:
                    os.system("{}".format(command_value))
                    if (os.path.exists("./{}".format(command_name))):
                        file = open(command_name[1:])
                        file_content = file.read()
                        send_message("{}".format(file_content), chat)

        except KeyError:
            pass


# def echo_all(updates):
#     for update in updates["result"]:
#         try:
#             text = update["message"]["text"]
#             chat = update["message"]["chat"]["id"]
#             send_message(text, chat)
#         except Exception as e:
#             print(e)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    last_update_id = None
    while True:
        print("Waiting for input...")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
