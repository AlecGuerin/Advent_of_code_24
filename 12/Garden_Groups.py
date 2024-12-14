import os
import sys
import time

# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file, print_timing

def get_inputs(path: str, test=False):
    """
    Returns the input data.

    Parameter:
        path (str): Input path.
    Return:
        list: Input data.
    """
    map=[]
    
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:
            x = 0
            for line in file:
                tmp = line.strip()
                map.append(tmp)
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return map


class Group:
    def __init__(self, id:int, char:str):
        self.id = id
        self.char = char
        self.coords = []

        self.area = 0
        self.perimeter = 0
        self.cost = 0
        self.sides = 0
    
    def add_coordonate(self, coord: list):
        self.coords.append(coord)
        self.area+=1

    def update_perimeter(self, len):
        self.perimeter += len
    
    def update_cost(self):
        self.cost = self.area * self.perimeter

    def get_sides_cnt(self):

        if len(self.coords) == 0:
            self.sides = 0
        elif len(self.coords) == 1 or len(self.coords) == 2:
            self.sides = 4
        elif len(self.coords) == 3:
            self.sides = 6
        else:
            self.sides = 1
            i=0
            dir = [(0,1), (1,0), (0,-1), (-1,0)] # right, bottom, left, top
            visited = set()
            # get boundaries:
            boudaries = set()
            for p in self.coords:
                for dx, dy in dir:
                    if [p[0] + dx, p[1]+dy] not in self.coords:
                        boudaries.add((p[0], p[1]))

            # Sort boundary points for traversal
            boudaries = sorted(boudaries, key=lambda p: (p[0], p[1]))

            i = 0            
            np = next(iter(boudaries))
            cnt = 0
            changed = False
            while True:
 
                prevNp = np   
                np = (np[0] + dir[i][0], np[1] + dir[i][1]) # Get next np
                # if not found, turn!
                if (np, i) in visited:
                    break
                if np not in boudaries:
                    self.sides += 1
                    # find new dirrection                    
                    if i == 0: # Going right
                        np = (prevNp[0] + dir[3][0], prevNp[1] + dir[3][1]) # check up                        
                    elif i == 1: # going down
                        np = (prevNp[0] + dir[0][0], prevNp[1] + dir[0][1]) # check right
                    elif i == 2: # going low
                        np = (prevNp[0] + dir[1][0], prevNp[1] + dir[1][1]) # check left
                    elif i == 3: # going left
                        np = (prevNp[0] + dir[2][0], prevNp[1] + dir[2][1]) # check low


                cnt+=1

        return self.sides


    def get_line(boundaries, p, visited):
       # count horrizontal lines:
       for p in boundaries:
           pass

    def print_group(self):
        print(f"{self.area} * {self.perimeter} = {self.cost}\n{self.area} * {self.sides} = {self.area*self.sides}")


def make_groupes(map, groups = None):
    """
    Naive rule application
    
    Note:
        Pretty slow, compuation grows exponentially with count.

    Parameters:
        data (list): Integer list to apply the rules.
        count (int): Number of time to apply the rule.
    
    Return
        int: Number of elements at the end.
    """
    res = 0    
    checked = {}    
    group = None

    if groups == None:
        groups = []
    
    for x in range(len(data)):
        for y in range(len(data[0])):
            # Already checked
            if (x, y) in checked:
                continue
            else:
                group = Group(len(groups), data[x][y])
                rec_area(data, [x,y], checked, group)
                groups.append(group)
    
    for g in groups:
        g.update_cost()
        res += g.cost

    return res


def rec_area(map: list, point:list, knownPoint:dict, group: Group):

    if (point[0] < 0 or point[0] >= len(map)\
        or point[1] < 0 or point[1] >= len(map[0])\
        or map[point[0]][point[1]] != group.char):
        group.update_perimeter(1)
        return
    
    if (point[0], point[1]) in knownPoint:
        return
    
    group.add_coordonate(point)
    knownPoint[(point[0], point[1])] = group
    rec_area(map, [point[0]+1, point[1]], knownPoint, group) # Go right
    rec_area(map, [point[0]-1, point[1]], knownPoint, group) # Go Left
    rec_area(map, [point[0], point[1]+1], knownPoint, group) # Go Low
    rec_area(map, [point[0], point[1]-1], knownPoint, group) # Go up        


def compute_new_cost(groups:list):
    res = 0
    for g in groups:
        res += g.get_sides_cnt() * g.area
        g.print_group()

    return res

if __name__ == '__main__':
    # Default file paths
    in_file = "12/inputs.data"
    out_file = "12/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

# try:
    times[0] = time.perf_counter()

    # Load inputs
    data = get_inputs(in_file, True)
    times[1] = time.perf_counter()

    # Compute the 1st challenge
    groups = []
    results[0] = make_groupes(data, groups)
    times[2] = time.perf_counter()

    # Compute the 2nd challenge
    results[1] = compute_new_cost(groups)
    times[3] = time.perf_counter()

    print(f"First challenge : {results[0]}")
    print(f"Second challenge: {results[1]}")

    # Save the results
    write_out_file(out_file, results)

    # Print timing statistics
    print_timing(times)

# except Exception as e:
#     print(f"An error occurred: {e}")
#     sys.exit(1)

    sys.exit()