
import speech_recognition as sr # распознавание пользовательской речи (Speech-To-Text)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os  # работа с файловой системой

import pyttsx3
from fuzzywuzzy import fuzz
import time
import datetime
import requests
import webbrowser
import repository_ekaterina as rp
#from selenium.webdriver import Yandex




opts ={
    "name": ('катя', 'эй', 'ну-ка', 'екатерина', 'девочка'),
    "tbr": ('послушай', 'скажи', 'покажи', 'сколько', 'произнеси','открой', 'запусти', 'включи', 'добавь', 'запиши'),
    "cmds":{
        "ctime": ('сколько время', 'время', 'который час'),
        "music":('музыка', 'песня'),
        "url":('сайт')
    }
}

class Kate():

    def __init__(self) -> None:
        self.speak= pyttsx3.init()
        self.repository=rp.Repository()

    def _speak(self, what):
        print(what)
        self.speak.say(what)
        self.speak.runAndWait()
        self.speak.stop()

    def record(self, recognizer, microphone):
        with microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            recognizer.adjust_for_ambient_noise(microphone, duration=2)

            try:
                print("Listening...")
                audio = recognizer.listen(microphone, 5, 5)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except sr.WaitTimeoutError:
                self._speak("Проверь микрофон. Я не разобрала ни слова")
                print("Can you check if your microphone is on, please?")
                return
            try:
                self.callback(recognizer, audio)
            except sr.UnknownValueError:
                pass

    def callback(self,recognizer, audio, tg=False):
            # использование online-распознавания через Google 
            try:
                print("Started recognition...")
                voice = recognizer.recognize_google(audio, language="ru").lower()
                #print (voice)
                if tg:
                    return voice
                if voice.startswith(opts["name"]):
                    cmd = voice

                    for x in opts["name"]:
                        cmd=cmd.replace(x,"").strip()

                    for x in opts["tbr"]:
                        cmd=cmd.replace(x,"").strip()

                    # распознаем и выполняем команду
                    cmd = self.recognize_cmd(cmd)
                    self.execute_cmd(cmd['cmd'])
            except sr.UnknownValueError:
                print (1)

            # в случае проблем с доступом в Интернет происходит попытка 
            # использовать offline-распознавание через Vosk
            except sr.RequestError:
                print("Trying to use offline recognition...")
                recognized = self.use_offline_recognition()
                print(recognized)

    def recognize_cmd(self, cmd):
        RC = {'cmd': '', 'percent': 70}
        for c,v in opts['cmds'].items():
 
            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > RC['percent']:
                    RC['cmd'] = c
                    RC['percent'] = vrt
        return RC

    def execute_cmd(self, cmd):
        if cmd == 'ctime':
        # сказать текущее время
            now = datetime.datetime.now()
            self._speak("Сейчас " + str(now.hour) + ":" + str(now.minute)) 
        if cmd == 'music':
            # запустить что-то
            #file_path = r'C:\windows\system32\cmd.exe'
            #os.system("start "+file_path)
            self._speak("Открываю Яндекс Музыку")
            url='https://music.yandex.ru/'
            webbrowser.open_new(url)

        if cmd == 'url':
            self._speak("Добавляю в свою базу сайт")
            name="яндекс музыка"
            url="https://music.yandex.ru/"
            self.repository.insertUrl(name, url)

    def record_and_recognize_audio(self,*args: tuple):
        """
        Запись и распознавание аудио
        """
        with microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            recognizer.adjust_for_ambient_noise(microphone, duration=2)

            try:
                print("Listening...")
                audio = recognizer.listen(microphone, 5, 5)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except sr.WaitTimeoutError:
                print("Can you check if your microphone is on, please?")
                return

            # использование online-распознавания через Google 
            try:
                print("Started recognition...")
                recognized_data = recognizer.recognize_google(audio, language="ru").lower()

            except sr.UnknownValueError:
                pass

            return recognized_data


if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 1000
    recognizer.pause_threshold = 0.5
    microphone = sr.Microphone()
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        K = Kate(recognizer, microphone)
        # K._speak("Ну привет!")
   # K._speak("Я слушаю, кожаный")
    
        #recognizer.listen_in_background(microphone, K.callback)
    #os.remove("microphone-results.wav")
    while True: 
        
        K.record(recognizer,microphone)       

