import os
import sys
import time
import re

# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file, print_timing

DEFAULT_W = 101
DEFAULT_H = 103

def get_inputs(path: str, test=False):
    """
    Returns the input data.

    Parameter:
        path (str): Input path.
    Return:
        list: Input data.
    """
    data=[]
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:
            for line in file:
                matches = re.findall(r'(?:p|v)=(-?\d+),(-?\d+)', line)
                if len(matches) > 0:
                    vec = [int(num) for pair in matches for num in pair] # Not beautifull but fast implementation
                    data.append(vec)
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return data


def compute_robot_position(initialVector, steps, height = DEFAULT_H, width = DEFAULT_W):

    nx = (initialVector[0] + steps * initialVector[2]) % width
    ny = (initialVector[1] + steps * initialVector[3]) % height
    endPos = [nx, ny]
    return endPos

def get_robots_pos(data, steps, height = DEFAULT_H, width = DEFAULT_W):

    # for i in range(6):
    #     a = compute_robot_position([2,4,2,-3], i, height, length)
    pos = []
    for d in data:
        pos.append(compute_robot_position(d, steps, height, width))

    # COmpute quadran
    quadranCnt = [0,0,0,0]
    midY = height//2
    midX = width//2
    for p in pos:
        if p[0] <  midX and  p[1] < midY:
            quadranCnt[0] +=1
        elif p[0] <  midX and  p[1] > midY:
            quadranCnt[1] +=1
        elif p[0] >  midX and  p[1] < midY:
            quadranCnt[2] +=1
        elif p[0] >  midX and  p[1] > midY:
            quadranCnt[3] +=1
        else:
            pass

    return quadranCnt[0] * quadranCnt[1] * quadranCnt[2] * quadranCnt[3]

def print_robots(data, steps, height = DEFAULT_H, width = DEFAULT_W):
    pic = [['.'] * height for _ in range(width)]
    for d in data:
        x,y = compute_robot_position(d, steps, height, width)
        pic[x][y] = '#'
    print(f'step: {steps}')
    print('\n'.join([''.join(row) for row in pic]))


def get_minimum_entropy(data, height = DEFAULT_H, width = DEFAULT_W):
    
    bestI = -1
    lowEnt = 10**9

    for i in range(height*width):
        entropy = get_robots_pos(data, i, height, width)
        if entropy < lowEnt:
            lowEnt = entropy
            bestI = i           
    
    return bestI


if __name__ == '__main__':
    # Default file paths
    in_file = "14/inputs.data"
    out_file = "14/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

# try:
    times[0] = time.perf_counter()

    test = False
    # Load inputs
    data = get_inputs(in_file, test)
    times[1] = time.perf_counter()

    # Compute the 1st challenge
    if test:
        results[0] = get_robots_pos(data, 100, 11, 7)
    else:
        results[0] = get_robots_pos(data, 100)
    times[2] = time.perf_counter()

    # Compute the 2nd challenge
    results[1] = get_minimum_entropy(data)
    times[3] = time.perf_counter()
    
    # Debug:
    print_robots(data, results[1])

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