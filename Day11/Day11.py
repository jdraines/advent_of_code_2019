"""
John Raines
Advent of Code 2019
Day 11
"""
from copy import copy
import numpy as np
import matplotlib.pyplot as plt

with open('advent_path.txt') as advent:
    advent_path = advent.read()
import sys
sys.path.append(advent_path)
from Day09.Day9 import IntcodeComputer


# We need a RegistrationID

class EHPR():
    """Emergency Hull Painting Robot"""
    def __init__(self, prog):
        self.prog = copy(prog)
        self.loc = (0,0)
        self.facing = 0
        self.Computer = None
        self.hullspace = {}
        self.color = 0
    
    def go(self):
        self.Computer = IntcodeComputer(self.prog, input_num=1, output_mode=1, output_switch=self.computer_switcher)
        while self.Computer.output:
            self.paint()
            self.turn()
            self.move()
            self.look()
            self.run_the_comp()
    
    def paint(self):
        self.hullspace[self.loc] = self.Computer.output[0]
    
    def turn(self):
        # Track and update orientation in degrees 0 to 360
        k = (self.Computer.output[1] - 0.5) * 2
        self.facing += k*90
        if self.facing >= 360 :
            self.facing -= 360
        elif self.facing <= -360:
            self.facing += 360
        
    def move(self):
        # Update x and y by trig functions
        x = self.loc[0] + int(round(np.cos(np.radians(self.facing)),0))
        y = self.loc[1] + int(round(np.sin(np.radians(self.facing)),0))
        self.loc = (x,y)

    def look(self):
        self.color = self.hullspace.get(self.loc, 0)

    def computer_switcher(self, output):
        # The robot's output_switch function to provide to the IntcodeComputer
        if len(output) == 2:
            return True
        else:
            return False
    
    def run_the_comp(self):
        # Run the Computer without resetting the memory
        self.Computer.input_id = self.color
        self.Computer.run_program()
        
    def view_the_result(self):
        ys = []
        xs = []
        colors = []
        for key, value in self.hullspace.items():
            ys.append(key[0])
            xs.append(key[1])
            colors.append(value)
        
        # Shift all locations to be non-negative
        ya = np.array(ys)
        xa = np.array(xs)
        
        ya = ya - np.min(ya)
        # Handle the Top > Bottom ascending orientation of imshow()
        ya = [y+ (-2*(y - int(round(np.mean(ya),0)))) for y in ya ] 
        
        xa = xa - np.min(xa)
        xa = np.array([int(round(x,0)) for x in xa])
        grid = np.zeros((np.max(ya)+1, np.max(xa)+1))
        for i, x in enumerate(ys):
            grid[ya[i], xa[i]] = colors[i]
            
        plt.imshow(grid)
        

if __name__ == '__main__':
    
    with open('day11in.txt', 'rt') as day11in:
        program = [int(x.strip()) for x in day11in.read().split(',')]
        
    robot = EHPR(program)
    robot.go()
    print(len(robot.hullspace.keys()))
    robot.view_the_result()