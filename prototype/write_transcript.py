import pandas as pd


class Transcriber():
    def __init__(self, start_time):
        self.df = pd.DataFrame(columns=['', 'time', 'speaker', 'utterance'])
        self.id = 0
        self.start_time = start_time

    def update_transcription(self, utterance, timestamp, jammr=True):
        if jammr:
            speaker = 'JAM_OUT'
        else:
            speaker = 'SNO_IN'
        data = [{'': self.id, 'time': timestamp,
                 'speaker': speaker, 'utterance': utterance}]

        updated_df = pd.concat([self.df, pd.DataFrame(data)])
        self.df = updated_df
        self.id += 1

    def convert_to_csv(self):
        fname = self.start_time.strftime('%d-%m-%Y_%H_%M_%S') + '.csv'
        self.df.to_csv(fname, index=False)
