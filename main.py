# %%
# IMPORT REQUIRED LIBRARIES
from examination import Examination


# %%
# Get Examination
exam_id = 1

exam = Examination(exam_id)

airflow = exam.get_breath_signal()

airflow.dur_exp()
# %%
import matplotlib.pyplot as plt
import numpy as np 

def respiratory_onsets(airflow):
    airflow_cumsum = np.cumsum(airflow.signal)
    plt.plot(airflow_cumsum)
    ons = airflow
    return ons

respiratory_onsets(airflow)

# %%
