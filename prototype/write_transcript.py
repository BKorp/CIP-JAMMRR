import pandas as pd


class Transcriber():
    def __init__(self):
        self.df = pd.DataFrame(columns=['', 'time', 'speaker', 'utterance'])
        self.id = 0

    def update_transcription(self, utterance, timestamp, jammr=True):
        if jammr:
            speaker = 'JAM_OUT'
        else:
            speaker = 'SNO_IN'
        data = [{'': self.id, 'time': timestamp, 'speaker': speaker, 'utterance': utterance}]

        updated_df = pd.concat([self.df, pd.DataFrame(data)])
        self.df = updated_df
        self.id += 1

    def convert_to_csv(self):
        self.df.to_csv('transcript.csv', index=False)

