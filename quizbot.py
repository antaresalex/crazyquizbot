import json
import requests

def quiz (url):
	response = requests.get(url)
	if response.status_code == 200:
		get_response = response.json()
		return get_response
	else:
		return ('На сервере что-то пошло не так.')


if __name__ == '__main__':
	user_category = input('Выбери тему вопросов.')
	user_difficulty = str(input('Выберете сложность вопросов.'))
	url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
	questions = quiz(url)
	
	print(questions)