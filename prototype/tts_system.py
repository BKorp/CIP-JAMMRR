from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime
import sys


def text_to_speech(text: str = 'Hello, how are you doing?',
                   tld: str = 'com.au') -> str:
    '''Converts a given string to audio using a given top level domain
    to set the accent of the english audio output.
    Returns a timestamp of the time of utterance.
    '''
    tld_list = ['com.au', 'us']
    if tld in tld_list:
        tts = gTTS(text, tld='com.au', lang_check=False)
    else:
        tts = gTTS(text)

    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    ttsaudio = AudioSegment.from_file(fp)
    timestamp = datetime.now()
    play(ttsaudio)

    return timestamp


def main():
    args = sys.argv
    if len(args) < 2:
        text_to_speech('This is a TTS test sentence. '
                       'I hope you can understand and hear what I am saying.')
    else:
        text_to_speech(args[1])


if __name__ == '__main__':
    main()
