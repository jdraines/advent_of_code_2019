# -*- coding: utf-8 -*-
"""
John Raines
Advent of Code
Day 3
"""
from copy import copy
from functools import reduce

class Wire():
    def __init__(self, path):
        self.locs = self.trace_path(path)
    
    def trace_path(self, path):
        x=0
        y=0
        locs = []
        for step in path :
            x, y, locs = self.mark(x, y, locs, step)
        return locs
    
    def mark(self, x, y, locs, step):
        if step[0] == 'R':
            for i in range(int(step[1:])):
                x += 1
                locs.append((x,y))
        elif step[0] == 'L':
            for i in range(int(step[1:])):
                x -= 1
                locs.append((x,y))
        elif step[0] == 'U':
            for i in range(int(step[1:])):
                y += 1
                locs.append((x,y))
        elif step[0] == 'D':
            for i in range(int(step[1:])):
                y -= 1
                locs.append((x,y))
        return x, y, locs

class Grid():
    def __init__(self, wires):
        self.wires = wires # list
        self.intersections = self.find_intersections()
        self.closest_intxn = self.find_closest()
        self.least_steps_intxn = self.least_steps_to_intxn()
    
    def find_intersections(self):
        intersections = []
        for one, _ in enumerate(self.wires) :
            xwires = copy(self.wires)
            wire = xwires.pop(one)
            if len(xwires) > 0:
                xlocs = set(reduce((lambda p,q:p+q),[bwire.locs for bwire in xwires]))
                for loc in wire.locs :
                    if loc in xlocs:
                        intersections.append(loc)
        return intersections
    
    def find_closest(self):
        measurements = {}
        for intersection in self.intersections:
            measurements[intersection] = abs(intersection[0]) + abs(intersection[1])
        self.shortest_dist = min(measurements.values())
        for loc, dist in measurements.items():
            if dist == self.shortest_dist:
                return loc
    
    def least_steps_to_intxn(self):
        step_measures = {}
        for intersection in self.intersections:
            r = 0
            for wire in self.wires:
                for i, loc in enumerate(wire.locs):
                    if intersection == loc :
                        r += i + 1
            step_measures[intersection] = r
        self.fewest_steps = min(step_measures.values())
        for loc, steps in step_measures.items():
            if steps == self.fewest_steps:
                return loc
                        

with open('day3-1.txt') as puzzin:
    wire_paths = puzzin.read()
    
wires = [Wire(wire.split(',')) for wire in wire_paths.split('\n')]
        
mah_grid = Grid(wires)

print(mah_grid.shortest_dist)
print(mah_grid.fewest_steps)