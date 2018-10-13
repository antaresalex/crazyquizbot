from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging
import json
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def get_token():
  with open('bot_settings.json', 'r') as f_bot_token:
      bot_token = json.loads(f_bot_token.read())["bot_token"]
      return bot_token

def proxy_login_data():
    with open('bot_settings.json', 'r') as f_proxy_login:
        proxy_login = json.loads(f_proxy_login.read())["bot_proxy"]
        return proxy_login

# def get_token():
# 	with open('bot_token.json', 'r') as f_bot_token:
# 		bot_token = f_bot_token.read()
# 		return bot_token

# def proxy_login_data():
#     with open('proxy_login.json', 'r') as f_proxy_login:
#         proxy_login = eval(f_proxy_login.read())
#         return proxy_login

#https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py

def greet_user(bot, update, user_data):
    hello = 'Hello, {}. I am Crazy Quiz Bot. \nI know many fun questions from all over the world. \nLet`s do it! \nChoose a category of questions.'.format(update.message.chat.first_name)
    print(hello)
    update.message.reply_text(hello)

# def choose_category(bot, update, user_data):
#     bot.send_messege(update.messege.chat_id, "Choose a category of questions.")
#     # what_category = "Choose a category of questions."
#     # print(what_category)
#     # update.message.reply_text(what_category)
#     user_data['category'] = update.message.text
#     print(user_data['category'])

# def choose_level(bot, update):
#     what_level = "Choose a dificulty level."
#     print(what_level)
#     update.message.reply_text(what_level)
#     user_level = update.message.reply_text(what_level)
#     return user_level

def talk_to_me(bot, update, user_data):
    user_text = update.message.text 
    #print(user_text)
    update.message.reply_text(user_text)
    user_data['text'] = update.message.text
    print(user_data['text'])

def start_bot():
    mybot = Updater(get_token(), request_kwargs=proxy_login_data() )
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    #dp.add_handler(CommandHandler('go', choose_category, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    start_bot()