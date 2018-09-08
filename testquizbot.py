# -*- coding: utf-8 -*-
import telebot
import json

import logging
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def get_token():
	with open('bot_token.json', 'r') as f_bot_token:
		bot_token = f_bot_token.read()
		return bot_token
bot = telebot.TeleBot(get_token())

# Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Hello. I am Crazy Quiz Bot. \nI know many fun questions from all over the world. \nWhat is your name? ')
    bot.register_next_step_handler(sent, choose_category)

def choose_category(message):
    what_category = bot.send_message(message.chat.id, '{name}, choose a category of questions.'.format(name=message.text))
    bot.register_next_step_handler(what_category, choose_level)

def choose_level(message):
    what_level = bot.send_message(message.chat.id, 'Okey, choose a dificulty level.')
    #bot.register_next_step_handler()

def user_url():
	user_category = choose_category()
	user_difficulty = choose_level()
	url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
	print(url)

 
bot.polling()

# def start_bot():
#     mybot = Updater(get_token(), request_kwargs=proxy_login_data() )
#     dp = mybot.dispatcher
#     dp.add_handler(CommandHandler('start', greet_user))
#     dp.add_handler(CommandHandler('go', choose_category_level))
#     dp.add_handler(MessageHandler(Filters.text, talk_to_me))

#     mybot.start_polling()
#     mybot.idle()

# if __name__ == '__main__':
#     start_bot()