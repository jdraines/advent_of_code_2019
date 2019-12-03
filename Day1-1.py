"""
John Raines
Advent of Christmas
Day 1, Star 1
"""

class Module:
    def __init__(self, mass):
        self.fuel = self.calculate_total_fuel(mass)
    
    def calculate_total_fuel(self, mass):
        total_fuel = 0
        this_mass = mass
        add_fuel = self.calculate_fuel(this_mass)
        while add_fuel > 0 :
            total_fuel += add_fuel
            this_mass = add_fuel
            add_fuel = self.calculate_fuel(this_mass)
        return total_fuel
    
    def calculate_fuel(self, mass):
        return int(((mass / 3) // 1 ) - 2)
    
class Spacecraft:
    def __init__(self):
        self.modules = []
        self.total_fuel = 0
    
    def add_module(self, module):
        self.modules.append(module)
    
    def calculate_total_fuel(self):
        self.total_fuel = 0
        for module in self.modules:
            self.total_fuel += module.fuel
        print("Total fuel required:", self.total_fuel)
        return self.total_fuel
        

with open("Day1-1_puzzle_in.txt", "rt") as puzzin:
    puzzle_in = puzzin.read()
    
module_masses = [int(x.strip()) for x in puzzle_in.split('\n')]

my_ship = Spacecraft()

for mass in module_masses :
    my_ship.add_module(Module(mass))
    
total_fuel = my_ship.calculate_total_fuel()