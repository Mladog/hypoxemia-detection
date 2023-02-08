"""
Modul odpowiedzialny za obsługę klasy Examination 
"""
import json
import pandas as pd
from breath_signal import BreathSignal
from constants import LOCAL_EXAMINATION_DIRECTORY, COMS_SIGNAL_EXT, PHYSIONET_SIGNAL_EXT, JSON_EXT


class Examination():
    """
    Klasa odpowiadajaca za utworzenie klasy Examination, pozwalajaca na wydobycie podstawowych 
    informacji o sygnale i wyciagnieciu odpowiednich jego fragmentow
    """
    def __init__(self, exam_id, exam_fs = 250, source = "COMS"):
        self.path = LOCAL_EXAMINATION_DIRECTORY
        self.source = source
        self.exam_id = exam_id
        self.exam_fs = exam_fs
        if self.source == "COMS":
            self.signals = pd.read_csv(f'{self.path}/{self.exam_id}{COMS_SIGNAL_EXT}',
                                        delimiter = ',', header=None)
            self.signals.columns = ["TIME", "RESP", "MARKER"]
        elif self.source == "physionet":
            self.signals = pd.read_csv(f'{self.path}/{self.exam_id}{PHYSIONET_SIGNAL_EXT}',
                                        delimiter = ',', header=None)
            self.signals.columns = ["Time", "RESP", "PLETH", "V", "AVR", "II"]
        else:
            raise ValueError(f'{self.source} wrong, use "COMS" or "physionet"')

    def get_breath_signal_all(self):
        """
        Funkcja zwracająca cały zarejestrowany sygnał w postaci obiektu klasy BreathSignal
        """
        return BreathSignal(self.signals[["RESP"]], self.exam_fs)

    def get_json(self):
        """
        Funkcja zwracająca cały zarejestrowany sygnał w postaci obiektu klasy BreathSignal
        """
        with open(f'{self.path}/{self.exam_id}{JSON_EXT}',  encoding='utf-8') as file:
            data = json.load(file)
        return data

    def get_signal_warmup(self):
        """
        Funkcja zwracająca sygnał zarejestrowany podczas rozgrzewki 
        w postaci obiektu klasy BreathSignal
        """
        jsn = self.get_json()
        boundries = [jsn["start_warmup_marker"], jsn["stop_warmup_marker"]]
        return BreathSignal(self.signals["RESP"].loc[boundries[0]:boundries[1]], self.exam_fs)

    def get_signal_exercise(self):
        """
        Funkcja zwracająca sygnał zarejestrowany podczas próby wysiłkowej 
        w postaci obiektu klasy BreathSignal
        """
        jsn = self.get_json()
        boundries = [jsn["start_exercise_marker"], jsn["stop_exercise_marker"]]
        print(boundries)
        return BreathSignal(self.signals["RESP"].loc[boundries[0]:boundries[1]], self.exam_fs)

    def get_signal_cooldown(self):
        """
        Funkcja zwracająca sygnał zarejestrowany w trakcie cooldownu 
        w postaci obiektu klasy BreathSignal
        """
        jsn = self.get_json()
        return BreathSignal(self.signals["RESP"].loc[jsn["stop_exercise_marker"]:], self.exam_fs)
