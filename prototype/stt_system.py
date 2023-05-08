import speech_recognition as sr

r = sr.Recognizer()

def stt_sys():

    with sr.Microphone() as source:
        print('Listening...')
        # r.pause_threshold = 1
        r.energy_threshold = 3980
        r.dynamic_energy_threshold = True
        audio = r.listen(source)

        try:
            print('Recognizing...')
            query = r.recognize_whisper(audio, language='english')
            # print(query.lstrip())
            return query.lstrip()
        except Exception as e:
            print(e)

