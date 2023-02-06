from email import header
from breath_signal import BreathSignal
from constants import *
import pandas as pd
import numpy as np

class Examination():

    def __init__(self, exam_id, fs = 250, source = "COMS"):
        self.path = LOCAL_EXAMINATION_DIRECTORY
        self.source = source
        self.exam_id = exam_id
        self.fs = fs

    def get_breath_signal(self):
        if self.source == "COMS":
            signals = pd.read_csv(f'{self.path}/{self.exam_id}{AIRFLOW_SIGNAL_EXT}', delimiter = ',')
            signals.columns = ["TIME", "RESP", "MARKER"]
            return BreathSignal(signals[["RESP"]], self.fs)
        
        elif self.source == "physionet":
            signals = pd.read_csv(f'{self.path}/{self.exam_id}{AIRFLOW_SIGNAL_EXT}', delimiter = ',')
            return BreathSignal(signals[[" RESP"]], self.fs)

        else:
            raise ValueError('{source} wrong, use "COMS" or "physionet"'.format(source=repr(self.source)))
