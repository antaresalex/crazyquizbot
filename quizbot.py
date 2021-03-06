# -*- coding: utf-8 -*-

import json
import requests

with open('proxy_login.json', 'r') as f_proxy_login:
	proxy_login = f_proxy_login.read()

proxies = {
	'http': str(proxy_login),
	'https': str(proxy_login)
	}

def quiz(url, proxies):
	response = requests.get(url, proxies=proxies)
	if response.status_code == 200:
		get_response = response.json()
		return get_response
	else:
		print('Server is not responding now and something has broken.')

if __name__ == '__main__':
	user_choice_continue = 'yes'
	while user_choice_continue == 'yes':
		user_category = input('Choose a category of questions.')
		user_difficulty = input('Choose a dificulty level.')
		url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
		data = quiz(url, proxies)
		if data.get('response_code') == 0:
			results = data.get('results')
			for question_answer_info in results:
				print(question_answer_info['question'])
				answers = question_answer_info['incorrect_answers']
				correct_answer = question_answer_info['correct_answer']
				answers.append(correct_answer)
				print(answers)
				user_answer = input('Write a right answer.')
				if user_answer == correct_answer:
					print('Yo! It is correct answer.')
				else:
					print("""Nope. Try again.
""" + str(answers))
					user_answer = input('Write a right answer.')
					if user_answer == correct_answer:
						print('Great! This is correct.')
					else:
						print("""No, no, no.
Correct answer is """ + correct_answer +'.')
			user_choice_continue = input('Well done! Bro, would you want to continue?')
		else:
			print('Something is wrong. Try again.')
	else:
		print('Okey and Buy. I will be miss you.')
	

	