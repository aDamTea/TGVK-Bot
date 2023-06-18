from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
import requests
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')

vkToken = 'vk1.a.Tq9IQcY2HFfKIHP6sOCPkLH3O3Sa9J60wRAjRWot6BJW_2wDEZZZIwjL5KKADvh2dN4vQ0OQiTIq_DDjaOlVFTdNzjFXxT5GA6i8PGs5k5CvdkrqsOpsWZ_H9Wrk30t42WO6rAXHIkABwlG1j2ekt_qQKt-uZ85zBgq-qVSyKOxn2F00ZZmafhRVQsynWvMKd8mliBSD-Qqov6oHw7_hqg'
vkId = 205576130
vkSession = vk_api.VkApi(token=vkToken)
apiSession = vkSession.get_api()
longPoll = VkBotLongPoll(vkSession, vkId)

def sendMessage(id, text=None, keyboard=None, file_path=None, forward=None, context=None):
    attachment = None
    if file_path != None:
        if file_path.lower().endswith(('.mp3', '.wav', '.ogg')): 
            # VK_API don't let you send voice message without saving it, so you need to select private chat to save voice before sending it to public chat.
            # To make it easy just use your ID. Type it instead of 'YOUR_ID' 
            a = vkSession.method("docs.getMessagesUploadServer", {"type": "audio_message", "peer_id": 'YOUR ID HERE' if id > 2000000000 else id, "v": "5.131"})
            b = requests.post(a['upload_url'], files={'file': open(file_path, 'rb')}).json()
            c = vkSession.method('docs.save', {"file": b['file']})['audio_message']
            attachment = "doc{}_{}".format(c["owner_id"], c["id"])
            message_type = "AUDIO"
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')): 
            a = vkSession.method("photos.getMessagesUploadServer")
            b = requests.post(a['upload_url'], files={'photo': open(file_path, 'rb')}).json()
            c = vkSession.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
            attachment = "photo{}_{}".format(c["owner_id"], c["id"])
            message_type = "PHOTO"
        else: 
            a = vkSession.method("docs.getMessagesUploadServer", {"peer_id": id, "v": "5.131"})
            b = requests.post(a['upload_url'], files={'file': open(file_path, 'rb')}).json()
            c = vkSession.method('docs.save', {"file": b['file']})['doc']
            attachment = "doc{}_{}".format(c["owner_id"], c["id"])
            message_type = "DOCUMENT"
    else: message_type = "TEXT"
    vkSession.method('messages.send', {'peer_id': id, 'message': text, 'forward': forward, "attachment": attachment, 'keyboard': keyboard, 'random_id': 0})
    logging.info(f"MESSAGE TYPE: {message_type}\t - " + (text if text != None else ""))

def sendCallback(event_id, id, peer_id, event_data):
    vkSession.method('messages.sendMessageEventAnswer', {"event_id": event_id, "user_id": id, "peer_id": peer_id, "event_data": event_data})
    logging.info("CALLBACK:\t")

# Help
keyboard_help = VkKeyboard(one_time=False, inline=True)
keyboard_help.add_callback_button(label = 'Страница разработчика', color=VkKeyboardColor.PRIMARY, payload = ['0botpage'])
keyboard_help.add_line()
keyboard_help.add_callback_button(label = 'Читать документацию', color=VkKeyboardColor.SECONDARY, payload = ['0readdocs'])
send_help_keyboard = keyboard_help.get_keyboard()