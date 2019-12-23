"""
Advent of Code 2019
Author: John Raines
Day 12
Pt.1
"""
from itertools import combinations
from time import time


class Moon():
    def __init__(self, name, loc, velocity):
        self.name = name
        self.loc = loc
        self.velocity = velocity
        self.PE = None
        self.KE = None
    
    def calc_PE(self):
        self.PE = abs(self.loc[0]) + abs(self.loc[1]) + abs(self.loc[2])
    
    def calc_KE(self):
        self.KE = abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])
    
    def calc_TE(self):
        if self.PE is None:
            self.calc_PE()
        if self.KE is None:
            self.calc_KE()
        return self.PE * self.KE
    
class JupiterKineticModel():
    time = 0
    
    def __init__(self, moons):
        self.moons = {moon.name : moon for moon in moons}
        self.pairs = list(combinations(moons, 2))
    
    def simulate(self, iterations):
        for n in range(iterations):
            self._apply_gravity()
            self._apply_velocity()
            self._time_step()
        
    def _apply_gravity(self):
        for pair in self.pairs:
            self._apply_gravity_once(*pair)
        
    def _apply_gravity_once(self, A, B):
        # find smaller's of change:
        A_change = self._return_unit_of_vel_change(B, A)
        B_change = self._return_unit_of_vel_change(A, B)
        A.velocity = self.update_vel(A, A_change)
        B.velocity = self.update_vel(B, B_change)
        """debug
        if A.name == 'Io':
            print('Io change', A_change, 'Io velocity', A.velocity)
        elif B.name == 'Io':
            print('Io change', B_change, 'Io velocity', B.velocity)
        """

    def _return_unit_of_vel_change(self, A, B):
        def one_dim(A, B, i):
            if A.loc[i] != B.loc[i]:
                return int((A.loc[i] - B.loc[i]) / abs(A.loc[i] - B.loc[i]))
            else:
                return 0  
        x = one_dim(A, B, 0)
        y = one_dim(A, B, 1)
        z = one_dim(A, B, 2)
        return (x,y,z)
        
    def update_vel(self, A, delt):
        def one_dim(A, delt, i):
            return A.velocity[i] + delt[i]
        x = one_dim(A, delt, 0)
        y = one_dim(A, delt, 1)
        z = one_dim(A, delt, 2)
        return (x,y,z)
    
    def _apply_velocity(self):
        def one_dim(moon, i):
            return moon.velocity[i] + moon.loc[i]
        
        for moon in self.moons.values():
            x = one_dim(moon, 0)
            y = one_dim(moon, 1)
            z = one_dim(moon, 2)
            moon.loc = (x,y,z)
            """ debug
            if moon.name == 'Io':
                print('Io loc', moon.loc)
            """
            
    def _time_step(self):
        self.time +=1

    def total_energy(self):
        energies = []
        for moon in self.moons.values():
            energies.append(moon.calc_TE())
        return sum(energies)
    
if __name__ == '__main__':    
    
    start_vel = (0,0,0)
    
    io_loc = (6, -2, -7)
    eu_loc = (-6, -7, -4)
    ga_loc = (-9, 11, 0)
    ca_loc = (-3, -4, 6)
    
    Io = Moon('Io', io_loc, start_vel)
    Europa = Moon('Europa', eu_loc, start_vel)
    Ganymede = Moon('Ganymede', ga_loc, start_vel)
    Callisto = Moon('Callisto', ca_loc, start_vel)
    
    MoonSim = JupiterKineticModel([Io, Europa, Ganymede, Callisto])
    time0 = time()
    MoonSim.simulate(100000)
    time1 = round(time() - time0,3)
    print(time1)
    
    print("Io        ", "loc", MoonSim.moons['Io'].loc, "  vel", MoonSim.moons['Io'].velocity)
    print("Europa    ", "loc", MoonSim.moons["Europa"].loc, "  vel", MoonSim.moons["Europa"].velocity)
    print("Ganymede  ", "loc", MoonSim.moons["Ganymede"].loc, "  vel", MoonSim.moons["Ganymede"].velocity)
    print("Callisto  ", "loc", MoonSim.moons["Callisto"].loc, "  vel", MoonSim.moons["Callisto"].velocity)
    print()
    print("Total Energy of System:", MoonSim.total_energy())