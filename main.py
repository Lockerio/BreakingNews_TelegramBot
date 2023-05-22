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

help_message = f"""
/start - Запуск бота
/help - Вывод всех возможных команд

/default - Посмотреть или выбрать источник по умолчанию
/get - Вывод новостей из источника по умолчанию
/update_n - Обновить количество новостей для показа за раз (по умолчанию 5)

/subscribe - Подписаться на агентство, вам будут приходить уведомления со свежими новостями от этого источника
/unsubscribe - Отписаться от агентства, вам не будут приходить уведомления

По предложениям, трудностям, багам, связанным со мной, писать ему🧐: @Lockerio
"""


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
    start_message = f"""
<b>Привет!</b>
Я новостной бот🤖

Я могу присылать Вам свежие новости от различных новостных агентств.
Либо Вы сами можете просматривать уже опубликованные новости.

Ладно, не буду томить Вас речами, которые написал мой разработчик🤓
Просмотрите список команд для управления мной и начинайте читать новости)
"""

    bot.send_message(message.chat.id, start_message, parse_mode="html")
    bot.send_message(message.chat.id, help_message)

    # Баг
    # Если юзер после старта бота, еще раз его стартанет, то будет исключение SQLAlchemy,
    # при попытке сохранить его действия
    #
    # telegram_id = message.from_user.id
    # user_id = requestHelper.create_user(telegram_id, message.chat.id)
    # action = message.json
    # requestHelper.record_user_actions(user_id, action)  # Баг в этой строчке


@bot.message_handler(commands=["help"])
def update_n(message):
    bot.send_message(message.chat.id, help_message)

    user_id = requestHelper.get_user(message.from_user.id).id
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

    if source_id:
        amount_news_to_show = user.news_amount_to_show

        for news_counter in range(amount_news_to_show):
            news = requestHelper.get_news_desc(user)

            if news:
                formatted_news = answerHelper.format_news(news)
                answerHelper.update_user_amount_of_read_news(user.id,
                                                             requestHelper.get_amount_of_read_news(user.id) + 1)
                bot.send_message(message.chat.id, formatted_news,
                                 parse_mode="html", disable_web_page_preview=True)
            else:
                answerHelper.update_user_amount_of_read_news(user.id, 1)
                bot.send_message(message.chat.id, "К сожалению, вы просмотрели все новости этого агентства")
                bot.send_message(message.chat.id, "Вы можете выбрать новое '/default' или "
                                                  "подождать, пока они выпустят что-нибудь новенькое😇")
                break

    else:
        bot.send_message(message.chat.id, "Вы не задали источник новостей")
        bot.send_message(message.chat.id,
                         "Используйте '/default' для установки агентства по умолчанию😏")


@bot.message_handler(commands=["default"])
def default(message):
    user = requestHelper.get_user(message.from_user.id)
    source_agency_id = user.source_agency_id

    agency = requestHelper.get_agency(source_agency_id)
    if agency:
        bot.send_message(message.chat.id, f"Источник по умолчанию: {agency.name}", disable_web_page_preview=True)

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
        types.InlineKeyboardButton("1", callback_data="default,1"),
        types.InlineKeyboardButton("2", callback_data="default,2"),
        types.InlineKeyboardButton("3", callback_data="default,3")
    ]
    markup = types.InlineKeyboardMarkup([buttons])

    bot.send_message(message.chat.id, mess, parse_mode="html", disable_web_page_preview=True,
                     reply_markup=markup)

    action = message.json
    requestHelper.record_user_actions(user.id, action)


@bot.message_handler(commands=["subscribe"])
def subscribe(message):
    user = requestHelper.get_user(message.from_user.id)

    agencies = requestHelper.get_agencies()
    agency1 = agencies[0]
    agency2 = agencies[1]
    agency3 = agencies[2]

    mess = f'''
    От какого агентства вы хотите получать уведомления:

1) <a href="{BAIKAL_DAILY_URL}">{agency1.name}</a> 
{agency1.description}  

2) <a href="{IRK_RU_URL}">{agency2.name}</a> 
{agency2.description}  

3) <a href="{CITY_N_URL}">{agency3.name}</a> 
{agency3.description}
    '''

    buttons = [
        types.InlineKeyboardButton("1", callback_data="subscribe,1"),
        types.InlineKeyboardButton("2", callback_data="subscribe,2"),
        types.InlineKeyboardButton("3", callback_data="subscribe,3")
    ]
    markup = types.InlineKeyboardMarkup([buttons])

    bot.send_message(message.chat.id, mess, parse_mode="html", disable_web_page_preview=True,
                     reply_markup=markup)

    action = message.json
    requestHelper.record_user_actions(user.id, action)


@bot.message_handler(commands=["unsubscribe"])
def unsubscribe(message):
    user = requestHelper.get_user(message.from_user.id)
    favorites = user.favorites

    if favorites:
        agencies = []
        for favorite in favorites:
            agency_id = favorite.agency_id

            agency = requestHelper.get_agency(agency_id)
            agencies.append(agency)

        mess = f'От какого агентства вы хотите отписаться?'

        buttons = [
            types.InlineKeyboardButton(f"{agency.name}", callback_data=f"unsubscribe,{agency.id}")
            for agency in agencies
        ]
        markup = types.InlineKeyboardMarkup([buttons])

        bot.send_message(message.chat.id, mess, parse_mode="html", disable_web_page_preview=True,
                         reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "Вы не подписаны ни на одно агентство")

    action = message.json
    requestHelper.record_user_actions(user.id, action)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    button_data = call.data.split(",")
    user = requestHelper.get_user(call.from_user.id)
    user_id = user.id

    sender, number = button_data[0], int(button_data[1])

    if sender == "default":
        requestHelper.save_source(call.from_user.id, number)
        answerHelper.update_user_amount_of_read_news(user.id, 1)

        bot.send_message(user.chat_id, "Источник по умолчанию установлен")

    elif sender == "subscribe":
        is_subscriber_already = requestHelper.assert_create_subscription(user_id, number)

        if is_subscriber_already:
            bot.send_message(user.chat_id, "Вы уже подписаны на это агенство")
        else:
            agency = requestHelper.get_agency(number)
            bot.send_message(user.chat_id, f"Вы подписались на {agency.name}")

    elif sender == "unsubscribe":
        agency = requestHelper.get_agency(number)
        requestHelper.delete_favorite(user_id, number)
        bot.send_message(user.chat_id, f"Вы отписались от {agency.name}")

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
