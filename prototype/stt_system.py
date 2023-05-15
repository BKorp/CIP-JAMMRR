import speech_recognition as sr
from datetime import datetime


class SpeechRec():
    def __init__(self) -> None:
        self.r = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:
            print('Listening...')
            # r.pause_threshold = 1
            self.r.energy_threshold = 3980
            self.r.dynamic_energy_threshold = True
            timestamp = datetime.now()
            audio = self.r.listen(source)

            try:
                print('Recognizing...')
                # query = self.r.recognize_whisper(audio, language='english')
                query = self.r.recognize_google(audio, language='english')
                # print(query.lstrip())
                return query.lstrip(), timestamp
            except Exception as e:
                print(e)

