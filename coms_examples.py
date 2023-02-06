# %%
# IMPORT REQUIRED LIBRARIES
from examination import Examination
from breath_signal import BreathSignal

import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import neurokit2 as nk
from scipy.signal import medfilt
import matplotlib.transforms as mtransforms

# Get Examination
exam_ids = ['HB086', 'HB090', 'HB091']
exam = Examination(exam_ids[1])
# %%

resp_impedance = exam.get_breath_signal()
resp_impedance_short = BreathSignal(resp_impedance.signal[-125*60:])

signal_diff = np.diff(resp_impedance_short.signal_raw)
signal_diff_clean = nk.rsp_clean(signal_diff, resp_impedance_short.freq)
_, signal_peaks = nk.rsp_peaks(signal_diff_clean, resp_impedance_short.freq)
diff_expiration_onsets = signal_peaks['RSP_Peaks']
diff_inspiration_onsets = signal_peaks['RSP_Troughs']


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
y_smooth = medfilt(resp_impedance_short.signal_raw, 121)
yprime = np.diff(y_smooth)
max_val = max(abs(yprime))*0.05
pause = abs(yprime) < max_val
pause = [1 if p == True else 0 for p in pause]
pause = medfilt(pause, 101)

x = [i for i, e in enumerate(yprime) if abs(e) < max_val]

fig, ax = plt.subplots(2, sharex=True)
fig.suptitle('Impedancja i różniczka')
trans = mtransforms.blended_transform_factory(ax[0].transData, ax[0].transAxes)
ax[0].plot(resp_impedance_short.time, resp_impedance_short.signal_raw)
ax[0].set_title('Impedancja')
ax[0].set_ylabel('Wartość impedancji')
#ax[0].plot(resp_impedance_short.time[x], yprime[x], 'ro')
ax[0].fill_between(resp_impedance_short.time[:-1], 0, 1, where= pause,
                facecolor='green', alpha=0.5, transform=trans)

ax[1].plot(resp_impedance_short.time[1:], yprime)
ax[1].set_title('Różniczka')
ax[1].set_xlabel('czas [s]')
ax[1].set_ylabel('Wartość różniczki')
# %%
resp_impedance_no_zeros = resp_impedance_short.signal[x]
resp_impedance_no_zeros = list(set(resp_impedance_short.signal) - set(resp_impedance_no_zeros))

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
ax[0].plot(time_insp[200:-1], u[200:])
ax[0].set_title('zmiany objętości podczas wdechu')
ax[0].set_xlabel('czas [s]')
ax[0].set_ylabel('zmiana objetosci oddechowej')

ax[1].plot(time_exp[200:-1], v[200:])
ax[1].set_title('zmiany objętości podczas wydechu')
ax[1].set_xlabel('czas [s]')
ax[1].set_ylabel('zmiana objetosci oddechowej')
# %%
