from TTS.api import TTS
import subprocess


class TTSsys():
    def __init__(self) -> None:
        self._tts_initializer()

    def _tts_initializer(self):
        # List available 🐸TTS models and choose the first one
        model_name = TTS.list_models()[0]
        # Init TTS
        self.tts = TTS(model_name)

    def tts_runner(self, text='Hello, how are you doing?'):
        with open('output/output.log', 'a') as f:
            f.write(text + '\n')
        output_file = 'output/output.wav'

        # Run TTS
        # ❗ Since this model is multi-speaker and multi-lingual,
        # we must set the target speaker and the language
        self.tts.tts_to_file(
            text=text,
            speaker=self.tts.speakers[0],
            language=self.tts.languages[0],
            file_path=output_file,
            #  emotion='happy',
            speed=1.5
        )

        # Run local terminal audio program with .wav
        subprocess.call(['play', f'{output_file}'])
