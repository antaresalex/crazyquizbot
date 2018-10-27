from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import random
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
    update.message.reply_text(hello)
    user_data['user_name'] = update.message.chat.first_name

def quiz_restart(bot, update, user_data):
    restart = 'Dear {}. Because I am Super Crazy Quiz Bot, I know many more fun questions. \nIf you want to start a Quiz game again - /play \nIf you want to stop - /stop \nPlease, give me the command '.format(update.message.chat.first_name)
    update.message.reply_text(restart)
    return 'category'

def quiz_choose_category(bot, update, user_data):
    keyboard = [['General Knowledge', 'Books', 'Films', 'Music'],
    ['Computers', 'Science & Nature', 'Mathematics', 'History'],
    ['Sports', 'Art', 'Geography', 'Animals']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('\nChoose a category of questions:', reply_markup=reply_markup, one_time_keyboard=True)
    return 'difficulty'

def quiz_choose_difficulty(bot, update, user_data):
    user_category = update.message.text
    dict_category = {'General Knowledge': '9', 'Books': '10', 'Films': '11', 'Music': '12', 'Computers': '18', 'Science & Nature': '17', 'Mathematics': '19', 'History': '23', 'Sports': '21', 'Art': '25', 'Geography': '22', 'Animals': '27'} 
    user_data['user_category'] = dict_category.get(user_category)
    keyboard = [['Easy', 'Medium', 'Hard']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('\nChoose a difficulty level:', reply_markup=reply_markup, one_time_keyboard=True)
    return 'create_url'

def quiz_url(bot, update, user_data):
    user_difficulty = update.message.text
    user_difficulty = user_difficulty.lower()
    user_data['user_difficulty'] = user_difficulty
    user_category = user_data['user_category']
    url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
    user_data['user_url'] = url
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        if data.get('response_code') == 0:
            results = data.get('results')
            user_data['user_results'] = results
            user_data['user_question_number'] = 0
            return quiz_questions(bot, update, user_data)
        else:
            print('Something is wrong. Check Postman')
            print(url)
            return 'quiz_restart'
    else:
        print('Server is not responding now. Check Postman')
        return 'quiz_restart'
        #return ConversationHandler.END

def quiz_questions(bot, update, user_data):
    results = user_data['user_results'] 
    user_question_number = user_data['user_question_number']
    question_answer_info = results[user_question_number]
    question_text = question_answer_info['question']
    user_data['user_question'] = question_text
    answers = question_answer_info['incorrect_answers']
    correct_answer = question_answer_info['correct_answer']
    user_data['user_correct_answer'] = correct_answer
    answers.append(correct_answer)
    random.shuffle(answers)
    keyboard = []
    for answer in answers:
        keyboard.append([answer])
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(question_text + '\nChoose a right answer:', reply_markup=reply_markup)
    return 'quiz_answers'

def quiz_answers(bot, update, user_data):
    user_answer = update.message.text
    correct_answer = user_data['user_correct_answer']
    if user_answer == correct_answer:
        update.message.reply_text('Yo! It is correct answer.')
        user_question_number = user_data['user_question_number']
        if user_question_number != 4:
            user_data['user_question_number'] = user_question_number + 1 
            return quiz_questions(bot, update, user_data)
        else:
            update.message.reply_text('Well done! Quiz is over. Bro, would you want to continue?')
            #клавиатура с да или нет и отлавливаем ответ в рестарте
            return quiz_restart(bot, update, user_data)
    else:
        question_text = user_data['user_question']
        update.message.reply_text('No! It is incorrect answer. Try again.\n' + question_text)
        return 'quiz_answers'

#     else:
#         return("""Nope. Try again.
# """ + str(answers))
#         user_answer = input('Write a right answer.')
#         if user_answer == correct_answer:
#             return('Great! This is correct.')
#         else:                       
#             return("""No, no, no.
# Correct answer is """ + correct_answer +'.')
#     user_choice_continue = input('Well done! Bro, would you want to continue?')
#     return user_choice_continue
    
# if __name__ == '__main__':
#     answers_questions = 'yes'
#     while answers_questions == 'yes':
#         user_questions_api = user_questions_url()
#         result_quiz = quiz(user_questions_api)
#         answers_questions = quiz_questions_answers(result_quiz)
#     else:
#         return 'Okey and Buy. I will be miss you.'

    #https://www.programcreek.com/python/example/106608/telegram.ext.CallbackQueryHandler

def open_google(bot, update, user_data):
    keyboard = [[InlineKeyboardButton(text="Googling", url='https://www.google.com/')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('\nPress the button and find more info:', reply_markup=reply_markup)

def talk_to_me(bot, update, user_data):
    user_text = update.message.text 
    update.message.reply_text(user_text)
    return ConversationHandler.END

def dont_know(bot, update, user_data):
    user_text = update.message.text 
    update.message.reply_text('When you write: ' + user_text + '. What do you mean?\nI dont understand you, sorry')

def start_bot():
    mybot = Updater(get_token(), request_kwargs=proxy_login_data() )
    dp = mybot.dispatcher
    quiz = ConversationHandler(
        entry_points=[CommandHandler('play', quiz_choose_category, pass_user_data=True)],
        states={
            'category': [CommandHandler('play', quiz_choose_category, pass_user_data=True)],
            'difficulty': [RegexHandler('^(General Knowledge|Books|Films|Music|Computers|Science & Nature|Mathematics|History|Sports|Art|Geography|Animals)$', quiz_choose_difficulty, pass_user_data=True)],
            'create_url': [RegexHandler('^(Easy|Medium|Hard)$', quiz_url, pass_user_data=True)],
            'quiz_restart': [
                CommandHandler('restart', quiz_restart, pass_user_data=True), 
                RegexHandler('^(restat|again)$',quiz_restart, pass_user_data=True)
            ],
            'quiz_answers': [MessageHandler(Filters.text, quiz_answers, pass_user_data=True)]
        },
        #fallbacks=[]
        fallbacks=[MessageHandler(Filters.text, dont_know, pass_user_data=True)]
        )
    dp.add_handler(quiz)
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('google', open_google, pass_user_data=True))
    dp.add_handler(RegexHandler('^(google|info|search)$', open_google, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    start_bot()