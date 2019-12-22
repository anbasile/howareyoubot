import os
import sys
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

try:
    token = os.environ['BOTKEY']
except KeyError:
    logging.warning('Token not found.')
    sys.exit(1)
    
updater = Updater(
    token=token, 
    use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=update.message.text)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()