import config
import telebot
from telebot import types
from database import Database

#импорт, необходимых для telegram-бота библиотек

db = Database('db.db')
bot = telebot.TeleBot(config.TOKEN)

#импорт базы данных и подключение telegram-бота к токену

#сейчас прописываем основные команды в меню telegram-бота

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
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Я исполнитель 🗣')
    item2 = types.KeyboardButton('Я битмейкер 🥁')
    item3 = types.KeyboardButton('Я менеджер 🌝')
    item4 = types.KeyboardButton('Я саунд-продюсер 🎧')
    item5 = types.KeyboardButton('Я саунд-дизайнер 🤭')
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}! Добро пожаловать в анонимный чат! Укажите ваш профиль! '.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Поиск музыканта')
    markup.add(item1)

    bot.send_message(message.chat.id, '📝 Меню'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['stop'])
def stop(message, markup=None):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('✏️ Следующий диалог')
        item2 = types.KeyboardButton('/menu')
        markup.add(item1, item2)

        bot.send_message(chat_info[1], '❌ Человек покинул чат', reply_markup = markup)
        bot.send_message(message.chat.id, '❌ Вы вышли из чата', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, '❌ Вы не начали чат!', reply_markup = markup)

#введены основные кнопки, далее

@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👥 Поиск музыканта' or message.text == '✏️ Следующий диалог':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🔎 Исполнитель')
            item2 = types.KeyboardButton('🔎 Битмейкер')
            item3 = types.KeyboardButton('🔎 Менеджер')
            item4 = types.KeyboardButton('🔎 Саунд-продюсер')
            item5 = types.KeyboardButton('🔎 Cаунд-дизайнер')
            markup.add(item1, item2, item3, item4, item5)

            bot.send_message(message.chat.id, 'Кого искать?', reply_markup = markup)

            
        elif message.text == '❌ Остановить поиск':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Поиск остановлен, напишите /menu', reply_markup = main_menu())

        
        elif message.text == '🔎 Исполнитель':
            user_info = db.get_gender_chat('singer')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск музыканта', reply_markup = stop_search())
            else:
                mess = 'Музыкант найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        
        elif message.text == '🔎 Битмейкер':
            user_info = db.get_gender_chat('beatmaker')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск человека', reply_markup = stop_search())
            else:
                mess = 'Музыкант найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        

        elif message.text == '🔎 Менеджер':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск человека', reply_markup = stop_search())
            else:
                mess = 'Человек найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())

        elif message.text == '🔎 Саунд-продюсер':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск человека', reply_markup = stop_search())
            else:
                mess = 'Человек найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())

        elif message.text == '🔎 Cаунд-дизайнер':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск человека', reply_markup=stop_search())
            else:
                mess = 'Человек найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                bot.send_message(chat_two, mess, reply_markup=stop_dialog())
        
        elif message.text == '🗣 Сказать свой профиль':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '🗣 Вы сказали свой профиль')
                else:
                    bot.send_message(message.chat.id, '❌ В вашем аккаунте не указан username')
            else:
                bot.send_message(message.chat.id, '❌ Вы не начали диалог!')

        

        elif message.text == 'Я исполнитель 🗣':
            if db.set_gender(message.chat.id, 'singer'):
                bot.send_message(message.chat.id, '✅ Ваш профиль успешно добавлен!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Вы уже указали ваш профиль. Обратитесь в поддержку @dimatherapper')
        
        elif message.text == 'Я битмейкер 🥁':
            if db.set_gender(message.chat.id, 'beatmaker'):
                bot.send_message(message.chat.id, '✅ Ваш профиль успешно добавлен!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Вы уже указали ваш профиль. Обратитесь в поддержку @dimatherapper')

        elif message.text == 'Я менеджер 🌝':
            if db.set_gender(message.chat.id, 'manager'):
                bot.send_message(message.chat.id, '✅ Ваш профиль успешно добавлен!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Вы уже указали ваш профиль. Обратитесь в поддержку @dimatherapper')

        elif message.text == 'Я саунд-продюсер 🎧':
            if db.set_gender(message.chat.id, 'sound producer'):
                bot.send_message(message.chat.id, '✅ Ваш профиль успешно добавлен!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Вы уже указали ваш профиль. Обратитесь в поддержку @dimatherapper')

        elif message.text == 'Я саунд-дизайнер 🤭':
            if db.set_gender(message.chat.id, 'sound director'):
                bot.send_message(message.chat.id, '✅ Ваш профиль успешно добавлен!', reply_markup=main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Вы уже указали ваш профиль. Обратитесь в поддержку @dimatherapper')


        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❌ Вы не начали диалог!')


@bot.message_handler(content_types='stickers')
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')

@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')



bot.polling(none_stop = True)