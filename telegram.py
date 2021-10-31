
import telebot
from telebot import types
import time 
import repository_ekaterina as rp
import config as conf

bot = telebot.TeleBot(conf.TELEGRAM)

repository=rp.Repository()
name =""
surname = ''
age = 0
chat_id=0
status=''
hello=['привет','здравствуй', 'здарова', 'приветики', 'ку', 'слушай', '', '', '']

@bot.message_handler(content_types=['text', 'audio'])

def start(message):
    global chat_id, name,surname,age, status
    chat_id= message.from_user.id
    name, surname, age, tg_id, status=repository.getPersonById(chat_id)
    if message.text.lower() in hello and chat_id==tg_id:
            bot.send_message(message.from_user.id, 'Вечер в хату! '+name)
    if chat_id!=tg_id:
        login = types.InlineKeyboardButton(text='Регистрация', callback_data='login'); #кнопка «регистрация»
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        keyboard.add(login); #добавляем кнопку в клавиатуру
        bot.send_message(message.from_user.id, text="Я не знаю с кем говорю", reply_markup=keyboard)

    if message.text == '/reg': 
        if chat_id==tg_id:
            bot.send_message(message.from_user.id, "Ты уже зарегестрирован: "+name)
        else: 
            bot.send_chat_action(chat_id=message.from_user.id, action = 'typing')
            bot.send_message(message.from_user.id, "Как тебя зовут?")
            bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name


def get_name(message): #получаем фамилию
    global name
    name = message.text
    
    bot.send_chat_action(chat_id=message.from_user.id, action = 'typing')
    bot.send_message(message.from_user.id, 'А фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_chat_action(chat_id=message.from_user.id, action = 'typing')

    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message): #Лень исправлять(
    error_age(message)

def error_age(message):
    global age
    try:#проверяем, что возраст введен корректно
        age = int(message.text) 
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        bot.send_chat_action(chat_id=message.from_user.id, action = 'typing')
        question = 'Тебе '+str(age)+', и зовут '+name+' '+surname+'?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    except Exception:
        bot.send_chat_action(chat_id=message.from_user.id, action = 'typing')
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста!')
        return bot.register_next_step_handler(message, get_age)

@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):
    global name, surname, age, chat_id, status
    if call.data == "yes": #call.data это callback_data, которую указали при объявлении кнопки
        status="user"
        repository.tgReg(name, surname, age, chat_id, status)
        bot.send_message(call.message.chat.id, 'Запомню, солнышко :)')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Это прискорбно :(')
        bot.send_chat_action(call.message.chat.id, action = 'typing')
        bot.send_message(call.message.chat.id, "Давай заново?! Как тебя зовут?")
        bot.register_next_step_handler(call.message, get_name)
    elif call.data == "login":
            bot.send_chat_action(chat_id=call.message.chat.id, action = 'typing')
            bot.send_message(call.message.chat.id, "Как тебя зовут?")
            bot.register_next_step_handler(call.message, get_name)




bot.polling(none_stop=True, interval=0)



