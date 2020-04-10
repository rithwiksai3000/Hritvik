from tkinter import *
from tkinter import ttk
import threading
# pip install chatterbot
# pip install chatterbot_corpus
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
#pip install SpeechRecognition
# pip install pyaudio
import pyaudio
import speech_recognition as sr
import os
import playsound
import random
#pip install gtts
from gtts import gTTS

class Chatbot:

    def __init__(self,root):
        self.root = root
        self.root.title("ChatBot")
        self.root.geometry('300x500')
        self.root.resizable(0,0)
        self.root.bind('<Return>',self.enter_pressed)


        # creating and training chat bot

              # chatbot main code ..
        self.bot = ChatBot("Alex")
        # here you can put many answers for bot or you can use a anoyher python file 
        # and make alist of answers in it ..
        # i am doing it here for only a practice purpose ... 

        answers = [
            'hello',
            'hey bro',
            'my name is Alex , i am a bot',
            'my favourite language is Python',
            'i am fine , are you good '
            'No i dont eat ',
            'by ,nice to meet you ',

           ]
        self.trainer = ListTrainer(self.bot)
        # train the bot ...
        self.trainer.train(answers)
        # adding widgets in it 

        self.ent = StringVar()

        self.chatScreen = Frame(self.root).grid()

        scrollbar = Scrollbar(self.chatScreen, orient=VERTICAL)
        scrollbar.place(x=280, y=0, height=420)
        self.chatArea = Listbox(self.chatScreen, bg='white', yscrollcommand=scrollbar.set,fg='blue',font=('arial',10,'bold'))

        self.chatArea.place(x=0, y=0, height=420, width=280)
        scrollbar.config(command=self.chatArea.yview)

        # Entry box for sending message ....

        self.entry = Entry(self.chatScreen, width=40, bd=4, relief='groove',textvariable=self.ent,font=('arial',10,'bold'))

        self.entry.place(x=5, y=425)

        self.send_button = Button(self.chatScreen, text='Send', bg='light green', width=5,command=self.entry_fetch_values)
        self.send_button.place(x=60, y=460)

        self.clear_button = Button(self.chatScreen, text='Clear', bg='light green', width=5,command=lambda : self.chatArea.delete(0,END))
        self.clear_button.place(x=130, y=460)


        self.speak_button = Button(self.chatScreen, text='Speak', bg='light green', width=5,command=self.call_get_speech_input)
        self.speak_button.place(x=200, y=460)

    def entry_fetch_values(self):
        entry_value = self.ent.get()
        entry_value = '\n' + 'You: '+entry_value
        self.chatArea.insert(END,entry_value)
        self.response(entry_value[6:])
        self.ent.set("")

    def response(self,entry_value):
        query = entry_value
        answer = self.bot.get_response(query)
        entry_value = '\n' + 'Bot: ' + str(answer)
        self.chatArea.insert(END, entry_value)

        audio_string = entry_value[6:]

        self.voice_output(audio_string)


    def call_get_speech_input(self):
    	threading.Thread(target=self.get_speech_input).start()



    def get_speech_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            voice_data=''
            try:
                voice_data = r.recognize_google(audio)
            except sr.UnknownValueError:
                print('Did not get that')
            
            except sr.RequestError:
                print("Server is down")

        self.enter_voice_data_into_list(voice_data)

    def call_voice_output(self,audio_string):
    	threading.Thread(target = self.voice_output,args=(audio_string,)).start()

    def voice_output(self,audio_string):
        tts = gTTS(text=audio_string,lang='en')
        r = random.randint(1,1000000)
        audio_file = 'audio-'+str(r)+'.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        path = os.getcwd()
        os.chdir(path)
        os.remove(audio_file)

    def enter_voice_data_into_list(self,voice_data):
        entry_value = voice_data
        entry_value = '\n' + 'You: '+entry_value
        self.chatArea.insert(END,entry_value)
        self.response(entry_value[6:])




    def enter_pressed(self,event):
        self.send_button.invoke()
        self.ent.set("")


if __name__ == "__main__":
    root = Tk()
    Chatbot(root)
    root.mainloop()
