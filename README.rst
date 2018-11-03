CRAZY QUIZ BOT
==============

CrazyQuizBot - это Телеграм-бот, который выдает пользавателю вопросы по выбранной категории и с заданной им сложностью. 
Вопросы и ответы получаются по API c сайта `Open TRIVIA Database`_ в виде словаря со списками.

Подключение и использование бота
--------------------------------

Вы можете найти данный бот в Телеграм по логину: @CrazyQuizBot

Установка
---------

Создайте виртуальное окружение и активируйте его. Далее в виртуальном окружениии выполните:

.. code-block:: text

	pip install -r requirements.txt

Ориентирование
--------------

Файл quizbot.py содержит код для выполнения в командной строке
Файл quizbotbot.py содержит код для выполнения в командной строке с разбивкой на функции
Файл quizbotbotbot.py с использованием библиотеки `Python Telegram Bot`_
Файл testquizbot.py с использованием библиотеки `TeleBot`_

.. _Open TRIVIA Database: https://opentdb.com/
.. _Python Telegram Bot: https://github.com/python-telegram-bot
.. _TeleBot: https://github.com/eternnoir/pyTelegramBotAPI