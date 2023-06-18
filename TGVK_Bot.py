from telegram.ext import CallbackContext, MessageHandler, Filters
from telegram import Update
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import threading
import logging
import vkApi
import tgApi
import commands

# <----- BOT PROGRAM SETTINGS ----->

# Multithreading: enables working on different threads, but may conflict with some libraries that should work in main thread
# !: Some functions could be run on the main thread without turning off multithreading
# !: Turn it off only if you know what you're doing
MULTITHREAD = True

# <-------------------------------->

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR, datefmt='%d-%b-%y %H:%M:%S')

# Function managing threads
def threadConltroller(info):
    commands.mainThread(info)
    if MULTITHREAD:
        thread = threading.Thread(target = commands.commandTasks, args = (info, ), name=f"{info['network'].upper()}-Thread").start()
    else: 
        commands.commandTasks(info)

def startEvent(update: Update, context: CallbackContext):
    message = update['message'].to_dict()
    info = {'network': 'tg', 
            'context': context,
            'info': message,
            'chat_id': message['chat']['id'], 
            'user_id': message['from']['id'],
            'message': message['caption'] if 'caption' in message else message['text'] if 'text' in message and 'forward_from' not in message else "",
            'photo': message['photo'] if 'photo' in message else None,
            'reply': message['reply_to_message'] if 'reply_to_message' in message else None,
            'forward': None }
    threadConltroller(info)

def core():
    try:
        start_handler = MessageHandler(Filters.all & (~Filters.command), startEvent)
        tgApi.dispatcher.add_handler(start_handler)

        for event in vkApi.longPoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW: 
                message = event.raw['object']['message']
                info = {'network': 'vk',
                        'context': None,
                        'info': event.raw,
                        'chat_id': message['peer_id'],
                        'user_id': message['from_id'],
                        'message': message['text'],
                        'photo': message['attachments'][0]['photo'] if message['attachments'] != [] and 'photo' in message['attachments'][0] else None,
                        'reply': message['reply_message'] if 'reply_message' in message else None,
                        'forward': message['fwd_messages'] if message['fwd_messages'] != [] else None }
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                callback = event.raw['object']
                info = {'network': 'vk_cb',
                        'context': None,
                        'info': event.raw,
                        'chat_id': callback['peer_id'],
                        'user_id': callback['user_id'],
                        'event_id': callback['event_id'],
                        'payload': callback['payload']}
            else: info = False

            if(info): threadConltroller(info)

    except Exception as _:
        core()

core()