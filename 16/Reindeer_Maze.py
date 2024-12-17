import os
import sys
import time
import re

# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file, print_timing

sys.setrecursionlimit(10**6)

MAX_VALUE = 10**24
DIR = [[0,-1], [0, 1], [1, 0], [-1, 0]] # <, >,v,^


def get_inputs(path: str, test=False):
    """
    Returns the input data.

    Parameter:
        path (str): Input path.
    Return:
        list: Input data.
    """
    data=[]
    initPos = []
    destination = []
    l = 0
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:
            for line in file:
                
                data.append(list(line.strip()))

                # Find original position
                matches = [match.start() for match in re.finditer("S", line)]
                if len(matches)>0:
                    initPos = [l, matches[0]]
                # Find destination position
                matches = [match.start() for match in re.finditer("E", line)]
                if len(matches)>0:
                    destination = [l, matches[0]]
                l += 1
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return data, initPos, destination


def combined(data, pos, dir, cost, path, validPath, best_res = MAX_VALUE, wasDeadEnd = [False], deadEnd = set()):
    val = get_possible_next(data, pos, dir, cost, path)
    if len(val) == 0:
        wasDeadEnd[0] = True
    else:
        wasDeadEnd[0] = False
    for v in val:
        if (v[0], v[1], v[2]) in deadEnd or cost > best_res:
            continue
        np = path.copy()
        np.append((v[0], v[1], v[2]))
        #draw_map(data, np, cost)
        if data[v[0]][v[1]] == 'E':
            validPath.append([np, cost])            
            if cost < best_res:
                best_res = cost
                #draw_map(data, np, cost)
        else:
            res = combined(data, [v[0], v[1]], v[2], v[3], np, validPath, best_res, wasDeadEnd, deadEnd)
            if wasDeadEnd[0]:
                deadEnd.add((v[0], v[1], v[2]))

            if res < best_res:
                best_res = res
    return best_res


def cost_penaly(cd, nd):
    p0 = 1
    p1 = 1000
    p2 = -1 # 2000
    # Default
    if cd == nd:
        return p0
    # Current dir is left
    elif cd == 0 :
        # Opposite ?
        if nd == 1: 
            return p2 # Turn twice
        else:
            return p1 # Turn once
    elif cd == 1:
        # Opposite ?
        if nd == 0: 
            return p2 # Turn twice
        else:
            return p1 # Turn once
    elif cd == 2:
        # Opposite ?
        if nd == 3: 
            return p2 # Turn twice
        else:
            return p1 # Turn once
    else:
        # Opposite ?
        if nd == 2: 
            return p2 # Turn twice
        else:
            return p1 # Turn once


def get_possible_next(data, pos, dir, cost, path):
    res=[]
    for i in range(4):
        nd = (dir+i)%4
        np = [pos[0] + DIR[nd][0], pos[1] + DIR[nd][1]] # Next position        
        if data[np[0]][np[1]]  != '#' and not_in_path(np, path):
            p = cost_penaly(dir,nd)
            if p > 0:
                res.append([np[0], np[1], nd, cost + p])
            # if p == 1:
            #     res.append([np[0], np[1], nd, cost + p])
            # elif p == 1000:
            #     if (np[0], np[1], nd) not in path:
            #         res.append([pos[0], pos[1], nd, cost + p])
    return res


def not_in_path(pos, path):
    for coor in path:
        if [coor[0], coor[1]] == pos:
            return False
    return True


def draw_map(data, path, score=None):

    def is_in_path(l,c, path):
        for d in path:
            p = (d[0], d[1])
            if p == (l,c):
                return d[2]
        return -1


    print('_'*50)
    print(f'Score: {score} | size: {len(path)}')
    for l in range(len(data)):
        line = ""
        for c in range(len(data[0])):
            v = is_in_path(l,c, path)
            if v >= 0: 
                n = '\033[31m' + '<>v^'[v] + '\033[0m'
            else:
                n = data[l][c]
            line+=n
        print(line)
    

def get_best_res(validPath):
    best = MAX_VALUE
    bl = -1
    bi = -1

    for i in range(len(validPath)):
        if validPath[i][1] < best:
            best = validPath[i][1]
            bi = i

    print(f'Recomputed score: {check_path(validPath[bi][0])}')
    known=set()
    for d in validPath[bi][0]:
        known.add((d[0], d[1]))
    #draw_map(data, validPath[i][0], best)
    return len(known)-1


def check_path(path):
    turns = 0
    score = 0
    for i in range(len(path)-1):
        if path[i][2] != path[i+1][2]:
            turns += 1

    #draw_map(data, path)
    score = len(path) + turns * 1000 - 1
    return score




if __name__ == '__main__':
    # Default file paths
    in_file = "16/inputs.data"
    out_file = "16/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

# try:
    times[0] = time.perf_counter()

    # Load inputs
    data, initPos, destination = get_inputs(in_file, False)
    times[1] = time.perf_counter()

    # Compute the 1st challenge
    path = []
    validPath=[]
    initPos[1] = initPos[1]-1
    results[0] = combined(data, initPos, 1, -1, path, validPath)
    times[2] = time.perf_counter()

    # Compute the 2nd challenge
    results[1] = get_best_res(validPath)
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