from email import header
from breath_signal import BreathSignal
from constants import *
import pandas as pd
import numpy as np

class Examination():

    def __init__(self, exam_id, fs = 125):
        self.path = LOCAL_EXAMINATION_DIRECTORY
        self.exam_id = exam_id
        self.fs = fs

    def get_breath_signal(self):
        signals = pd.read_csv(f'{self.path}/{self.exam_id}{AIRFLOW_SIGNAL_EXT}', delimiter = ',')
        return BreathSignal(signals[[' RESP']], self.fs)

