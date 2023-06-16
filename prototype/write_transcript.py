import pandas as pd


class Transcriber():
    def __init__(self, start_time):
        self.df = pd.DataFrame(columns=['', 'time', 'speaker', 'utterance'])
        self.id = 0
        self.start_time = start_time    # start time of the conversation

    def update_transcription(self, utterance, timestamp, jammr=True):
        """This function updates the transcript when
        an utterance is produced by JAMMR or SNOOP by
        adding it to a Pandas DataFrame."""
        if jammr:
            speaker = 'JAM_OUT'
        else:
            speaker = 'SNO_IN'

        data = [{'': self.id, 'time': timestamp,
                 'speaker': speaker, 'utterance': utterance}]

        # add the new data to the dataframe
        updated_df = pd.concat([self.df, pd.DataFrame(data)])
        self.df = updated_df
        self.id += 1

    def convert_to_csv(self):
        """This function converts the transcript of the
        conversation that is stored in a Pandas DataFrame
        to a CSV file"""
        # use the start time of the conversation as the filename
        # for the transcript
        fname = self.start_time.strftime('%d-%m-%Y_%H_%M_%S') + '.csv'
        self.df.to_csv(fname, index=False)
