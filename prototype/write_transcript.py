import pandas as pd
from datetime import datetime

class Transcriber():
    def __init__(self):
        self.df = pd.DataFrame(columns=['', 'time', 'speaker', 'utterance'])
        self.id = 0

    def update_transcription(self, utterance, jammr=True):
        if jammr:
            speaker = 'JAM_OUT'
        else:
            speaker = 'SNO_IN'
        data = [{'': self.id, 'time': str(datetime.now()), 'speaker': speaker, 'utterance': utterance}]

        updated_df = pd.concat([self.df, pd.DataFrame(data)])
        self.df = updated_df
        self.id += 1

    def convert_to_csv(self):
        self.df.to_csv('transcript.csv', index=False)

