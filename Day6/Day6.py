"""
John Raines
Advent of Code 
Day 6
"""
from copy import copy

class SystemMap:
    def __init__(self, orbit_str, fullmap=True):
        '''Represent a map of orbital systems. Takes a string of list of A)B (B orbits A)'''
        # Definitions
        self.orbits = self._get_orbits(orbit_str) # set
        self.objects = self._get_objects() # set
        self.ObjectRelations = dict()
        self.center = ''
        self.leaves = set()
        
        # Do:
        self._map_inward()
        self._map_outward()
        self._get_leaves()
    
        if fullmap == True:
            self.fullmap()
    
    def fullmap(self):
        '''Trace branches'''
        # Map ancestors by tracing every node to root
        for obj in self.objects:
            if self.ObjectRelations[obj]['parent'] not in [self.center, ''] :
                parent = self.ObjectRelations[obj]['parent']
                abuelo = self.ObjectRelations[parent]['parent']
                focus = self.ObjectRelations[self.ObjectRelations[copy(obj)]['parent']]['parent']
                stopper = 0
                while stopper != 1 :
                    if focus != obj :
                        self.ObjectRelations[obj]['ancestors'].add(copy(focus))
                        if focus == self.center :
                            stopper = 1
                        focus = self.ObjectRelations[focus]['parent']
                    elif focus == self.center :
                        stopper = 1
        
        # Map descendants from leaf to root
        leafs = list(copy(self.leaves))
        for obj in leafs:
            focus = copy(obj)
            parent = self.ObjectRelations[focus]['parent']
            children = self.ObjectRelations[focus]['children']
            descendants = set()
            stopper = 0

            while stopper != 1 :
                if (parent not in [None, '']): 
                    if children != set():
                        descendants.update(copy(children))
                        self.ObjectRelations[parent]['descendants'].update(descendants)
                    self.ObjectRelations[parent]['children'].add(copy(focus))
                    
                if focus == self.center:
                    stopper = 1
                else:
                    focus = copy(parent)
                    parent = self.ObjectRelations[focus]['parent']
                    children = self.ObjectRelations[focus]['children']

        
        # Fix the 'set()' value for various generations
        for obj in self.objects:
            if self.ObjectRelations[obj]['parent']== '':
                self.ObjectRelations[obj]['parent'] = None
            if self.ObjectRelations[obj]['ancestors']== set():
                self.ObjectRelations[obj]['ancestors'] = None
            if self.ObjectRelations[obj]['children']== set():
                self.ObjectRelations[obj]['children'] = None
            if self.ObjectRelations[obj]['descendants']== set():
                self.ObjectRelations[obj]['descendants'] = None
            
    
    def shortest_path(self, A, B, to_screen=False):
        if to_screen:
            print("Shortest path from", A, "to", B, ":")
        
        # Go to the first parent of A which has B as a descendant, and record steps there
        set_to_parent = set()
        steps_to_parent = []
        foundB = False
        parent = self.ObjectRelations[A]['parent']
        while foundB == False:
            if self.ObjectRelations[parent]['descendants'] is not None:
                cousins = self.ObjectRelations[parent]['children'].union(self.ObjectRelations[parent]['descendants'])
            else:
                cousins = self.ObjectRelations[parent]['children']
            if B in cousins:
                steps_to_parent.append(parent)
                steps_to_parent = steps_to_parent[1:]
                foundB = True
            else:
                set_to_parent.add(parent)
                steps_to_parent.append(parent)
                parent = self.ObjectRelations[parent]['parent']
        
        #Find the path to B from the parent
        set_to_B = set()
        steps_to_B = []
        atB = False
        children = self.ObjectRelations[parent]['children']
        
        
        
        # Find the child whose children/descendants include B
        while atB == False :
            for child in children :
                if B in self.ObjectRelations[child]['children']:
                    set_to_B.add(child)
                    steps_to_B.append(child)
                    atB = True
                else:        
                    # for each branch-to-leaf, check to see if B lies along that branch
                    for leaf in list(self.leaves) :
                        if self.ObjectRelations[parent]['descendants'] is not None:
                            child_line = self.ObjectRelations[child]['children'].union(self.ObjectRelations[child]['descendants'])
                        else:
                            child_line = self.ObjectRelations[child]['children']
                        if (leaf in child_line) and (B in child_line):
                            set_to_B.add(child)
                            steps_to_B.append(child)
                            break
                if child in set_to_B :
                    children = self.ObjectRelations[child]['children']
                    break
        
        shortest_path = steps_to_parent + steps_to_B
        return shortest_path
        
    
    def count_orbits(self, object_list):
        dir_desc_count = 0
        ind_desc_count = 0
        dir_anc_count = 0
        ind_anc_count = 0
        
        for obj in object_list :
            if self.ObjectRelations[obj]['parent'] not in [ None, '']:
                dir_anc_count += 1
            if self.ObjectRelations[obj]['ancestors'] is not None:
                ind_anc_count += len(self.ObjectRelations[obj]['ancestors'])    
        print()
        print("Number of orbits")
        print(" Direct:", dir_anc_count)
        print(" Indirect:", ind_anc_count)
        print(" Total:", dir_anc_count + ind_anc_count)
        print()
        
    def _get_orbits(self, input_str):
        '''Get edges'''
        return { x.strip() for x in input_str.split('\n') }

    def _get_objects(self):
        '''Get nodes'''
        step1 = [ x.split(')') for x in self.orbits ]
        uniques = []
        for x in step1:
            uniques.extend(x)
        return set(uniques)

    def _get_child_parent(self, node):
        '''Return: child, parent'''        
        return node.split(')')[1], node.split(')')[0]
    
    def _map_inward(self):
        for orbit in self.orbits:
            child, parent = self._get_child_parent(orbit)
            self.ObjectRelations[child] = {'parent':parent, 
                                           'children':set(), 
                                           'ancestors':set(), 
                                           'descendants':set()}
    
    def _map_outward(self):
        for orbit in self.orbits:
            child, parent = self._get_child_parent(orbit)
            if parent in self.ObjectRelations:
                self.ObjectRelations[parent]['children'].add(child)
            else :
                self.center = parent
                self.ObjectRelations[parent] = {'parent': '', 
                                                'children':set(), 
                                                'ancestors':set(), 
                                                'descendants': set()}
                self.ObjectRelations[parent]['children'].add(child)
    
    def _get_leaves(self):
        for obj in self.objects:
            if self.ObjectRelations[obj]['children'] == set() :
                self.leaves.add(obj)
        
with open('day6in.txt', 'rt') as day6_input:
    local_orbits = day6_input.read()

example="""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""


Map = SystemMap(local_orbits)
Map.count_orbits(Map.objects)
print("Length: ", len( Map.shortest_path('YOU', 'SAN', to_screen=True)))

