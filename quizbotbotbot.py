from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import json
import logging

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
    hello = 'Hello, {}. I am Crazy Quiz Bot. \nI know many fun questions from all over the world. \nLet`s do it! \nStart a Quiz game - /play \nStart the Quiz again - /restart \nStop this game - /stop \nSearch info in Google - /google '.format(update.message.chat.first_name)
    print(hello)
    update.message.reply_text(hello)
    user_data['user_name'] = update.message.chat.first_name
    print(user_data['user_name'])

def choose_category(bot, update, user_data):
    keyboard = [['General Knowledge', 'Books', 'Films', 'Music'],
    ['Computers', 'Science & Nature', 'Mathematics', 'History'],
    ['Sports', 'Art', 'Geography', 'Animals']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('\nChoose a category of questions:', reply_markup=reply_markup)

def create_url_category(bot, update, user_data):
    dict_category = {'General Knowledge': '9', 'Books': '10', 'Films': '11', 'Music': '12', 'Computers': '18', 'Science & Nature': '17', 'Mathematics': '19', 'History': '23', 'Sports': '21', 'Art': '25', 'Geography': '22', 'Animals': '27'}
    user_data['user_category'] = 

def create_url(bot, update, user_data)
    user_category = user_data['user_category']
    user_difficulty = user_data['user_difficulty']
    url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
    return url

# def choose_category(bot, update, user_data):
#     keyboard = [[InlineKeyboardButton("General Knowledge", callback_data='9')],
#         [InlineKeyboardButton("Entertaiment: Books", callback_data='10')],
#         [InlineKeyboardButton("Entertaiment: Films", callback_data='11')],
#         [InlineKeyboardButton("Entertaiment: Music", callback_data='12')],
#         [InlineKeyboardButton("Science: Computers", callback_data='18')],
#         [InlineKeyboardButton("Science & Nature", callback_data='17')],
#         [InlineKeyboardButton("Science: Mathematics", callback_data='19')],
#         [InlineKeyboardButton("History", callback_data='23')],             
#         [InlineKeyboardButton("Sports", callback_data='21')],                
#         [InlineKeyboardButton("Art", callback_data='25')],
#         [InlineKeyboardButton("Geography", callback_data='22')],
#         [InlineKeyboardButton("Animals", callback_data='27')]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('\nChoose a category of questions:', reply_markup=reply_markup)
    # user_data['user_category'] = callback_data
    # print(user_data['user_category'])
    #https://www.programcreek.com/python/example/106608/telegram.ext.CallbackQueryHandler

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
    #user_data['text'] = update.message.text
    

def start_bot():
    mybot = Updater(get_token(), request_kwargs=proxy_login_data() )
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('play', choose_category, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(Computers)$', create_url, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    start_bot()