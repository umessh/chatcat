from preprocessor import preprocessor
import pandas as pd
import csv
from config import BLOCK_DIVIDER
from collections import Counter

class analyser(object):

    def __init__(self, file_path):
        file_preprocessor = preprocessor(file_path)
        self._processed_file = file_preprocessor.create_processed_data()
        dtypes= file_preprocessor.get_dtypes()
        self._df = pd.read_csv(self._processed_file, engine ='python', quotechar='"', dtype= dtypes, quoting=csv.QUOTE_NONNUMERIC)


    def get_users(self):
        users = self._df.user.unique()
        return users

    def texts_per_user(self):
        user_texts = self._df.groupby('user').agg(['count'])
        for item in user_texts.iterrows():
            print "%s's total message count is %s"%(item[0],item[1][0])
        print BLOCK_DIVIDER

    def most_texted_day_of_week(self):
        user_texts = self._df[['user','weekday','chat_text']].groupby(['user','weekday']).agg(['count'])
        print user_texts
        print BLOCK_DIVIDER

    def most_used_words_by_user(self):
        user_texts = self._df[['user','chat_text']].groupby('user')
        #print user_texts
        #user_word_counter = {}
        for name,group in user_texts:
            print name
            c1 = Counter()
            for row in group.iterrows():
                #print row[1][1]
                c2 = Counter([word.lower() for word in row[1][1].split(' ')])
                c1 = c1 + c2
            print c1.most_common(20)
        print BLOCK_DIVIDER

    def analyse_data(self):
        print 'Chat data summary'
        print BLOCK_DIVIDER
        print 'Users list', self.get_users()
        print BLOCK_DIVIDER
        #print self._df.describe()
        #print BLOCK_DIVIDER
        self.texts_per_user()
        self.most_texted_day_of_week()
        self.most_used_words_by_user()


if __name__ == '__main__':
    x = analyser('/home/messy/Downloads/Data Science from Scratch/test/Personal.txt')
    x.analyse_data()

