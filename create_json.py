#plik służący uzupełnieniu informacji o badaniu
# %% ZALADOWANIE ODPOWIEDNICH BIBLIOTEK
"""
Modul zawierajacy fragmenty kodu pozwalajace na utworzenie pliku JSN zawierającego opis badania
"""
import json
import matplotlib.pyplot as plt
import numpy as np

from examination import Examination
# %% WIZUALIZACJA MARKEROW

exam_ids = ['HB086', 'HB090', 'HB091']
exam = Examination(exam_ids[2])

plt.plot(exam.signals[["MARKER"]])

m = exam.signals[["MARKER"]]
idx = np.where(np.array(m) == 1)
t = exam.signals['TIME'].loc[exam.signals['MARKER'] == 1]
# %% UZUPELNIENIE JSN
num = "086"

# uzupelnienie legendy markerow
dictionary = {
    "file_number": num, #numer pliku
    "start_warmup_marker": 2, #rozpoczecie rozgrzewki
    "stop_warmup_marker": 3, #koniec rozgrzewki
    "start_exercise_marker": 3, #rozpoczecie proby wysikowej
    "stop_exercise_marker": 4, #koniec proby wysilkowej
    "sex": "M", #plec
    "start_power": 90, #moc poczatkowa [Watt]
}

# serializacja json
json_object = json.dumps(dictionary, indent=4)
 
# zapis
with open(f"./data/HB{num}.json", "w", encoding='utf-8') as outfile:
    outfile.write(json_object)
# %%
# 74232 133155 154253 300328