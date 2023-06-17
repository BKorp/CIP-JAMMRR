import pickle
import pandas as pd
from transformers import pipeline
from transformers import T5Tokenizer, TFT5ForConditionalGeneration
from stt_system import SpeechRec
from tts_system import text_to_speech
from write_transcript import Transcriber
from datetime import datetime
from pathlib import Path
from dialog_tag import DialogTag
import threading as th
import time
import regex as re


class LanguageModelSys():
    def __init__(self,
                 model_str: str,
                 ml_setup: str,
                 ml_task: str='text2text-generation') -> None:
        self.model_str = model_str

        if ml_setup == 'basic':
            self.sys = self._basic_sys(ml_task)

    def chat(self, inp_sent: str | list[str]) -> list[str]:
        '''Takes a string or a list of strings and returns
        the answer of a seq2seq language model as a list.
        '''
        return [sent['generated_text'].lstrip() for sent in self.sys(inp_sent)]

    def _basic_sys(self, ml_task='text2text-generation'):
        '''Takes a machine learning task and returns
        a Transformers pipeline for the language model
        specified in the object's self.model_str.
        '''
        return pipeline(ml_task, self.model_str)


class ModeModerator():
    def __init__(self) -> None:
        pass

    def _equal_rand(self, choices: pd.DataFrame) -> tuple[str, pd.DataFrame]:
        '''Returns a random choice from a given dataframe with scores.
        It also returns an updated dataframe with new scores.
        The choice is taken randomly from all if all scores are
        the same, or where the score is smaller than max otherwise.
        '''
        if len(choices.score.unique()) == 1:
            choice = choices.sent.sample().to_string(index=False)
            choices.loc[choices.sent == choice, 'score'] += 1
        else:
            choice = choices[choices.score < choices.score.max()].sent.sample().to_string(index=False)
            choices.loc[choices.sent == choice, 'score'] = choices.score.max()

        return choice, choices

    def initiate_conv(self) -> str:
        '''Imports a greeting.csv with choices and scores
        as a Dataframe and returns a random choice from
        said dataframe.
        '''
        f_name = 'greeting.csv'
        choices = pd.read_csv(f_name, sep='\t', names=['sent', 'score'])
        choice, choices = self._equal_rand(choices)
        choices.to_csv(f_name, sep='\t', header=False, index=False)

        return choice

    # def end_conv(self):
        # choice_lst =
        # self.tts(self._equal_rand(choice_lst))


class DetectState():
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model
        self.dialog_tag_model = DialogTag('distilbert-base-uncased')

        self.opening_statement = ['Conventional-opening']
        self.closing_statement = ['Conventional-closing']
        self.question = ['Wh-Question', 'Declarative Yes-No-Question', 'Backchannel in question form', 'Open-Question',
                     'Rhetorical-Questions', 'Tag-Question', 'Declarative Wh-Question', 'Yes-No-Question']
        self.answer = ['Yes answers', 'No answers', 'Affirmative non-yes answers', 'Negative non-no answers',
                   'Dispreferred answers']

        self.state = 'main'
        self.is_question = False

    def add_punctuation(self, utt):
        """This function adds punctuation to an utterance."""
        inp = self.tokenizer.encode("punctuate: " + utt, return_tensors="tf")
        result = self.model.generate(inp)
        return self.tokenizer.decode(result[0], skip_special_tokens=True)

    def split_sentences(self, utt):
        """This function splits sentences on punctuation marks (,.?)"""
        sentence_parts = re.split('[,.?!]', utt)
        return sentence_parts

    def detect_intent(self, utt):
        """This function detects the intent of an utterance."""
        with_punkt = self.add_punctuation(utt)
        sentence_parts = self.split_sentences(with_punkt)
        intents = []

        for part in sentence_parts:
            if part != '':
                intents.append(self.dialog_tag_model.predict_tag(part))

        return intents

    def detect_state(self, utt):
        """This function detects whether an utterance is a greeting, goodbye or question
        so that the chatbot can move to the correct state."""
        intents = self.detect_intent(utt)

        # if [intent for intent in intents if intent in self.opening_statement]:
        #     self.state = 'greeting'
        if [intent for intent in intents if intent in self.closing_statement]:
            self.state = 'closing'
        else:
            self.state = 'main'

        if [intent for intent in intents if intent in self.question]: # detect whether utterance is question or not
            self.is_question = True
        else:
            self.is_question = False

        return self.state, self.is_question

    def return_state(self):
        return self.state, self.is_question

    def update_state(self, state):
        self.state = state
        return self.state


