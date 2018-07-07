# -*- coding: utf-8 -*-

import json
import requests

def proxy_login_data():
	with open('proxy_login.json', 'r') as f_proxy_login:
		proxy_login = f_proxy_login.read()
	proxies = {
		'http': str(proxy_login),
		'https': str(proxy_login)
		}
	return proxies

def user_questions_url():
	user_category = input('Choose a category of questions.')
	user_difficulty = input('Choose a dificulty level.')
	url = 'https://opentdb.com/api.php?amount=5&category=%s&difficulty=%s' % (user_category, user_difficulty)
	return url

def quiz(url, proxies):
	data = requests.get(url, proxies=proxies)
	if data.status_code == 200:
		data = data.json()
		if data.get('response_code') == 0:
			results = data.get('results')
			return results
		else:
			print('Something is wrong. Try again.')
	else:
		print('Server is not responding now and something has broken.')

def quiz_questions_answers(results):
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
	return user_choice_continue

def user_choice_continue(proxies, results, user_choice_continue):
	while user_choice_continue == 'yes':
			category_range = user_questions_url()
			quiz_range = quiz(category_range, proxies)
			continue_answers = quiz_questions_answers(results)
			return continue_answers
	else:
		print('Okey and Buy. I will be miss you.')
	
if __name__ == '__main__':
	PROXY = proxy_login_data()
	user_questions_api = user_questions_url()
	result_quiz = quiz(user_questions_api, PROXY)
	answers_questions = quiz_questions_answers(result_quiz)
	continue_choice = user_choice_continue(PROXY, result_quiz, answers_questions)

