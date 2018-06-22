# -*- coding: utf-8 -*-

import json
import requests

with open('proxy_login.json', 'r') as f_proxy_login:
	proxy_login = f_proxy_login.read()

proxies = {
	'http': str(proxy_login),
	'https': str(proxy_login)
	}

def quiz (url, proxies):
	response = requests.get(url, proxies=proxies)
	if response.status_code == 200:
		get_response = response.json()
		return get_response
	else:
		return 'На сервере что-то пошло не так.'


if __name__ == '__main__':
	user_category = input('Выбирай скорее тему вопросов и погнали.')
	user_difficulty = input('Кстати, хочешь посложнее или полегче вопросики?')
	url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
	questions = quiz(url, proxies)
	
	print(questions)