def thread_greeter(bot_state, n=10):
    if bot_state[-1] < 1:
        time.sleep(n)
        bot_state[0] = 'greeting'


def main():
    start_time = datetime.now()

    bot_name = 'blenderbot'
    if not Path(f'{bot_name}.pkl').is_file():
        blenderbot = LanguageModelSys('facebook/blenderbot-400M-distill', 'basic')
        pickle.dump(blenderbot, open(f'{bot_name}.pkl', 'wb'))
    else:
        blenderbot = pickle.load(open(f'{bot_name}.pkl', 'rb'))

    # tokenizer and model for adding punctuation to inp utterance
    tokenizer = T5Tokenizer.from_pretrained('SJ-Ray/Re-Punctuate')
    punkt_model = TFT5ForConditionalGeneration.from_pretrained('SJ-Ray/Re-Punctuate')

    script_transcriber = Transcriber(start_time)

    speech_to_text = SpeechRec()

    # bot_state = ['main', -1]
    # thr = th.Thread(target=thread_greeter, args=(bot_state, 5), daemon=True)
    # thr.start()

    state_detector = DetectState(tokenizer, punkt_model)
    print('❗ JAMMRR has finished preparing! ❗')
    bot_state, is_question = state_detector.return_state()
    make_contact = True

    while True:
        if bot_state == 'make_contact':
            while make_contact:
                inp, timestamp = speech_to_text.listen(bot_state)
                if inp:
                    make_contact = False
                    bot_state = 'greeting'
                    state_detector.update_state(bot_state)
                else:
                    out = 'Hello, is anybody there?'
                    print('\n', '🎶 JAMMRR: ', out, '🎶', '\n')
                    timestamp = text_to_speech(out)
                    script_transcriber.update_transcription(out, timestamp)

        while bot_state == 'main':
            inp, timestamp = speech_to_text.listen(bot_state)
            if not inp:
                out = 'Are you still here?'
                print('\n', '🎶 JAMMRR: ', out, '🎶', '\n')
                timestamp = text_to_speech(out)
                script_transcriber.update_transcription(out, timestamp)
                break
            script_transcriber.update_transcription(inp, timestamp, False)
            bot_state, is_question = state_detector.detect_state(inp)

            out = blenderbot.chat(inp)[0]
            print('\n', '🎶 JAMMRR: ', out, '🎶', '\n')
            timestamp = text_to_speech(out)
            script_transcriber.update_transcription(out, timestamp)

            script_transcriber.convert_to_csv()


        if bot_state == 'greeting':
            out = ModeModerator().initiate_conv()
            print('\n', '🎶 JAMMRR: ', out, '🎶', '\n')
            timestamp = text_to_speech(out)
            script_transcriber.update_transcription(out, timestamp)

            script_transcriber.convert_to_csv()
            bot_state = 'main'

        if bot_state == 'closing':
            out = 'It was nice talking to you!'
            print('\n', '🎶 JAMMRR: ', out, '🎶', '\n')
            timestamp = text_to_speech(out)
            script_transcriber.update_transcription(out, timestamp)

            script_transcriber.convert_to_csv()
            bot_state = 'main'

            # end conversation

        if is_question:
            pass
            # answer question; do not initiate new topic (before answering question)

if __name__ == '__main__':
    main()
