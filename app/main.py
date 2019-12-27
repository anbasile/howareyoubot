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
    TOKEN = os.environ['BOTKEY']
except KeyError:
    logging.warning('Token not found.')
    sys.exit(1)


def main():
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    # add handlers

    dispatcher = updater.dispatcher

    def start(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Hi! Welcome: I am Dr. Humbot's assistant: the doctor will receive you soon.")

    def reply(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=update.message.text)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    main_handler = MessageHandler(Filters.text, reply)
    dispatcher.add_handler(main_handler)


    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
    updater.bot.set_webhook("https://howareyoubot.herokuapp.com/" + TOKEN)
    updater.idle()
        

if __name__ == '__main__':
    main()