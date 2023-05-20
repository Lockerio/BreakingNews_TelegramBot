import telebot
import threading

from config import BOT_TOKEN
from utils.answers_helper import AnswerHelper
from utils.request_helper import RequestHelper


requestHelper = RequestHelper()
answerHelper = AnswerHelper()

bot = telebot.TeleBot(BOT_TOKEN)


def background_task():
    is_there_newest_news = RequestHelper.background_request()








# background_thread = threading.Thread(target=background_task)
# background_thread.daemon = True
# background_thread.start()


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
