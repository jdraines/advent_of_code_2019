# -*- coding: utf-8 -*-
"""
John Raines
Advent of Code 2019
Day 8
"""

import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

class SpIF():
    
    def __init__(self, spif_file):
        '''Takes a SpIF tuple'''
        self.data = spif_file # a Space Image Format file                
    
    @classmethod    
    def deserialize(cls, serial, nwide, ntall):
        '''Takes a serialized SpIF file, and returns a formatted SpIF file'''
        spif_unlayered = []
        if len(serial) % nwide == 0:
            nrows = int(len(serial) / nwide)
        else:
            nrows = int(len(serial) // nwide)
            print("Problem: Serialized file was not evenly divisible into rows.")
            print(str(len(serial) % nwide) + " trailing pixel(s) will be dropped.")
        
        for n in range(nrows):
            spif_unlayered.append(serial[n*nwide : (n+1)*nwide])
        spif = []
        if len(spif_unlayered) % ntall == 0:
            nlayers = int(len(spif_unlayered) / ntall)
        else:
            nlayers = int(len(spif_unlayered) // ntall)
            print("Problem: Serialized file was not evenly divisible into layers.")
            print(str(len(spif_unlayered) % ntall) + " trailing row(s) will be dropped.")
        
        
        for n in range(nlayers):
            spif.append(spif_unlayered[n*ntall : (n+1)*ntall])
        
            aspif = np.array(spif)
        
        return cls(aspif)

class SpIFViewer():
    def __init__(self, spif_file):
        self.spif = spif_file
    
    def show_image_flattened(self):
        flat_spif = self._flatten_image()
        plt.imshow(flat_spif)
        plt.show()
    
    def _flatten_image(self):
        flat_spif = np.empty((self.spif.data.shape[1], self.spif.data.shape[2]))
        for x in range(self.spif.data.shape[1]):
            for y in range(self.spif.data.shape[2]):
                for z in range(self.spif.data.shape[0]):
                    if self.spif.data[z,x,y] in { 0, 1 }:
                        flat_spif[x,y] = self.spif.data[z,x,y]
                        break
        return flat_spif
    
    def find_brightest_layer(self):
        layer_zeros = {}
        layer_ones = {}
        layer_twos = {}
        for z in range(self.spif.data.shape[0]):
            layer_zeros[z] = Counter(self.spif.data[z,:,:].flatten())[0]
            layer_ones[z] = Counter(self.spif.data[z,:,:].flatten())[1]
            layer_twos[z] = Counter(self.spif.data[z,:,:].flatten())[2]
                    
        brightest = min(layer_zeros.values())
        
        for loc, value in layer_zeros.items():
            if value == brightest:
                bloc = loc
                break
            
        return layer_ones[bloc] * layer_twos[bloc]
        
if __name__ == '__main__':

    with open('day8in.txt', 'rt') as day8in:
           password =  [int(x) for x in day8in.read()]

    
    example=[int(x) for x in '123456789012']
    spif = SpIF.deserialize(password, 25, 6)
    print(SpIFViewer(spif).show_image_flattened())