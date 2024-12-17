import os
import sys
import time
import re

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
    data=[]
    initPos = []
    commands = ''
    l = 0
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:
            comSec = False
            for line in file:
                #Find the command section
                if line == '\n':
                    comSec = True
                    continue
                
                if comSec:
                    commands += line.strip()
                    continue
                
                data.append(list(line.strip()))

                # Find orriginal position
                matches = [match.start() for match in re.finditer("@", line)]
                if len(matches)>0:
                    initPos = [l, matches[0]]
                l += 1
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return data, initPos, commands


def compute_map(data, initPos, commands):

    pos = initPos # Set initial position
    dir = [[0,-1], [0, 1], [1, 0], [-1, 0]] # <, >,v,^
    draw_map(data, "Initial state:")
    # Compute all the command interations
    for i in range(len(commands)):
        # Find next position
        if commands[i] == "^":
           d = 3
        elif commands[i] == "v":
            d = 2
        elif commands[i] == "<":
            d = 0
        elif commands[i] == ">":
            d = 1

        pos = update_map(data, pos, dir[d])
        # Debug
        # draw_map(data, f"Move {'<>v^'[d]}: ({i})")


def compute_map2(data, initPos, commands):
    pos = initPos # Set initial position
    dir = [[0,-1], [0, 1], [1, 0], [-1, 0]] # <, >,v,^
    draw_map(data, "Initial state:")
    # Compute all the command interations
    for i in range(len(commands)):
        # Find next position
        if commands[i] == "^":
           d = 3
        elif commands[i] == "v":
            d = 2
        elif commands[i] == "<":
            d = 0
        elif commands[i] == ">":
            d = 1

        pos = update_map2(data, pos, dir[d])
        # Debug
        # draw_map(data, f"Move {'<>v^'[d]}: ({i})")


def update_map(data, pos, dir):
    np = [pos[0] + dir[0], pos[1] + dir[1]] # Get next position
    # Check for wall
    if data[np[0]][np[1]] == "#":
        return pos
    elif data[np[0]][np[1]] == ".":
        swap(data, pos, np)
        return [np[0], np[1]]
    elif data[np[0]][np[1]] == "O":

        prevNp = update_map(data, np, dir)
        # Check if can move
        if np == prevNp:
            return pos
        prevNp = [prevNp[0]-dir[0], prevNp[1]-dir[1]]

        # Retro fit the move
        while data[prevNp[0]][prevNp[1]] == '.' or data[prevNp[0]][prevNp[1]] == '@':
            prevNp = update_map(data, [prevNp[0]-dir[0], prevNp[1]-dir[1]], dir)
            if prevNp == np:
                break
            prevNp = [prevNp[0]-dir[0], prevNp[1]-dir[1]]        
        return np
    

def update_map2(data, pos, dir):
    np = [pos[0] + dir[0], pos[1] + dir[1]] # Get next position
    # Check for wall
    if data[np[0]][np[1]] == "#":
        return pos
    elif data[np[0]][np[1]] == ".":
        swap(data, pos, np)
        return [np[0], np[1]]
    elif data[np[0]][np[1]] == "[" or data[np[0]][np[1]] == "]":

        npCLosing = [np[0] + dir[0], np[1] + dir[1]] # Get the closing box
        prevNp = update_map(data, np, dir)
        # Check if can move
        if np == prevNp:
            return pos
        
        prevNp = [prevNp[0]-dir[0], prevNp[1]-dir[1]]
        PrevNpCLosing = [npCLosing[0]-dir[0], npCLosing[1]-dir[1]]

        # Retro fit the move
        while data[prevNp[0]][prevNp[1]] == '.' or data[prevNp[0]][prevNp[1]] == '@':
            prevNp = update_map(data, [prevNp[0]-dir[0], prevNp[1]-dir[1]], dir)
            if prevNp == np:
                break
            prevNp = [prevNp[0]-dir[0], prevNp[1]-dir[1]]
        
        return np


def move_box(pos, dir):
    pass #TODO: code!
    
def swap(data, pos, np):
    tmp = data[pos[0]][pos[1]]
    data[pos[0]][pos[1]] = data[np[0]][np[1]]
    data[np[0]][np[1]] = tmp


def draw_map(data, msg):
    print('_'*50)
    print(msg)
    print('\n'.join([''.join(row) for row in data]))
    

def make_map_2(data, map2):
    convDict = {'#':'##', 'O':'[]', '.':'..', '@':'@.'}
    for d in data:
        line = ''
        for i in range(len(d)):
           line += convDict[d[i]]
        map2.append(line)


def compute_result(data):
    res = 0
    for l in range(len(data)):
        for c in range(len(data[0])):
            if data[l][c] == "O":
                res += 100*l + c
    return res


if __name__ == '__main__':
    # Default file paths
    in_file = "15/inputs.data"
    out_file = "15/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

# try:
    times[0] = time.perf_counter()

    map2 = []
    # Load inputs
    data, initPos, commands = get_inputs(in_file, True)
    make_map_2(data, map2)
    times[1] = time.perf_counter()

    # Compute the 1st challenge
    compute_map(data, initPos, commands)
    results[0] = compute_result(data)
    times[2] = time.perf_counter()


    sys.exit() # DEbug

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