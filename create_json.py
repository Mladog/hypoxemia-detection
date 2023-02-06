#plik służący uzupełnieniu informacji o badaniu
# %% ZALADOWANIE ODPOWIEDNICH BIBLIOTEK
from examination import Examination
import matplotlib.pyplot as plt
import json


"""
TODO:
zmiana sekund na numer probki
"""

# %% WIZUALIZACJA MARKEROW
exam_ids = ['HB086', 'HB090', 'HB091']
exam = Examination(exam_ids[2])

plt.plot(exam.signals[["MARKER"]])

t = exam.signals['TIME'].loc[exam.signals['MARKER'] == 1]
# %% UZUPELNIENIE JSN

number = ""

# uzupelnienie legendy markerow
dictionary = {
    "file_number": number, #numer pliku
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
with open(f"./data/HB{number}.json", "w") as outfile:
    outfile.write(json_object)
# %%
