import speech_recognition as sr
from datetime import datetime


class SpeechRec():
    def __init__(self) -> None:
        self.r = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:
            print('Listening...')
            self.r.adjust_for_ambient_noise(source)
            timestamp = datetime.now()
            audio = self.r.listen(source, phrase_time_limit=5)

            try:
                print('Recognizing...')
                # query = self.r.recognize_whisper(audio, language='english')
                query = self.r.recognize_google(audio, language='english')
                # print(query.lstrip())
                return query.lstrip(), timestamp
            except Exception as e:
                #print(e)
                return self.listen()
