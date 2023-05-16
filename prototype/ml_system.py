import pickle
from transformers import pipeline
from stt_system import SpeechRec
from tts_system import text_to_speech
from write_transcript import Transcriber
from datetime import datetime
from pathlib import Path


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


def main():
    start_time = datetime.now()

    bot_name = 'blenderbot'
    if not Path(f'{bot_name}.pkl').is_file():
        blenderbot = LanguageModelSys('facebook/blenderbot-400M-distill', 'basic')
        pickle.dump(blenderbot, open(f'{bot_name}.pkl', 'wb'))
    else:
        blenderbot = pickle.load(open(f'{bot_name}.pkl', 'rb'))

    script_transcriber = Transcriber(start_time)

    speech_to_text = SpeechRec()
    inp, inp_timestamp = speech_to_text.listen()
    script_transcriber.update_transcription(inp, inp_timestamp, False)

    out = blenderbot.chat(inp)[0]
    out_timestamp = text_to_speech(out)
    script_transcriber.update_transcription(out, out_timestamp)

    script_transcriber.convert_to_csv()


if __name__ == '__main__':
    main()
