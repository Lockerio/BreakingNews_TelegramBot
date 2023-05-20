from time import sleep

import telebot
import threading

from config import BOT_TOKEN
from parsing.meta import BAIKAL_DAILY_ID, IRK_RU_ID, CITY_N_ID
from utils.answers_helper import AnswerHelper
from utils.request_helper import RequestHelper


requestHelper = RequestHelper()
answerHelper = AnswerHelper()

bot = telebot.TeleBot(BOT_TOKEN)


def background_task():
    while True:
        is_there_newest_news = RequestHelper.background_request()

        all_chat_ids = requestHelper.get_sorted_chat_ids_with_sources_agency_id()

        if is_there_newest_news[BAIKAL_DAILY_ID]:
            news = requestHelper.get_news(BAIKAL_DAILY_ID)
            for chat in all_chat_ids[BAIKAL_DAILY_ID]:
                bot.send_message(chat, news, parse_mode="html")

        if is_there_newest_news[IRK_RU_ID]:
            news = requestHelper.get_news(IRK_RU_ID)
            for chat in all_chat_ids[IRK_RU_ID]:
                bot.send_message(chat, news, parse_mode="html")

        if is_there_newest_news[CITY_N_ID]:
            news = requestHelper.get_news(CITY_N_ID)
            for chat in all_chat_ids[CITY_N_ID]:
                bot.send_message(chat, news, parse_mode="html")

        sleep(3600)


background_thread = threading.Thread(target=background_task)
background_thread.daemon = True
background_thread.start()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "<b>Привет</b>", parse_mode="html")

    telegram_id = message.from_user.id
    user_id = requestHelper.create_user(telegram_id, message.chat.id)

    action = message.json
    requestHelper.record_user_actions(user_id, action)


@bot.message_handler(commands=["update_n"])
def update_n(message):
    bot.send_message(message.chat.id, "Введите желаемое количество новостей для показа за один раз:", parse_mode="html")

    user_id = requestHelper.get_user_id(message.from_user.id)
    action = message.json
    requestHelper.record_user_actions(user_id, action)

    answerHelper.update_user_waiting_n(user_id, True)


@bot.message_handler(content_types=["text"])
def text(message):
    chat_id = message.chat.id
    user_id = requestHelper.get_user_id(message.from_user.id)

    if answerHelper.is_user_waiting_n(user_id):

        answer = requestHelper.assert_save_n(user_id, message.text)
        if answer[0]:
            answerHelper.update_user_waiting_n(user_id, False)

        bot.send_message(chat_id, answer[1], parse_mode="html")

    else:
        bot.send_message(chat_id, "К сожалению, мой разработчик не научил меня разговаривать с людьми😢")
        bot.send_message(chat_id, "Я лишь могу отправлять Вам новости")

    action = message.json
    requestHelper.record_user_actions(user_id, action)


bot.polling(none_stop=True)
