'''
Author: joe 
Date: 2024-01-18 14:31:37
LastEditTime: 2024-01-21 12:53:58
LastEditors: joe skchan222@gmail.com
Description: 
FilePath: /race-simulator/simulation.py
'''
import heapq, os
import numpy as np
import pandas as pd
from pprint import pprint
from collections import Counter
from scipy.stats import beta

class simulator(object):
    def __init__(self, filename, n_simulations=1000, STD_LEN=500, a=3, b=3, noise=True, noice_ratio=0.00001, highest=True):
        self.filename = filename
        self.n_simulations = n_simulations
        self.STD_LEN = STD_LEN
        self.a = a
        self.b = b
        self.cdfs = []
        self.noise = noise
        self.noise_ratio = noice_ratio
        self.highest = highest

    def getRecords(self):
        start_pt = -self.STD_LEN
        stop_pt = self.STD_LEN
        total_len = 2 * self.STD_LEN + 1
        x = 0.1 * np.linspace(start_pt, stop_pt, total_len)
        if not os.path.exists(self.filename):
            raise Exception("file not found: %s" % self.filename)
        df = pd.read_csv(self.filename)
        for _, row in df.iterrows():
            if row['total'] > 0:
                self.cdfs.append(beta.cdf(x, row['win'], row['total']-row['win']))
            else:
                self.cdfs.append(beta.cdf(x, self.a, self.b))
    
    def RN_generator(self, cdf):
        if len(self.cdfs) == 0:
            raise Exception('CDF list cannot be empty')
        rns = np.random.rand(self.n_simulations)
        if self.noise:
            return [ self.noise_ratio + sum([rn > prob for prob in cdf]) for rn in rns ]
        else:
            return [ self.noise_ratio + sum([rn > prob for prob in cdf]) for rn in rns ]
    
    def getPosition(self, race, position):
        if self.highest:
            return heapq.nlargest(position+1, range(len(race)), key=race.__getitem__)[position]
        else:
            return heapq.nsmallest(position+1, range(len(race)), key=race.__getitem__)[position]

    def run_simulation(self, simulation=1000):
        if len(self.cdfs) == 0:
            self.getRecords()
        if simulation != self.n_simulations:
            self.n_simulations = simulation
        sim_races = np.array([ self.RN_generator(cdf) for cdf in self.cdfs ])
        sim_races_T = np.transpose(sim_races)
        first = [ self.getPosition(sim_horse, 0) for sim_horse in sim_races_T ]
        second = [ self.getPosition(sim_horse, 1) for sim_horse in sim_races_T ]
        third = [ self.getPosition(sim_horse, 2) for sim_horse in sim_races_T ]
        return self.getSummary(first, second, third)

    @staticmethod
    def getSummary(first, second, third):
        win = Counter(first)
        sec = Counter(second)
        thi = Counter(third)
        show = sec.update(win)
        place = thi.update(sec)
        exacta = Counter(zip(win, sec))
        trifecta = Counter(zip(win,sec,thi))
        return {"win": win, "place": place, "exacta": exacta, "trifecta": trifecta}        
    
    def getWinProb(self, summary):
        winProb = [0.0] * len(self.cdfs)
        horse_idx = 0
        for index, item in summary['win'].most_common():
            winProb[index] = item/self.n_simulations
            horse_idx += 1
        return winProb
