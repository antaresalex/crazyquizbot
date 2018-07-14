from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from quizbotbot import proxy_login_data, user_questions_url, quiz, quiz_questions_answers

import logging
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def greet_user(bot, update):
    hello = "Hello, dear user. I am Crazy Quiz Bot. \nI know many fun questions from all over the world. \nLet`s do it!"
    print(hello)
    update.message.reply_text(hello)


def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)


def get_token():
    with open('bot_token.json', 'r') as f_bot_token:
        bot_token = f_bot_token.read()
        return bot_token


def start_bot():
    PROXY = proxy_login_data()
    mybot = Updater(get_token(), request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('questions', quiz_questions_answers))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    start_bot()