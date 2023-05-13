import speech_recognition as sr


class SpeechRec():
    def __init__(self) -> None:
        self.r = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:
            print('Listening...')
            # r.pause_threshold = 1
            self.r.energy_threshold = 3980
            self.r.dynamic_energy_threshold = True
            audio = self.r.listen(source)

            try:
                print('Recognizing...')
                # query = self.r.recognize_whisper(audio, language='english')
                query = self.r.recognize_google(audio, language='english')
                # print(query.lstrip())
                return query.lstrip()
            except Exception as e:
                print(e)
