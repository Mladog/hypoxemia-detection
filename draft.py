"""
brudnopis
"""
# %% IMPORT REQUIRED LIBRARIES
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
from examination import Examination

# %% Get Examination
exam_ids = ['HB086', 'HB090', 'HB091']
exam = Examination(exam_ids[0])

warmup = exam.get_signal_warmup()
exercise = exam.get_signal_exercise()
cooldown = exam.get_signal_cooldown()
# %%
signal_diff = np.diff(exercise.signal)
signal_diff_clean = nk.rsp_clean(signal_diff, exercise.freq)
_, signal_peaks = nk.rsp_peaks(signal_diff_clean, exercise.freq)
diff_expiration_onsets = signal_peaks['RSP_Peaks']
diff_inspiration_onsets = signal_peaks['RSP_Troughs']

plt.plot(exercise.time, exercise.signal,
        label='Sygnał impedancji oddechowej')
plt.plot(exercise.inspiration_onsets/exercise.freq, 
        exercise.signal[exercise.inspiration_onsets], 'ro',
        label = 'Początki wdechów')
plt.plot(exercise.expiration_onsets/exercise.freq, 
        exercise.signal[exercise.expiration_onsets], 'go',
        label = 'Początki wydechów')
plt.legend()
plt.ylabel('Impedancja oddechowa')
plt.xlabel('Czas [s]')
plt.title('Wyznaczone początki faz oddechowych')
# %%
