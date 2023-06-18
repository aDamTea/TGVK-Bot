# Telegram-Vkontakte Python Bot
This is bot template that works with Telegram and VK with multithreading. 
Used libraries:
* [python-telegram-bot==13.15](https://github.com/python-telegram-bot/python-telegram-bot) <sub>To be upgraded soon</sub>
* [vk-api](https://github.com/python273/vk_api) <sub>Maybe I'll use vkbottle in other version, but I'm not so into async now</sub>

## How to add commands
You can add text commands and keyboard. 
<br><br>
Adding text command (how i do it):
```
if message in ['your', 'commands', 'here']:
     sendMessage(id=info['chat_id'], 
                 text="your response", 
                 context=info['context'])
```
Or complex commands like that:
```
if message.split()[0] in ['!say']: # For example
    sendMessage(id=info['chat_id'], 
                text=message.split()[1:], 
                context=info['context'])
```
Every time use ```context=info['context']``` to be able to work with Telegram API.<br>
All command recommended to write in ```commandTasks()``` function for multithreading, but if you need to run your module in the main thread use ```mainThread()``` function.<br>
Keyboards should be written in ```vkApi``` and ```tgApi``` modules (if you know how to do it of course), examples included.

## Collected message information
All information that is collected from message is storaged in ```info``` dict:<br>
+ ```info['network']``` - where we've recieved message ```'tg'``` or ```'vk'```
+ ```info['context']``` - is used for Telegram API ```sendMessage()``` function
+ ```info['info']``` - raw information of event for those who know how to use it
+ ```info['chat_id']``` - id of chat frow where we've recieved message
+ ```info['user_id']``` - id of user that sent message. Equals ```info['chat_id']``` in private chat
+ ```info['message']``` - message text. ```""``` if there is no text
+ ```info['photo']``` - photos that are in message.  ```None``` if there is no photos
+ ```info['reply']``` - raw information of replied message
+ ```info['forward']``` - **ONLY FOR VK** - raw information of forwarded message

## To do
+ Use async libraries as: python-telegram-bot==20.3 and [vkbottle](https://github.com/vkbottle/vkbottle)
+ Add user information in ```info``` dict
+ <sub>Maybe GUI?</sub>
