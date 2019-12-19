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
    def __init__(self, prog):
        self.prog = copy(prog)
        self.loc = (0,0)
        self.facing = 0
        self.Computer = None
        self.hullspace = {}
        self.colors = {0:'.', 1:'#'}
    
    def go(self):
        self.Computer = IntcodeComputer(self.prog, input_num=1, output_mode=1, output_switch=self.computer_switcher)
        while self.Computer.output:
            self.paint()
            self.turn()
            self.move()
            color = self.look()
            self.run_the_comp(color)
    
    def paint(self):
        self.hullspace[self.loc] = self.Computer.output[0]
    
    def turn(self):
        # print("output", self.Computer.output)
        k = (self.Computer.output[1] - 0.5) * 2
        self.facing += k*90
        if self.facing >= 360 :
            self.facing -= 360
        elif self.facing <= -360:
            self.facing += 360
        
    def move(self):
        x = self.loc[0] + int(round(np.cos(np.radians(self.facing)),0))
        y = self.loc[1] + int(round(np.sin(np.radians(self.facing)),0))
        self.loc = (x,y)

    def look(self):
        return self.hullspace.get(self.loc, 0)

    def computer_switcher(self, output):
        # print("switch output", output)
        if len(output) == 2:
            return True
        else:
            return False
    
    def run_the_comp(self, color):
        self.Computer.input_id = color
        self.Computer.run_program()
        
    def view_the_result(self):
        xs = []
        ys = []
        colors = []
        for key, value in self.hullspace.items():
            xs.append(key[0])
            ys.append(key[1])
            colors.append(value)
            
        xa = np.array(xs)
        ya = np.array(ys)
        
        xa = xa - np.min(xa)
        # Handle the Top > Bottom ascending orientation of imshow()
        xa = [x+ (-2*(x - int(round(np.mean(xa),0)))) for x in xa ] 
        
        ya = ya - np.min(ya)
        ya = np.array([int(round(x,0)) for x in ya])
        grid = np.zeros((np.max(xa)+1, np.max(ya)+1))
        for i, x in enumerate(xs):
            try:
                grid[xa[i], ya[i]] = colors[i]
            except:
                print(key)
                raise
        plt.imshow(grid)
        
    
with open('day11in.txt', 'rt') as day11in:
    program = [int(x.strip()) for x in day11in.read().split(',')]
    
robot = EHPR(program)
robot.go()
print(len(robot.hullspace.keys()))
robot.view_the_result()