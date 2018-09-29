# -*- coding: utf-8 -*-
import telebot
import json
from telebot import types

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

#greeting
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
    
#google
@bot.message_handler(commands=['google'])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Googling", url="https://www.google.com/")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Press the button and find more info.", reply_markup=keyboard)

#echo-bot
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

# def user_url():
# 	user_category = choose_category()
# 	user_difficulty = choose_level()
# 	url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
# 	print(url)
 
if __name__ == '__main__':
    bot.polling(none_stop=True)
