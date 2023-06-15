import speech_recognition as sr
import random
from datetime import datetime


class SpeechRec():
    def __init__(self) -> None:
        self.r = sr.Recognizer()

    def listen(self, bot_state: str) -> tuple[str, str] | tuple[None, None]:
        '''Returns a string representing input audio and a timestamp.
        Uses the computer's microphone to listen for audio and converts
        it into text. Returns None, None for states that are not main.
        '''

        with sr.Microphone() as source:
            # print('=== Listening...')
            self.r.adjust_for_ambient_noise(source)
            timestamp = datetime.now()
            try:
                if bot_state[0] == 'greeting':
                    return None, None
                print('⏳ JAMMRR is trying to listen & understand... ⏳')
                audio = self.r.listen(source, timeout=3, phrase_time_limit=10)

                # print('=== Recognizing...')
                query = self.r.recognize_google(audio, language='english')

                return query.lstrip(), timestamp

            except Exception:
                if bot_state == 'make_contact':
                    return None, None

                if bot_state == 'main':
                    return None, None

                return self.listen(bot_state)
