import pickle
import pandas as pd
from transformers import pipeline
from stt_system import SpeechRec
from tts_system import text_to_speech
from write_transcript import Transcriber
from pathlib import Path
import threading as th
import time


class LanguageModelSys():
    def __init__(self,
                 model_str: str,
                 ml_setup: str,
                 ml_task: str='text2text-generation') -> None:
        self.model_str = model_str

        if ml_setup == 'basic':
            self.sys = self._basic_sys(ml_task)

    def chat(self, inp_sent) -> list[str]:
        return [sent['generated_text'].lstrip() for sent in self.sys(inp_sent)]

    def _basic_sys(self, ml_task='text2text-generation'):
        return pipeline(ml_task, self.model_str)


class ModeModerator():
    def __init__(self) -> None:
        pass

    def _equal_rand(self, choices):
        if len(choices.score.unique()) == 1:
            choice = choices.sent.sample().to_string(index=False)
            choices.loc[choices.sent == choice, 'score'] += 1
        else:
            choice = choices[choices.score < choices.score.max()].sent.sample().to_string(index=False)
            choices.loc[choices.sent == choice, 'score'] = choices.score.max()

        return choice, choices

    def initiate_conv(self):
        f_name = 'greeting.csv'
        choices = pd.read_csv(f_name, sep='\t', names=['sent', 'score'])
        choice, choices = self._equal_rand(choices)
        choices.to_csv(f_name, sep='\t', header=False, index=False)

        return choice

    # def end_conv(self):
        # choice_lst =
        # self.tts(self._equal_rand(choice_lst))


def thread_greeter(bot_state, n=10):
    if bot_state[-1] < 1:
        time.sleep(n)
        bot_state[0] = 'greeting'


def main():
    bot_name = 'blenderbot'
    if not Path(f'{bot_name}.pkl').is_file():
        blenderbot = LanguageModelSys('facebook/blenderbot-400M-distill', 'basic')
        pickle.dump(blenderbot, open(f'{bot_name}.pkl', 'wb'))
    else:
        blenderbot = pickle.load(open(f'{bot_name}.pkl', 'rb'))

    script_transcriber = Transcriber()

    speech_to_text = SpeechRec()

    bot_state = ['main', -1]
    thr = th.Thread(target=thread_greeter, args=(bot_state, 5), daemon=True)
    thr.start()

    while True:
        while bot_state[0] == 'main':
            bot_state[-1] += 1

            inp, timestamp = speech_to_text.listen(bot_state)
            if inp == None:
                break
            script_transcriber.update_transcription(inp, timestamp, False)

            out = blenderbot.chat(inp)[0]
            print('JAMMR: ', out)
            timestamp = text_to_speech(out)
            script_transcriber.update_transcription(out, timestamp)

            script_transcriber.convert_to_csv()

        if bot_state[0] == 'greeting':
            bot_state[-1] += 1

            out = ModeModerator().initiate_conv()
            print('JAMMR: ', out)
            timestamp = text_to_speech(out)
            script_transcriber.update_transcription(out, timestamp)

            script_transcriber.convert_to_csv()
            bot_state[0] = 'main'


if __name__ == '__main__':
    main()
