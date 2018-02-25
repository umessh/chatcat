from config import WORKING_DIR, DATA_DIR_NAME
from dateutil.parser import parse
from datetime import datetime
import os

class preprocessor(object):

    def __init__(self, file_path):
        """
        Args:
            file_path: chat file path to run pre-processing
        """
        self._file_path = file_path


    def create_processed_data(self, processed_data_file_name=None):
        """
        Args:
            processed_data_file_name: processed file name
        """
        data_dir = WORKING_DIR + DATA_DIR_NAME
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        if not processed_data_file_name:
           outfile_name = 'processed_' + self._file_path.split('/')[-1]
        else:
            outfile_name = processed_data_file_name
        outfile_name = data_dir + outfile_name

        if os.path.exists(outfile_name):
            return outfile_name

        with open(outfile_name,'w') as outfile:
            header = '"date","time","weekday","user","chat_text","word_count","char_count"\n'
            new_lines = []
            out_new_lines = []
            out_new_lines.append(header)
            with open(self._file_path,'r') as infile:
                for line in infile:
                    try:
                        datetime_end_index = line.index(' - ')
                        new_lines.append(line)
                    except ValueError,e:
                        #If it is Value error then it is continuation of previous line
                        new_lines[-1] = new_lines[-1].rstrip('\n') + ' ' + line
                for line in new_lines:
                    datetime_end_index = line.index(' - ')
                    username_end_index = line.index(': ')
                    datetime_value = line[:datetime_end_index]
                    username_value = line[datetime_end_index+3:username_end_index]
                    chat_value = line[username_end_index+2:].replace('"','').rstrip('\n')
                    day_value = str(parse(datetime_value, dayfirst=False).weekday())
                    datetime_txt = datetime_value.split(',')
                    word_count = str(len(chat_value.split()))
                    char_count = str(len(line))
                    out_new_lines.append('"' +datetime_txt[0] + '","' +datetime_txt[1].strip(' ') + '",'+ day_value + ',"' +\
                                         username_value  + '","' + chat_value + '",' + word_count + ',' + char_count + '\n')
            outfile.writelines(out_new_lines)

        return outfile_name

    def get_dtypes(self):
        return  {'date':datetime, 'time':datetime, 'weekday':int, 'user':str, 'chat_text':str,
                 'word_count':int, 'char_count':int}

    def get_headers(self):
        return ["date", "time", "weekday", "user", "chat_text", "word_count", "char_count"]