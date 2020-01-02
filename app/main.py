import random
import argparse
import logging
import os
import sys
import time
from functools import wraps
from pathlib import Path
import telegram
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

try:
    TOKEN = os.environ['BOTKEY']
    MASTERUID = os.environ['MASTERUID']
except KeyError:
    logging.warning('Token not found.')
    sys.exit(1)

patients = set()

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN, use_context=True)
jobs = updater.job_queue

dispatcher = updater.dispatcher

def start(update, context):
    chat_id = update.effective_chat
    patients.update(chat_id)

    context.bot.send_message(
        chat_id=chat_id,
        text="Hi! Welcome: I am Dr. Humbot's assistant: the doctor will receive you soon.")

answers = [
    x.strip() for x in 
    Path('./answers.txt').read_text().split('\n')]

def rasa(chat_id, text):
    
    return random.choice(answers)

def reply(update, context):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    bot_text = rasa(chat_id, user_text)

    context.bot.send_message(
        chat_id=chat_id,
        text=bot_text,
        parse_mode=telegram.ParseMode.MARKDOWN)

questions = [
    x.strip() for x in 
    Path('./questions.txt').read_text().split('\n')]

def ask(context: CallbackContext):
    text = random.choice(questions)
    for patient in patients:
        context.bot.send_message(
            chat_id=patient, 
            text=text,
            parse_mode=telegram.ParseMode.MARKDOWN)

job_a = jobs.run_daily(ask, time=19)

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