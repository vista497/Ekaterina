import ekaterina
import speech_recognition as sr

Kate = ekaterina.Kate

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