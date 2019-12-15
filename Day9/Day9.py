# -*- coding: utf-8 -*-
"""
John Raines
Advent of Code 2019
Day 9
"""
from copy import copy
import sys

class IntcodeComputer():
    """Version 3.0, Now BOOST Certified!"""
    def __init__(self, prog, input_num=None):
        self.memory_zero = copy(prog)
        self.memory_last = copy(self.memory_zero)
        self.p = 0 # instruction pointer
        self.rb = 0 # relative base
        self.instruction = {
              1: (3, self.one), # add 1 & 2, then store to 3
              2: (3, self.two), # multiply 1 & 2 then store to 3
              3: (1, self.three), # input to 1
              4: (1, self.four), # output 1
              5: (2, self.five), # jump-if-true, if 1 non-zero p = 2
              6: (2, self.six), # jump-if-false, if 1 is 0, p = 2
              7: (3, self.seven), # less-than, if 1 < 2, 3 = int(1), else: 3 = 0
              8: (3, self.eight), # equals, if 1 == 2, 3 = int(1), else: 3 = 0
              9: (1, self.nine), # adjust relative base
              99: (0, self.halt) # halt
              }
        self.p_mode_control = {
            0 : self.position_mode,
            1 : self.immediate_mode,
            2 : self.relative_mode
            }
        self.input_id = input_num
        self.run_program()
        if self.memory_last is not None :
            self.output = self.memory_last[0] 
        else:
            self.output = None
    
    def run_program(self):
        mem = copy(self.memory_last)
        #mem.extend([0]*1000)
        halt = None
        while not halt:
            try:
                opcode = self.get_opcode(str(mem[self.p]))
                parameter_modes = self.get_param_modes(str(mem[self.p]), opcode)
                values = self.get_values(mem, self.p, opcode, parameter_modes)
                halt = self.instruction[opcode][1](mem, opcode, *values)
            except IndexError:
                if len(mem) < 10**6:
                    mem.extend([0]*1000)
                    print("(extended memory)")
                else:
                    print("Length size is already 10^6. Raise ceiling?")
                    sys.exit()
        
    def one(self, mem, opcode, b, c, d):
        '''add 1 & 2, then store to 3'''
        mem[d] = mem[b] + mem[c]
        self.store(mem)
        self.update_p(opcode)
        
    def two(self, mem, opcode, b, c, d):
        '''multiply 1 & 2 then store to 3'''
        mem[d] = mem[b] * mem[c]
        self.store(mem)
        self.update_p(opcode)
            
    def three(self, mem, opcode, b):
        '''input to 1'''
        mem[b] = int(self.input_id)
        self.store(mem)
        self.update_p(opcode)

    def four(self, mem, opcode, b):
        '''output 1'''
        print("Out:", mem[b])
        self.store(mem)
        self.update_p(opcode)
        
    def five(self, mem, opcode, b, c):
        '''jump-if-true: if 1 non-zero, p = 2'''
        if mem[b] != 0:
            self.p = mem[c]
        else:
            self.update_p(opcode)
        self.store(mem)
    
    def six(self, mem, opcode, b, c):
        '''jump-if-false, if 1 is 0, p = 2'''
        if mem[b] == 0:
            self.p = mem[c]
        else:
            self.update_p(opcode)
        self.store(mem)
    
    def seven(self, mem, opcode, b, c, d):
        '''less-than, if 1 < 2, 3 = int(1), else: 3 = 0'''
        if mem[b] < mem[c] :
            mem[d] = 1
        else:
            mem[d] = 0
        self.store(mem)
        self.update_p(opcode)
        
    def eight(self, mem, opcode, b, c, d): 
        '''equals, if 1 == 2, 3 = int(1), else: 3 = 0'''
        if mem[b] == mem[c] :
            mem[d] = 1
        else:
            mem[d] = 0
        self.store(mem)
        self.update_p(opcode)
    
    def nine(self, mem, opcode, b):
        '''self.rb += 1'''
        self.rb += mem[b]
        self.store(mem)
        self.update_p(opcode)
    
    def halt(self, _a, _b):
        try:
            sys.exit()
        except:
            return True
            
    def get_opcode(self, instruct_code):
        length = len(instruct_code)
        if length == 1:
            opcode = int(instruct_code[-1])
        else:
            opcode = int(instruct_code[-2:])
        return opcode
    
    def get_param_modes(self, instruct_code, opcode):
        if len(instruct_code) >= 2:
            parameters = instruct_code[::-1][2:] # the parameters, left to right
        else:
            parameters = ''
        
        param_modes = []
        for digit in parameters:
            param_modes.append(int(digit))
        
        exp_prm_cnt = self.instruction[opcode][0]  # expected parameter count
        if len(parameters) < exp_prm_cnt :
            for i in range(exp_prm_cnt - len(parameters)):
                param_modes.append(0)
        
        return param_modes
    
    def get_values(self, mem, n, opcode, parameter_modes):
        values = []
        for i, param_num in enumerate(range((n+1), (n + self.instruction[opcode][0]+1))):
            value = self.p_mode_control[parameter_modes[i]](mem, param_num)
            values.append(value)
        return values

    def position_mode(self, mem, param): return int(mem[param])

    def immediate_mode(self, mem, param): return int(param)
    
    def relative_mode(self, mem, param): return int(mem[param] + self.rb)
    
    def store(self, mem):
        self.memory_last = mem
    
    def update_p(self, opcode):
        self.p += self.instruction[opcode][0] + 1
    
    @classmethod
    def set_state(cls, prog, noun, verb):
        prog_copy = copy(prog)
        prog_copy[1] = noun
        prog_copy[2] = verb
        return cls(prog_copy)

if __name__ == '__main__':
    example=[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    
    with open('day9in.txt', 'rt') as day9in:
        BOOSTin = [int(x.strip()) for x in day9in.read().split(',')]
    
    # BOOST test
    # BOOST = IntcodeComputer(BOOSTin, 1)
    
    # boost with BOOST 
    BOOST = IntcodeComputer(BOOSTin, 2)