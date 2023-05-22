import speech_recognition as sr
from datetime import datetime


class SpeechRec():
    def __init__(self) -> None:
        self.r = sr.Recognizer()

    def listen(self, t):

        with sr.Microphone() as source:
            # print('=== Listening...')
            self.r.adjust_for_ambient_noise(source)
            timestamp = datetime.now()
            try:
                if t[0] == 'greeting':
                    return None, None
                print('⏳ JAMMRR is trying to listen & understand... ⏳')
                audio = self.r.listen(source, timeout=3, phrase_time_limit=10)

                # print('=== Recognizing...')
                query = self.r.recognize_google(audio, language='english')

                return query.lstrip(), timestamp

            except:
                return self.listen(t)
