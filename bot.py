import config
import telebot
from telebot import types
from database import Database

db = Database('db.db')
bot = telebot.TeleBot(config.TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Поиск музыканта')
    markup.add(item1)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🗣 Сказать свой профиль')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('❌ Остановить поиск')
    markup.add(item1)
    return markup

@bot.message_handler(commands = ['start'])
@dp.message_handler(commands="inline_url")
async def cmd_inline_url(message: types.Message):
    buttons = [
    item1 = types.KeyboardButton('Я исполнитель 🗣')
    item2 = types.KeyboardButton('Я битмейкер 🥁')
    item3 = types.KeyboardButton('Я менеджер 🌝')
    item4 = types.KeyboardButton('Я саунд-продюсер 🎧')
    item5 = types.KeyboardButton('Я саунд-дизайнер 🤭')
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}! Ты не спроста зашёл сюда. Выбери кто-то из указанного списка! И вскоре начнём искать музыканта специально для тебя! '.format(message.from_user), reply_markup = markup)
