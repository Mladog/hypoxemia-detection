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
exam = Examination(exam_ids[2])

resp_impedance = exam.get_breath_signal()
# %%
