"""
John Raines
Advent of Code 2019
Day 10
"""
import numpy as np
import sys
from collections import Counter
from copy import deepcopy

class Asteroid():
    def __init__(self, coords=None):
        """Create an asteroid. Takes a coordinate-pair tuple."""
        self.coords = coords
        self.detects = None
        self.detected_thetas = {}
        self.detected_lengths = {}
    
    def detect_asteroids(self, asteroid_dict):
        """Identify the location of every other asteroid in polar coordinates.
        
        Takes a dict of loc: asteroid. Thetas are stored in self.detected_thetas, 
        and radius lengths are stored in self.detected_lengths. Number of unique
        thetas is stored in self.detects."""
        
        thetas = set()
        asteroids = {loc: b for loc, b in asteroid_dict.items() if loc != self.coords}

        for loc, asteroid in asteroids.items():
            # Translate all locs so that self.coords functions as origin
            x = loc[0] - self.coords[0]
            y = self.coords[1] - loc[1] # invert y calc b/c of the system used by the map
            
            # Calculate theta depending on the quadrant, with zero-handling
            if (x==0) and (y>0):
                theta = 0
            elif (x>=0) and (y>0):
                theta = np.arctan((x/y))
            elif (x>0) and (y==0):
                theta = 90
            elif (x>0) and (y<0):
                theta1 = np.arctan((y/x))
                theta = abs(theta1) + 90
            elif (x==0) and (y<0):
                theta = 180
            elif (x<0) and (y<0):
                theta1 = np.arctan((x/y))
                theta = abs(theta1) + 180
            elif (x<0) and (y==0):
                theta = 270
            elif (x<0) and (y>0):
                theta1 = np.arctan((y/x))
                theta = abs(theta1) + 270
            else:
                # in case we messed up
                print("Didn't account for:")
                print("x",x, "y",y)
                sys.exit()
            thetas.add(theta)
            self.detected_thetas[loc] = theta
            self.detected_lengths[loc] = np.sqrt(x**2 + y**2)
        self.detects = len(thetas)

class AsteroidField():
    def __init__(self, ast_map):
        """Create field of asteroids: takes a string map like the examples."""
        # Define
        self.ast_map = ast_map
        self.asteroids = {}
        self.station = None
        self.order_for_destruction = None
        
        # Do
        self.chart_asteroids()
        
    def chart_asteroids(self):
        """Chart the asteroid locations.
        
        Fills self.asteroids with key = location of asteroid and 
        value = new Asteroid() obj with that location as arg
        """
        rows_map = self.ast_map.split('\n')
        for i, row in enumerate(rows_map):
            for j, loc in enumerate(row):
                if rows_map[j][i] == '#':
                    self.asteroids[(i,j)] = Asteroid((i,j))
                    
    def set_detection_counts(self):
        """For each asteroid, detect as many asteroids as possible.
        
        Calls the `detect_asteroids()` method on each asteroid. Provide
        self.asteroids as the dict of asteroids to detect.
        """
        loc_detect = {}
        for loc, asteroid in self.asteroids.items():
            asteroid.detect_asteroids(self.asteroids)
            loc_detect[loc] = asteroid.detects
        
        # Find the asteroid which detects the most number of asteroids. Set as station.
        highest_detected = max(loc_detect.values())
        self.station = self._return_key(loc_detect, highest_detected)
    
    def detection_field(self):
        """Create a detection field like the one shown in examples, for debugging."""
        rows_map = self.ast_map.split('\n')
        detection_field = ""
        for i, row in enumerate(rows_map):
            for j, loc in enumerate(row):
                if (i,j) in self.asteroids:
                    detection_field += " " + str(self.asteroids[(i,j)].detects) + " "
                else:
                    detection_field += "."
            detection_field += "\n"
        return detection_field
                    
    def laserize(self):
        """Create a list of asteroid locations in the order they'll be destroyed.
        
        Cycle through the unique thetas, append the location of the nearest 
        instance of an asteroid with that theta to the destruction list. Pop 
        that location from a deepcopy list of asteroids. Continue until all
        asteroids have been laserized.
        """
        station = self.asteroids[self.station]
        remaining_thetas = deepcopy(station.detected_thetas)
        slotted_for_destruction = []
        
        while remaining_thetas.keys():
            theta_counts = Counter(list(remaining_thetas.values()))
            thetas = sorted(list(set(remaining_thetas.values())))
            
            for theta in thetas:
    
                if theta_counts[theta] == 1:
                    thisloc = self._return_key(remaining_thetas, theta)
                    slotted_for_destruction.append(thisloc)
                    remaining_thetas.pop(thisloc)
                    
                elif theta_counts[theta] > 1:
                    first_one = self._sort_collinear_by_distance(station, remaining_thetas, theta)
                    slotted_for_destruction.append(first_one)
                    remaining_thetas.pop(first_one)
                    
        self.order_for_destruction = slotted_for_destruction
        
    def _sort_collinear_by_distance(self, station, pop_dict, atheta):
        roids_dist = {}
        for loc, theta in pop_dict.items():
            if theta == atheta:
                roids_dist[loc] = station.detected_lengths[loc]

        sorted_roids = {k: v for k, v in sorted(roids_dist.items(), key=lambda item: item[1])}
        sorted_keys = list(sorted_roids.keys())
        return sorted_keys[0]
        
    def _return_key(self, adict, avalue):
        for key, value in adict.items():
            if value == avalue:
                return key

if __name__ == '__main__':

    with open('day10in.txt', 'rt') as day10in:
        asteroid_belt = day10in.read()
    
    Belt = AsteroidField(asteroid_belt)
    Belt.set_detection_counts()
    print("Best station location is", Belt.station, "with", Belt.asteroids[Belt.station].detects, "asteroids detected.")
    Belt.laserize()
    print("200th to be destroyed:", Belt.order_for_destruction[199])