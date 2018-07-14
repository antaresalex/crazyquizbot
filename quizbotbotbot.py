from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from quizbotbot import proxy_login_data, user_questions_url, quiz, quiz_questions_answers

import logging
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def get_token():
	with open('bot_token.json', 'r') as f_bot_token:
		bot_token = f_bot_token.read()
		return bot_token

def greet_user(bot, update):
	hello = "Hello, dear user. I am Crazy Quiz Bot. \nI know many fun questions of different topics. Let is start to play."
	print(hello)
	update.message.reply_text(hello)

def choose_category_level(bot, update):
	what_category = "Choose a category of questions."
	print(what_category)
	update.message.reply_text(what_category)

def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def start_bot():
	mybot = Updater(get_token(), request_kwargs=proxy_login_data() )
	mybot.dispatcher.add_handler(CommandHandler('start', greet_user))
	mybot.dispatcher.add_handler(CommandHandler('go', choose_category_level))
	mybot.dispatcher.add_handler(MessageHandler(Filters.text, talk_to_me))

	mybot.start_polling()
	mybot.idle()

if __name__ == '__main__':
	start_bot()