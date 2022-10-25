from email import header
from breath_signal import BreathSignal
from constants import *
import pandas as pd
import numpy as np

class Examination():

    def __init__(self, exam_id):
        self.path = LOCAL_EXAMINATION_DIRECTORY
        self.exam_id = exam_id

    def get_breath_signal(self):
        return BreathSignal(np.genfromtxt(f'{self.path}/{self.exam_id}{AIRFLOW_SIGNAL_EXT}', delimiter = ','))

    def get_ecg_signal(self):
        return np.genfromtxt(f'{self.path}/{self.exam_id}{ECG_SIGNAL_EXT}', delimiter = ',')