from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import json
import logging
import requests

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

def quiz_choose_category(bot, update, user_data):
    keyboard = [['General Knowledge', 'Books', 'Films', 'Music'],
    ['Computers', 'Science & Nature', 'Mathematics', 'History'],
    ['Sports', 'Art', 'Geography', 'Animals']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('\nChoose a category of questions:', reply_markup=reply_markup, one_time_keyboard=True)
    return 'difficulty'

# def quiz_get_category(bot, update, user_data):
#     user_category = update.message.text
#     print(user_category)
#     dict_category = {'General Knowledge': '9', 'Books': '10', 'Films': '11', 'Music': '12', 'Computers': '18', 'Science & Nature': '17', 'Mathematics': '19', 'History': '23', 'Sports': '21', 'Art': '25', 'Geography': '22', 'Animals': '27'} 
#     user_data['user_category'] = dict_category.get(user_category)
#     print(user_data['user_category'])
#     return 'difficulty'

def quiz_choose_difficulty(bot, update, user_data):
    user_category = update.message.text
    dict_category = {'General Knowledge': '9', 'Books': '10', 'Films': '11', 'Music': '12', 'Computers': '18', 'Science & Nature': '17', 'Mathematics': '19', 'History': '23', 'Sports': '21', 'Art': '25', 'Geography': '22', 'Animals': '27'} 
    user_data['user_category'] = dict_category.get(user_category)
    keyboard = [['Easy', 'Medium', 'Hard']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('\nChoose a difficulty level:', reply_markup=reply_markup, one_time_keyboard=True)
    return 'create_url'

def quiz_create_url(bot, update, user_data):
    user_difficulty = update.message.text
    user_data['user_difficulty'] = user_difficulty
    user_category = user_data['user_category']
    url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
    user_data['user_url'] = url
    return get_quiz

def get_quiz(bot, update, user_data):
    url = user_data['user_url']
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        if data.get('response_code') == 0:
            results = data.get('results')
            return results
        else:
            return 'Something is wrong. Try again.'
    else:
        return 'Server is not responding now and something has broken.'

# def quiz_questions_answers(results):
#     for question_answer_info in results:
#         return(question_answer_info['question'])
#         answers = question_answer_info['incorrect_answers']
#         correct_answer = question_answer_info['correct_answer']
#         answers.append(correct_answer)
#         return(answers)
#         user_answer = input('Write a right answer.')
#         if user_answer == correct_answer:
#             return('Yo! It is correct answer.')
#         else:
#             return("""Nope. Try again.
# """ + str(answers))
#             user_answer = input('Write a right answer.')
#             if user_answer == correct_answer:
#                 return('Great! This is correct.')
#             else:                       
#                 return("""No, no, no.
# Correct answer is """ + correct_answer +'.')
#     user_choice_continue = input('Well done! Bro, would you want to continue?')
#     return user_choice_continue
    
# if __name__ == '__main__':
#     #PROXY = proxy_login_data()
#     answers_questions = 'yes'
#     while answers_questions == 'yes':
#         user_questions_api = user_questions_url()
#         result_quiz = quiz(user_questions_api)
#         answers_questions = quiz_questions_answers(result_quiz)
#     else:
#         return 'Okey and Buy. I will be miss you.'

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

def open_google(bot, update, user_data):
    keyboard = [[InlineKeyboardButton(text="Googling", url='https://www.google.com/')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('\nPress the button and find more info:', reply_markup=reply_markup)

def talk_to_me(bot, update, user_data):
    user_text = update.message.text 
    #print(user_text)
    update.message.reply_text(user_text)
    #user_data['text'] = update.message.text

def start_bot():
    mybot = Updater(get_token(), request_kwargs=proxy_login_data() )
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('play', quiz_choose_category, pass_user_data=True))
    dp.add_handler(CommandHandler('google', open_google, pass_user_data=True))
    dp.add_handler(RegexHandler('^(google|info|search)$', open_google, pass_user_data=True))
    dp.add_handler(RegexHandler('^(General Knowledge|Books|Films|Music|Computers|Science & Nature|Mathematics|History|Sports|Art|Geography|Animals)$', create_url, pass_user_data=True))
    quiz = ConversationHandler(
        entry_points=[CommandHandler('play', quiz_choose_category, pass_user_data=True)],
        states={
        'difficulty': [RegexHandler('^(General Knowledge|Books|Films|Music|Computers|Science & Nature|Mathematics|History|Sports|Art|Geography|Animals)$', quiz_choose_difficulty, pass_user_data=True)],
        'create_url': [RegexHandler('^(Easy|Medium|Hard)$', quiz_create_url, pass_user_data=True)]
            }
        fallbacks=[]
        )
    dp.add_handler(quiz)
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    start_bot()