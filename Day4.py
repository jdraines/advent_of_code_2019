# -*- coding: utf-8 -*-
"""
John Raines
Advent of Code
Day 4
"""


class PasswordCracker:
    def __init__(self, low, high):
        self.range_of_nums = [ str(x) for x in range(low, high) ]
        self.first_star = self.narrow_the_field(self.range_of_nums, self.check_one)
        self.second_star = self.narrow_the_field(self.first_star, self.check_again)
        
    def narrow_the_field(self, possibles, func):
        still_possibles = []
        for poss in possibles :
            still_poss = func(poss)
            if still_poss is not None:
                still_possibles.append(still_poss)
        return still_possibles

    def check_one(self, numstr):
        doubles = []
        for i in range(6):
            if any([int(numstr[x]) > int(numstr[i]) for x in range(i)]) :
                return None
            if i != 5 :
               doubles.append(int(numstr[i+1]) != int(numstr[i]))
        if all(doubles):
            return None    
        return numstr
    
    def check_again(self, numstr):
        has2=[]
        for i in range(6):
            if numstr.count(numstr[i]) == 2:
                return numstr
    
    def show_answers(self):
        print("First star answer:", len(self.first_star))
        print("Second star answer:", len(self.second_star))


low = 273025
high = 767253

PasswordCracker(low, high).show_answers()
