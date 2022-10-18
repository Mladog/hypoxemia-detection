from constants import *
import pandas as pd

class Examination():

    def __init__(self, exam_id):
        self.path = LOCAL_EXAMINATION_DIRECTORY
        self.exam_id = exam_id

    def get_breath_signal(self):
        breath_path = f'{self.path}/{self.exam_id}{AIRFLOW_SIGNAL_EXT}'
        breath_signal = pd.read_csv(breath_path)
        return breath_signal