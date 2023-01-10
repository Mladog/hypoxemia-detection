# %%
# IMPORT REQUIRED LIBRARIES
from examination import Examination
from breath_signal import BreathSignal

import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import neurokit2 as nk

# Get Examination
exam_ids = ['bidmc_01', 'bidmc_02']

exam = Examination(exam_ids[1])
"""signals = pd.read_csv("C:/Users/mlado/Desktop/Magisterka/hypoxemia-detection/data/bidmc_01_Signals.csv", delimiter = ',')
signal = nk.rsp_clean(signals[" RESP"], 125)
signal_raw = np.array(signals[" RESP"])"""

resp_impedance = exam.get_breath_signal()
resp_impedance_short = BreathSignal(resp_impedance.signal[:125*60])
# %%

plt.plot(resp_impedance_short.time, resp_impedance_short.signal,
        label='Sygnał impedancji oddechowej')
plt.plot(resp_impedance_short.inspiration_onsets/resp_impedance_short.freq, 
        resp_impedance_short.signal[resp_impedance_short.inspiration_onsets], 'ro',
        label = 'Początki wdechów')
plt.plot(resp_impedance_short.expiration_onsets/resp_impedance_short.freq, 
        resp_impedance_short.signal[resp_impedance_short.expiration_onsets], 'go',
        label = 'Początki wydechów')
plt.legend()
plt.ylabel('Impedancja oddechowa')
plt.xlabel('Czas [s]')
plt.title('Wyznaczone początki faz oddechowych')
# %%
limit = len(resp_impedance_short.signal) - int(resp_impedance_short.signal/25) - 25
moving_averages = [sum(resp_impedance_short.signal[i:i+25])/25 for i in range(int(len(resp_impedance_short.signal)/25))]

# %%
time = resp_impedance.expiration_onsets/resp_impedance.freq
plt.plot(time, resp_impedance.dur_exp)
plt.title('Zmiany długości fazy wydechu')
plt.ylabel('Długość fazy wydechu [s]')
plt.xlabel('Czas [s]')
# %%
time = resp_impedance.inspiration_onsets[:-1]/resp_impedance.freq
plt.plot(time, resp_impedance.fs_inst)
plt.title('Zmiany częstotliwości oddychania')
plt.ylabel('Ilość oddechów na minutę')
plt.xlabel('Czas [s]')
# %%
time_insp = resp_impedance.inspiration_onsets[1:-1]/resp_impedance.freq
time_exp = resp_impedance.expiration_onsets[:-1]/resp_impedance.freq
fig, ax = plt.subplots(2, sharex=True)
fig.suptitle('Objętość oddechowa')
ax[0].plot(time_insp, np.concatenate(resp_impedance.insp_depth, 0))
ax[0].set_title('Objętość podczas wdechu')
ax[0].set_xlabel('czas [s]')
ax[0].set_ylabel('objetość oddechowa')

ax[1].plot(time_exp, np.concatenate(resp_impedance.exp_depth, 0))
ax[1].set_title('Objętość podczas wydechu')
ax[1].set_xlabel('czas [s]')
ax[1].set_ylabel('objetość oddechowa')
#resp_impedance.exp_depth
# %%
v = np.diff(np.concatenate(resp_impedance.exp_depth, 0))
u = np.diff(np.concatenate(resp_impedance.insp_depth, 0))

fig, ax = plt.subplots(2, sharex=True)
fig.suptitle('Zmiany objetosci oddechowej w czasie')
ax[0].plot(time_insp[:-1], u)
ax[0].set_title('zmiany objętości podczas wdechu')
ax[0].set_xlabel('czas [s]')
ax[0].set_ylabel('zmiana objetosci oddechowej')

ax[1].plot(time_exp[:-1], v)
ax[1].set_title('zmiany objętości podczas wydechu')
ax[1].set_xlabel('czas [s]')
ax[1].set_ylabel('zmiana objetosci oddechowej')
# %%
