# %%
# IMPORT REQUIRED LIBRARIES
from examination import Examination

import matplotlib.pyplot as plt
import numpy as np 

# Get Examination
exam_id = 1

exam = Examination(exam_id)

airflow = exam.get_breath_signal()

#airflow.dur_exp()

plt.plot(airflow.time, airflow.signal)
plt.plot(airflow.inspiration_onsets/airflow.freq, airflow.signal[airflow.inspiration_onsets], 'ro')
plt.plot(airflow.expiration_onsets/airflow.freq, airflow.signal[airflow.expiration_onsets], 'go')
# %%
