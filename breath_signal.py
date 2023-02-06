import neurokit2 as nk
import numpy as np

# klasa BreathSignal zawierajaca wszystkie metody i atrybuty dotyczace analizy 
# sygnalu oddechowego pochodzacego z pneumonitora impedancyjnego
class BreathSignal():
    def __init__(self, signal, fs=250):
        # ustalenie czestotliwosci probkowania sygnalu
        self.freq = fs
        # sygnal oddechowy poddany filtracji filtrem dolnoprzepustowym IIR Butterwortha 
        # piatego rzedu o czestotliwosci odciecia 2Hz
        self.signal = nk.rsp_clean(signal, self.freq)
        self.signal_raw = np.array(signal)
        # wektor czasu
        self.time = np.arange(start=0, stop=len(self.signal)/self.freq, step=1/self.freq)
        # wyznaczenie ekstremow sygnalu
        self.get_peaks()
        # wyznaczenie czestotliwosci chwilowej
        self.get_fs_inst()
        # wyznaczenie objetosci oddechowej
        self.get_tv()
        # wyznaczenie dlugosci faz oddechowych
        self.get_dur()

    # funkcja sluzaca do znalezienia minimow oraz maksimow sygnalu oddechowego,
    # ktore charakterysuja poczatek i koniec danej fazy oddechowej
    def get_peaks(self):
        _, signal_peaks = nk.rsp_peaks(self.signal, self.freq)
        # probki z poczatkiem fazy wydechu
        self.expiration_onsets = signal_peaks['RSP_Peaks']
        # probki z poczatkiem fazy wdechu
        self.inspiration_onsets = signal_peaks['RSP_Troughs']

    # funkcja sluzaca obliczeniu czestotliwosci chwilowej sygnalu (RR - Respiratory Rate)
    def get_fs_inst(self):
        # wyznaczenie roznic czasowych miedzy kolejnymi poczatkami wdechow
        t_diff = [j/self.freq-i/self.freq for i, j in zip(self.inspiration_onsets[:-1], self.inspiration_onsets[1:])]
        # wyznaczenie częstości oddechowej
        self.fs_inst = [60/t for t in t_diff]

    def get_tv(self):        
        if self.expiration_onsets[0] > self.inspiration_onsets[0]:
            self.insp_depth = [max(self.signal_raw[this_exp:next_insp]) - min(self.signal_raw[prev_exp:this_insp]) 
                            for this_exp, next_insp, prev_exp, this_insp in zip(self.expiration_onsets[1:], self.inspiration_onsets[2:], self.expiration_onsets, self.inspiration_onsets[1:])]
            self.exp_depth = [-max(self.signal_raw[prev_insp:this_exp]) + min(self.signal_raw[this_insp:next_exp]) 
                            for prev_insp, this_exp, this_insp, next_exp in zip(self.inspiration_onsets, self.expiration_onsets, self.inspiration_onsets[1:], self.expiration_onsets[1:])]

        else:
            self.insp_depth = [max(self.signal[this_exp:next_insp]) - min(self.signal[prev_exp:this_insp]) 
                            for this_exp, next_insp, prev_exp, this_insp in zip(self.expiration_onsets[0:], self.inspiration_onsets[1:], self.expiration_onsets, self.inspiration_onsets[1:])]
            self.exp_depth = [-max(self.signal[prev_insp:this_exp]) + min(self.signal[this_insp:next_exp]) 
                            for prev_insp, this_exp, this_insp, next_exp in zip(self.inspiration_onsets, self.expiration_onsets[1:], self.inspiration_onsets[1:], self.expiration_onsets[2:])]

    def get_dur(self):
        if self.expiration_onsets[0] > self.inspiration_onsets[0]:
            self.dur_insp = [insp/self.freq-exp/self.freq for insp, exp in zip(self.inspiration_onsets[1:], self.expiration_onsets)]
            self.dur_exp = [exp/self.freq-insp/self.freq for insp, exp in zip(self.inspiration_onsets, self.expiration_onsets)]
        else:
            self.dur_insp = [insp/self.freq-exp/self.freq for insp, exp in zip(self.inspiration_onsets[1:], self.expiration_onsets)]
            self.dur_exp = [exp/self.freq-insp/self.freq for insp, exp in zip(self.inspiration_onsets, self.expiration_onsets)]

    def trend(slef):
        print('trend not implemented')

    def complexity_note(self):
        print("complexity not implemented")

    def mov_average(self, window = 125):
        limit = len(self.signal) - int(len(self.signal)/window) - window
        moving_averages = [sum(self.signal[i:i+window])/window for i in range(limit)]

        return moving_averages