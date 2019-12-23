"""
Advent of Code 2019
Author: John Raines
Day 12
Pt.2
"""
import numpy as np
from time import time
import sys


class seq(list):
    def __init__(self, array):
        for i in range(array.shape[0]):
            self.i = array[i]
        self.n = array.shape[0]
    
    def __hash__(self):
        hasher = []
        for i in range(self.n):
            hasher.append(self.i)
        return hash(tuple(hasher))
        

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
        self.ndims = len(moons[0].loc)
        self.moons = {i : moon for i, moon in enumerate(moons)}
        self.moonarray = self._create_moonarray().astype('int')
        self.states = set()
    
    def _create_moonarray(self):
        a = np.empty((self.nmoons, self.ndims*2))
        for i, moon in self.moons.items():
            for j, val in enumerate(moon.loc):
                a[i,j] = val
            for k, val in enumerate(moon.velocity):
                a[i, k+self.ndims] = val
        return a
                
    def simulate(self, iterations):
        velocities=[]
        for t in range(iterations):
            for j in range(self.ndims):
                dim = self.moonarray[:,j]
                for i in range(self.nmoons):
                    moondim = self.moonarray[i,j]
                    self.moonarray[i, j+self.ndims] = np.sum(dim > moondim) - np.sum(dim < moondim)
                    self.moonarray[i,j] = moondim + np.sum(dim > moondim) - np.sum(dim < moondim)
            state = seq(self.moonarray.flatten())
            self.time += 1
            if state in self.states:
                print("State repeated at time:", self.time)

        
if __name__ == '__main__':    
    
    start_vel = (0,)
    
    # example
    io_loc = (-1,)
    eu_loc = (2,)
    ga_loc = (4,)
    ca_loc = (3,)
    
    
    """ # input
    io_loc = (6,)
    eu_loc = (-6,)
    ga_loc = (-9,)
    ca_loc = (-3,)
    """
    
    Io = Moon('Io', io_loc, start_vel)
    Europa = Moon('Europa', eu_loc, start_vel)
    Ganymede = Moon('Ganymede', ga_loc, start_vel)
    Callisto = Moon('Callisto', ca_loc, start_vel)
    
    MoonSim = JupiterKineticModel([Io, Europa, Ganymede, Callisto])
    time0 = time()
    MoonSim.simulate(1000000)
    time1 = round(time() - time0,3)
    print(time1)
    print(MoonSim.moonarray)            
            