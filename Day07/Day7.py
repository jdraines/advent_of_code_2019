"""
John Raines
Advent of Code
Day 7
"""
from copy import copy
from itertools import permutations
with open('advent_path.txt') as advent:
    advent_path = advent.read()
import sys
sys.path.append(advent_path)
from Day5.Day5 import IntcodeComputer

class AmplifierIntcodeComputer(IntcodeComputer):
    
    def __init__(self, prog, phase, signal=0):
        self.input_switch = {0 : phase,
                             1 : signal}
        self.input_pointer = 0
        self.amplifier_output = None
        self.halt_flag = False
        self.call_next = False
        
        self.memory_zero = copy(prog)
        self.memory_last = copy(self.memory_zero)
        self.p = 0 # instruction pointer
        self.instruction = {
              1: (3, self.one), # add 1 & 2, then store to 3
              2: (3, self.two), # multiply 1 & 2 then store to 3
              3: (1, self.three), # input to 1
              4: (1, self.four), # output 1
              5: (2, self.five), # jump-if-true, if 1 non-zero p = 2
              6: (2, self.six), # jump-if-false, if 1 is 0, p = 2
              7: (3, self.seven), # less-than, if 1 < 2, 3 = int(1), else: 3 = 0
              8: (3, self.eight), # equals, if 1 == 2, 3 = int(1), else: 3 = 0
              99: (0, self.halt) # halt
              }
        self.p_mode_control = {
            0 : self.position_mode,
            1 : self.immediate_mode  # immediate mode
            }
        
        # Sets a default 'output' attribute to the first index of memory. Other
        # outputs can be specified by overloading self.four, as in this case.
        if self.memory_last is not None :
            self.output = self.memory_last[0] 
        else:
            self.output = None
        
    def run_program(self):
        mem = copy(self.memory_last)
        while (self.amplifier_output is None) and (self.halt_flag != True):
            opcode = self.get_opcode(str(mem[self.p]))
            parameter_modes = self.get_param_modes(str(mem[self.p]), opcode)
            values = self.get_values(mem, self.p, opcode, parameter_modes)
            self.instruction[opcode][1](mem, opcode, *values)
        if self.halt_flag == True:
            return True
        elif self.amplifier_output is not None:
            self.call_next = True
        
        
    def three(self, mem, opcode, b):
        '''input to 1'''
        mem[b] = int(self.input_switch[self.input_pointer])
        self.store(mem)
        self.update_p(opcode)
        if self.input_pointer == 0:
            self.input_pointer = 1
    
    def four(self, mem, opcode, b):
        '''output to self.amplifier_output'''
        self.amplifier_output = mem[b]
        self.store(mem)
        self.update_p(opcode)
    
    def halt(self, _a, _b):
        # print("halting...")
        self.halt_flag = True
        
class Amplifier:
    def __init__(self, prog, phase):
        self.prog_frozen = str(prog)
        self.prog_in_mem = literal_eval(self.prog_frozen)
        self.Computer = AmplifierIntcodeComputer(self.prog_in_mem, phase)
        
    def run_prog(self, signal_in):
        # initialize settings--program is not updated
        self.Computer.amplifier_output = None
        self.Computer.input_switch[1] = signal_in
        self.Computer.call_next = False
        self.call_next = False
        
        # run program        
        halted = self.Computer.run_program()
        if halted:
            return True

        # collect necessary outputs
        self.signal_out = self.Computer.amplifier_output
        self.prog_in_mem = literal_eval(self.prog_frozen)
        self.call_next = self.Computer.call_next
    
        
class AmpSeries:
    def __init__(self, prog, phase_sequence):
        self.phase_sequence = phase_sequence
        self.Amp0 = Amplifier(prog, phase_sequence[0])
        self.Amp1 = Amplifier(prog, phase_sequence[1])
        self.Amp2 = Amplifier(prog, phase_sequence[2])
        self.Amp3 = Amplifier(prog, phase_sequence[3])
        self.Amp4 = Amplifier(prog, phase_sequence[4])
        self.maximization_testing = {}
        self.dangerous_overloading = {}
            
    def maximize_amplification(self):
        phase_permutations = list(permutations(range(5)))
        for seq in phase_permutations:
            sequence = "".join([str(x) for x in seq])
            self.maximization_testing[sequence] = self.amplify_signal(seq)
        return max(self.maximization_testing.values())
                
    def amplify_signal(self, phase_sequence, start):
        Amps = [self.Amp0, self.Amp1, self.Amp2, self.Amp3, self.Amp4]
    
        signal_in = start
        
        for i, Amp in enumerate(Amps) :
            halted = Amp.run_prog(signal_in)
            if halted:
                return signal_in, True
    
            signal_in = Amp.signal_out
            if Amp.call_next:
                continue
            elif Amp.Comp.halt_flag:
                break

        halt_indicator = any([x.Computer.halt_flag for x in Amps])
        return Amp.signal_out, halt_indicator
    
    def jury_rig(self):
        a_signal, indicator = self.amplify_signal(self.phase_sequence, 0)
        while not indicator:
            a_signal, indicator = self.amplify_signal(self.phase_sequence, a_signal)
        return a_signal
            

class DangerousSystemOverloader():
    
    def __init__(self, prog, phase_range, auto_push=True):
        self.phase_range = phase_range
        self.prog = prog
        self.dangerous_overloading = {}
        if auto_push:
            self.push_into_the_red()
        
    def push_into_the_red(self):
        phase_permutations = list(permutations(self.phase_range))
        for seq in phase_permutations:
            sequence = "".join([str(x) for x in seq])
            _OverloadedAmps = AmpSeries(copy(self.prog), sequence)
            self.dangerous_overloading[sequence] = _OverloadedAmps.jury_rig()
        max_thrust = max(self.dangerous_overloading.values())
        print("Max thrust achieved:", max_thrust)


if __name__ == '__main__':        
        
    with open('day7in.txt', 'rt') as day7in:
        program = [int(x.strip()) for x in day7in.read().split(',')]
    
    examp = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    
    
    DangerousSystemOverloader(program, range(5,10))