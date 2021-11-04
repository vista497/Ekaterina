import telebot
from telebot import types
import time 
import config
import repository_ekaterina as rp
import subprocess
import speech_recognition as sr
from ekaterina import Kate
import os

bot = telebot.TeleBot(config.TELEGRAM)

repository=rp.Repository()
name =""
surname = ''
age = 0
chat_id=0
status=''
hello=['привет','здравствуй', 'здарова', 'приветики', 'ку', 'слушай', '', '', '']

@bot.message_handler(commands=['start'])
def starting(message):
    global chat_id, name,surname,age, status
    chat_id= message.from_user.id
    name, surname, age, tg_id, status=repository.getPersonById(chat_id)
    if chat_id!=tg_id:
        login = types.InlineKeyboardButton(text='Регистрация', callback_data='login'); #кнопка «регистрация»
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        keyboard.add(login); #добавляем кнопку в клавиатуру
        bot.send_message(message.from_user.id, text="Я не знаю с кем говорю", reply_markup=keyboard)

@bot.message_handler(commands=['reg'])
def reg(message):
    global chat_id, name,surname,age, status
    chat_id= message.from_user.id
    name, surname, age, tg_id, status=repository.getPersonById(chat_id)
    if chat_id==tg_id:
        bot.send_message(message.from_user.id, "Ты уже зарегестрирован: "+name)
    else: 
        bot.send_chat_action(chat_id=message.from_user.id, action = 'typing')
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name

@bot.message_handler(content_types=['text'])
def messages(message):
    global chat_id, name,surname,age, status
    chat_id= message.from_user.id
    name, surname, age, tg_id, status=repository.getPersonById(chat_id)
    if message.text.lower() in hello and chat_id==tg_id:
            bot.send_message(message.from_user.id, 'Вечер в хату! '+name)

@bot.message_handler(content_types=['voice'])  
def voices(message):
    # fileID=message.voice.file_id
    # file=bot.get_file(fileID)
    # down_file=bot.download_file(file.file_path)
    # with open('audio.ogg', 'wb') as f:
    #     f.write(down_file)
    # #process=subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])

    # os.system("ffmpeg -i audio.ogg audio.wav")

    # file_ = sr.AudioFile('audio.wav')
    recognizer = sr.Recognizer()
    # k=Kate()
    # with file_ as source:
    #     audio = recognizer.record(source)
    #     text=k.callback(recognizer, audio)
    #     bot.send_message(message.from_user.id, text)
    filename = "qwerty"
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recognizer(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)


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
            bot.register_next_step_handler(call.message, reg)




bot.polling(none_stop=True, interval=0)



