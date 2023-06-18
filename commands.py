import logging
import requests
import vkApi
import tgApi
import json

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')

def saveByUrl(name, URL):
    path = "./RESOURCES/" + name
    with open(path, 'wb') as _: _.write(requests.get(URL).content)
    return path

# I'll do the same for Telegram later
def callbackVK(info):
    event_id = info['event_id']
    user_id = info['user_id']
    peer_id = info['chat_id']
    payload = info['payload']
    if '0botpage' in payload: event_data = json.dumps({"type": "open_link", "link": "https://github.com/aDamTea"}, ensure_ascii = False)
    elif '0readdocs' in payload: event_data = json.dumps({"type": "open_link", "link": "https://github.com/aDamTea/TGVK-Bot"}, ensure_ascii = False)
    return vkApi.sendCallback(event_id, user_id, peer_id, event_data)

# This is command processing fuction always working in the main thread
# In this fuction recommended to execute easy-processing commands and subprograms if it is possible
# For other commands strongly recommended to use commandTasks() function
def mainThread(info):
    return

def commandTasks(info):
    if info['network'] == 'vk_cb': return callbackVK(info)

    if info['network'] == 'vk':  network = vkApi
    else: network = tgApi
    message = info['message'].lower() if info['message'] != None else ""

    logging.info(f"[{info['network']}] CHAT_ID: ({info['chat_id']}) USER_ID: ({info['user_id']})\t - {info['message']}")

    if message in ["!hello"]:
        return network.sendMessage(id=info['chat_id'], text="Привет!", file_path=saveByUrl('image.png', 'https://i.ytimg.com/vi/IMLwb8DIksk/maxresdefault.jpg'), context=info['context'])
    elif message in ["!help"]: 
        return network.sendMessage(id=info['chat_id'], text="Слышал кому-то нужна помощь:", keyboard=network.send_help_keyboard, context=info['context'])