"""
John Raines
Advent of Code
Day 2
"""
from sys import exit
from copy import copy

class IntcodeComputer():
    def __init__(self, prog):
        self.memory_zero = prog
        self.instruction = {
              1: self.add,
              2: self.multiply
              }
        self.memory_last = self.run_program(self.memory_zero)
        if self.memory_last is not None :
            self.output = self.memory_last[0] 
        else:
            self.output = None
            
    def run_program(self, mem):
        n = 0
        while n < len(mem):
            if mem[n] in self.instruction:
                mem[mem[n+3]] = self.instruction[mem[n]](mem[mem[n+1]], mem[mem[n+2]])
                self.memory_last = mem
                n += 4
            elif mem[n]==99:
                return mem
            else:
                print("Error: Cannot accept", mem[n], "as an instruction.")
                return None
        return mem
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
        
    @classmethod
    def set_state(cls, prog, noun, verb):
        prog_copy = copy(prog)
        prog_copy[1] = noun
        prog_copy[2] = verb
        return cls(prog_copy)


with open("day2-1_input.txt", "rt") as puzzin:
    raw_program = [int(x.strip()) for x in puzzin.read().split(',')]

'''First Star'''    
borg_now = IntcodeComputer.set_state(raw_program, 12, 2)
# print("borg_now.output:", borg_now.output)


""" Second Star """

for noun in range(100):
    for verb in range(100):
        hal = IntcodeComputer.set_state(raw_program, noun, verb) 
        if hal.output == 19690720 :
            print("output:", hal.output)
            print("noun:", noun, "verb:", verb)
            print("Answer:", ((100*noun)+verb))
            break