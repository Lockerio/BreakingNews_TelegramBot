import telebot
import threading

from time import sleep
from telebot import types

from config import BOT_TOKEN
from parsing.meta import BAIKAL_DAILY_ID, IRK_RU_ID, CITY_N_ID, BAIKAL_DAILY_URL, IRK_RU_URL, CITY_N_URL
from utils.answers_helper import AnswerHelper
from utils.request_helper import RequestHelper


requestHelper = RequestHelper()
answerHelper = AnswerHelper()

bot = telebot.TeleBot(BOT_TOKEN)


# def background_task():
#     while True:
#         is_there_newest_news = RequestHelper.background_request()
#
#         all_chat_ids = requestHelper.get_sorted_chat_ids_with_sources_agency_id()
#
#         if is_there_newest_news[BAIKAL_DAILY_ID]:
#             news = requestHelper.get_news(BAIKAL_DAILY_ID)
#             for chat in all_chat_ids[BAIKAL_DAILY_ID]:
#                 bot.send_message(chat, news, parse_mode="html")
#
#         if is_there_newest_news[IRK_RU_ID]:
#             news = requestHelper.get_news(IRK_RU_ID)
#             for chat in all_chat_ids[IRK_RU_ID]:
#                 bot.send_message(chat, news, parse_mode="html")
#
#         if is_there_newest_news[CITY_N_ID]:
#             news = requestHelper.get_news(CITY_N_ID)
#             for chat in all_chat_ids[CITY_N_ID]:
#                 bot.send_message(chat, news, parse_mode="html")
#
#         sleep(3600)
#
#
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

    user_id = requestHelper.get_user(message.from_user.id).id
    action = message.json
    requestHelper.record_user_actions(user_id, action)
    answerHelper.update_user_waiting_n(user_id, True)


@bot.message_handler(commands=["get"])
def get(message):
    user = requestHelper.get_user(message.from_user.id)
    action = message.json
    requestHelper.record_user_actions(user.id, action)

    source_id = user.source_agency_id
    amount_news_to_show = user.news_amount_to_show

    for news in range(amount_news_to_show):
        news = requestHelper.get_news(source_id)
        formatted_news = answerHelper.format_news(news)
        bot.send_message(message.chat.id, formatted_news,
                         parse_mode="html", disable_web_page_preview=True)


@bot.message_handler(commands=["from_source"])
def from_source(message):
    agencies = requestHelper.get_agencies()
    agency1 = agencies[0]
    agency2 = agencies[1]
    agency3 = agencies[2]

    mess = f'''
    Выберите источник по умолчанию:
    
1) <a href="{BAIKAL_DAILY_URL}">{agency1.name}</a> 
{agency1.description}  

2) <a href="{IRK_RU_URL}">{agency2.name}</a> 
{agency2.description}  

3) <a href="{CITY_N_URL}">{agency3.name}</a> 
{agency3.description}
    '''

    buttons = [
        types.InlineKeyboardButton("1", callback_data=1),
        types.InlineKeyboardButton("2", callback_data=2),
        types.InlineKeyboardButton("3", callback_data=3)
    ]

    markup = types.InlineKeyboardMarkup([buttons])

    bot.send_message(message.chat.id, mess, parse_mode="html", disable_web_page_preview=True,
                     reply_markup=markup)

    user = requestHelper.get_user(message.from_user.id)
    action = message.json
    print(user.id)
    requestHelper.record_user_actions(user.id, action)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    button_data = call.data
    requestHelper.save_source(call.from_user.id, button_data)
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=["text"])
def text(message):
    chat_id = message.chat.id
    user = requestHelper.get_user(message.from_user.id)

    user_id = user.id

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
