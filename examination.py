from email import header
from breath_signal import BreathSignal
from constants import *
import pandas as pd
import numpy as np
import json

class Examination():

    def __init__(self, exam_id, fs = 250, source = "COMS"):
        self.path = LOCAL_EXAMINATION_DIRECTORY
        self.source = source
        self.exam_id = exam_id
        self.fs = fs
        if self.source == "COMS":
            self.signals = pd.read_csv(f'{self.path}/{self.exam_id}{COMS_SIGNAL_EXT}', delimiter = ',', header=None)
            self.signals.columns = ["TIME", "RESP", "MARKER"]
        elif self.source == "physionet":
            self.signals = pd.read_csv(f'{self.path}/{self.exam_id}{PHYSIONET_SIGNAL_EXT}', delimiter = ',', header=None)
            self.signals.columns = ["Time", "RESP", "PLETH", "V", "AVR", "II"]
        else:
            raise ValueError('{source} wrong, use "COMS" or "physionet"'.format(source=repr(self.source)))

    def get_breath_signal_all(self):
        return BreathSignal(self.signals[["RESP"]], self.fs)

    def get_json(self):
        with open(f'{self.path}/{self.exam_id}{JSON_EXT}') as f:
            data = json.load(f)
        return data

    def get_signal_warmup(self):
        jsn = self.get_json()
        boundries = [jsn["start_warmup_marker"]:jsn["stop_warmup_marker"]]
        return BreathSignal(self.signals["RESP"].iloc[boundries], self.fs)

    def get_signal_exercise(self):
        pass

    def get_signal_cooldown(self):
        pass

        
