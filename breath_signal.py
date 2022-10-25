

class BreathSignal():

    def __init__(self, signal, fs= 500):
        self.freq = fs
        self.signal = signal
        
    def fs_inst(self):
        print('fs inst not implemented')

    def tv_insp(self):
        print('tv inst not implemented')

    def tv_exp(self):
        print('tv exp not implemented')

    def dur_insp(self):
        print('dur insp not implemented')

    def dur_exp(self):
        print('dur exp not implemented')

    def trend(slef):
        print('trend not implemented')


def respiratory_depth(rsp, insp_onsets, exp_onsets):
    exp_depth = []
    insp_depth = []
    # ustalenie czy pierwszym zdarzeniem jest wdech czy wydech
    if exp_onsets[0] < insp_onsets[0]:
        #do obliczenia glebokosci potrzebna jest informacja o poprzedzajacym wdechu
        exp_onsets = exp_onsets[1:]
    # wyliczenie glebokosci wdechow
    for i in range(1,len(insp_onsets)-1):
        insp_depth.append(max(rsp[exp_onsets[i]:insp_onsets[i+1]]) - min(rsp[exp_onsets[i-1]:insp_onsets[i]]))
    
    # wyliczenie glebokosci wydechow
    for i in range(1,len(exp_onsets)-1):
        exp_depth.append(-max(rsp[insp_onsets[i-1]:exp_onsets[i]]) + min(rsp[insp_onsets[i]:exp_onsets[i+1]]))
    
    return insp_depth, exp_depth