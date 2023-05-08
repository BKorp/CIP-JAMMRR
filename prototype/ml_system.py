from transformers import pipeline
from stt_system import stt_sys
from tts_system import TTSsys


class LanguageModelSys():
    def __init__(self, model_str: str, ml_setup: str, ml_task: str='text2text-generation') -> None:
        self.model_str = model_str

        if ml_setup == 'basic':
            self.sys = self._basic_sys(ml_task)

    def chat(self, inp_sent) -> list[str]:
        return [sent['generated_text'].lstrip() for sent in self.sys(inp_sent)]

    def _basic_sys(self, ml_task='text2text-generation'):
        return pipeline(ml_task, self.model_str)


def chat_printer(inp_list):
    print('\n'.join(inp_list))


def main():
    blenderbot = LanguageModelSys('facebook/blenderbot-400M-distill', 'basic')
    tts = TTSsys()
    # chat_printer(blenderbot.chat('what is your name?'))
    # chat_printer(blenderbot.chat('Do you like music?'))
    # chat_printer(blenderbot.chat(['hello', 'I\'m doing fine, what are you going to do today?']))
    # chat_printer(blenderbot.chat(stt_sys()))
    # print(blenderbot.chat(stt_sys()))

    tts.tts_runner(blenderbot.chat(stt_sys())[0])


if __name__ == '__main__':
    main()