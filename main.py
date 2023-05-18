import json
import telebot
from sqlalchemy.orm import Session

# from DB.container import userService
from database import engine
from serializers.user_serializer import UserSerializer
from services.user_service import UserService
from config import BOT_TOKEN
from utils.request_helper import RequestHelper

bot = telebot.TeleBot(BOT_TOKEN)
requestHelper = RequestHelper()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "<b>Привет</b>", parse_mode="html")

    telegram_id = message.from_user.id
    user_id = requestHelper.create_user(telegram_id)

    action = message.json
    requestHelper.record_user_actions(user_id, action)


@bot.message_handler(content_types=["text"])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "К сожалению, мой разработчик не научил меня разговаривать с людьми😢")
    bot.send_message(chat_id, "Я лишь могу отправлять Вам новости")

    user_id = requestHelper.get_user_id(message.from_user.id)
    action = message.json
    requestHelper.record_user_actions(user_id, action)



bot.polling(none_stop=True)
