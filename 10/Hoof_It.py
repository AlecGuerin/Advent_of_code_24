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
            for line in file:
                tmp = line.strip()                            
                map.append([int(x) for x in tmp])
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return map


def count_single_paths(map):
    """
    Get the accumulation of unique reachable path ends.

    Parameters:
        map (list): 2D integer array representing the map.
    
    Return
        int: Accumulation of unique reachable path ends.
    """
    res = 0

    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == 0:
                res += explore_next_unk(map, [x,y], [])
    return res


def explore_next_unk(map, pos, known):
    """
    Count recursively the unique path ends rechable.

    Parameters:
        map (list): 2D map to explore.
        pos ([int, int]): Current position.

    Return:
        int: Count rechable in the path.
    """
    res = 0
    # Check bound
    if  pos[0] < 0 or pos[0] >= len(map) or pos[1] < 0 or pos[1] >= len(map[0]):
        return 0

    if map[pos[0]][pos[1]] == 9 and pos not in known:
        known.append(pos)
        return 1
    
    ns = map[pos[0]][pos[1]] +1 # Expected next value to reach
    
    np = [pos[0]+1, pos[1]] # Next position to sample
    if  0 <= np[0] < len(map) and  0 <= np[1] < len(map[0]) and map[np[0]][np[1]] == ns:
        res += explore_next_unk(map, np, known)
    
    np = [pos[0]-1, pos[1]]
    if  0 <= np[0] < len(map) and  0 <= np[1] < len(map[0]) and map[np[0]][np[1]] == ns:
        res += explore_next_unk(map, np, known)
    
    np = [pos[0], pos[1]+1]
    if  0 <= np[0] < len(map) and  0 <= np[1] < len(map[0]) and map[np[0]][np[1]] == ns:
        res += explore_next_unk(map, np, known)

    np = [pos[0], pos[1]-1]
    if  0 <= np[0] < len(map) and  0 <= np[1] < len(map[0]) and map[np[0]][np[1]] == ns:
        res += explore_next_unk(map, np, known)
    
    return res


def count_paths(map):
    """
    Get the count of all possible path to ends.

    Parameters:
        map (list): 2D map.
    
    Return
        int: Count of all possible path to reachable ends.
    """
    res = 0

    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == 0:
                res += explore_next(map, [x,y])
    return res


def explore_next(map, pos):
    """
    Count recursivelly all possible path to ends.

    Parameters:
        map (list): 2D map to explore.
        pos ([int, int]): Current position.

    Return:
        int: Count of all possible path to ends.
    """

    res = 0
    # Check bound
    if  pos[0] < 0 or pos[0] >= len(map) or pos[1] < 0 or pos[1] >= len(map[0]):
        return 0

    # Check end
    if map[pos[0]][pos[1]] == 9:
        return 1
    
    ns = map[pos[0]][pos[1]] +1 # Expected next value to reach
    
    np = [pos[0]+1, pos[1]] # Next position to sample
    if  0 <= np[0] < len(map) and  0 <= np[1] < len(map[0]) and map[np[0]][np[1]] == ns:
        res += explore_next(map, np)
    
    np = [pos[0]-1, pos[1]]
    if  0 <= np[0] < len(map) and  0 <= np[1] < len(map[0]) and map[np[0]][np[1]] == ns:
        res += explore_next(map, np)
    
    np = [pos[0], pos[1]+1]
    if  0 <= np[0] < len(map) and  0 <= np[1] < len(map[0]) and map[np[0]][np[1]] == ns:
        res += explore_next(map, np)

    np = [pos[0], pos[1]-1]
    if  0 <= np[0] < len(map) and  0 <= np[1] < len(map[0]) and map[np[0]][np[1]] == ns:
        res += explore_next(map, np)
    
    return res


if __name__ == '__main__':
    # Default file paths
    in_file = "10/inputs.data"
    out_file = "10/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

# try:
    times[0] = time.perf_counter()

    # Load inputs
    map = get_inputs(in_file, False)
    times[1] = time.perf_counter()

    # Compute the 1st challenge
    results[0] = count_single_paths(map)
    times[2] = time.perf_counter()

    # Compute the 2nd challenge
    results[1] = count_paths(map)
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