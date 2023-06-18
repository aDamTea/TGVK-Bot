from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext
import logging

tgToken = 'YOUR_TOKEN'
tgSession = Updater(token=tgToken, use_context=True)
dispatcher = tgSession.dispatcher
tgSession.start_polling()

def sendMessage(id, context: CallbackContext, text=None, keyboard=None, file_path=None, forward=None):
    photo = False
    if file_path != None:
        if file_path.lower().endswith(('.mp3', '.wav', '.ogg')): 
            message_type = "AUDIO"
            context.bot.send_voice(chat_id=id, voice=open(file_path, 'rb'))
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            message_type = "PHOTO"
            context.bot.send_photo(chat_id=id, photo=open(file_path, 'rb'), caption=(text if text != None else ""))
    else: 
        message_type = "TEXT"
        context.bot.send_message(chat_id=id, text=text, reply_markup=keyboard)
        logging.info(f"MESSAGE TYPE: {message_type}\t - " + (text if text != None else ""))

# Help
keyboard_help = [[InlineKeyboardButton(text="Страница разработчика", url="https://github.com/aDamTea")],
                 [InlineKeyboardButton(text="Читать документацию", url="https://github.com/aDamTea/TGVK-Bot")]]
send_help_keyboard = InlineKeyboardMarkup(keyboard_help)
