import time
import os
from functools import wraps
import sys
import logging
import argparse
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

try:
    TOKEN = os.environ['BOTKEY']
except KeyError:
    logging.warning('Token not found.')
    sys.exit(1)


PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hi! Welcome: I am Dr. Humbot's assistant: the doctor will receive you soon.")

def rasa(chat_id, text):
    return text

def reply(update, context):
    chat_id = update.effective_chat.id
    user_text = update.message.text
    bot_text = rasa(chat_id, user_text)

    context.bot.send_message(
        chat_id=chat_id,
        text=bot_text)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

main_handler = MessageHandler(Filters.text, reply)
dispatcher.add_handler(main_handler)

def start_webhook():
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
    updater.bot.set_webhook("https://howareyoubot.herokuapp.com/" + TOKEN)
    updater.idle()

def start_polling():
    updater.start_polling()

if __name__=='__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--webhook', action='store_true')

    args = parser.parse_args()

    if args.webhook:
        start_webhook()
    else:
        start_polling()