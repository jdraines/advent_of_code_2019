"""
Advent of Code 2019
Author: John Raines
Day 12
Pt.2
"""
import numpy as np
from time import time
from copy import deepcopy
import math
from functools import reduce

class Moon():
    def __init__(self, name, loc, velocity):
        self.name = name
        self.loc = loc
        self.velocity = velocity
        self.PE = None
        self.KE = None
        
class JupiterKineticModel():
    def __init__(self, moons):
        self.time = 0
        self.nmoons = len(moons)
        self.moons = {i : moon for i, moon in enumerate(moons)}
        self.moonarray = self._create_moonarray().astype('int')
        self.initial = deepcopy(self.moonarray)
        self.dim_cycles = {}
        self.cycles = []
    
    def _create_moonarray(self):
        a = np.empty((self.nmoons, 6))
        for i, moon in self.moons.items():
            for j, val in enumerate(moon.loc):
                a[i,j] = val
            for k, val in enumerate(moon.velocity):
                a[i, k+3] = val
        return a
                
    def simulate(self):
        # Simulate 3 times, by dimension
        for j in range(3):
            self.time = 0
            no_repetitions = True
            while no_repetitions:
                # slice the jth dimension of locations for easy ranking
                dim = self.moonarray[:,j]
                
                # perform velocity update for jth dimension, moonwise
                for i in range(self.nmoons):
                    moondim = self.moonarray[i,j]
                    self.moonarray[i, j+3] = self.moonarray[i, j+3] + np.sum(dim > moondim) - np.sum(dim < moondim)   
                
                # perform location update for the jth dimension
                self.moonarray[:,j] = dim + self.moonarray[:,j+3]

                if np.array_equal(self.moonarray[:,[j, j+3]], self.initial[:,[j, j+3]]):
                    self.dim_cycles[j] = self.time + 1
                    self.cycles.append(self.time + 1)
                    no_repetitions = False
            
                self.time +=1
                
                if self.time % 100000 == 0:
                    print("Elapsed steps:", self.time, " Still working on dim", j)
        
        a = np.array(self.cycles).astype('int64')
        return np.lcm.reduce(a)
        
        
if __name__ == '__main__':    
    
    start_vel = (0,0,0)

    # input
    io_loc = (6, -2, -7)
    eu_loc = (-6, -7, -4)
    ga_loc = (-9, 11, 0)
    ca_loc = (-3, -4, 6)
    
    
    Io = Moon('Io', io_loc, start_vel)
    Europa = Moon('Europa', eu_loc, start_vel)
    Ganymede = Moon('Ganymede', ga_loc, start_vel)
    Callisto = Moon('Callisto', ca_loc, start_vel)
    
    MoonSim = JupiterKineticModel([Io, Europa, Ganymede, Callisto])
    answer = MoonSim.simulate()
    print(answer)
            