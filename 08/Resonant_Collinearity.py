import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, Manager

# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file

def get_inputs(path: str, test=False):
    """
    Returns the input.

    Parameter:
        path (str): Input path.
    Return:
        str: Input string.
    """
    data=[]
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:            
            for line in file:
                data.append(list(line.strip()))
                                   
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return data


def get_map(data: list) -> list:
    """
    Generate a map of the data composed of elements [ID, position, length]
    Parameter:
        data (list): input integer data.
    Return:
        list: Generated map.
    """
    map = []
    for x in range (len(data)):
        for y in range(len(data[0])):
            if data[x][y].isalnum():
                map.append([data[x][y], x,y])

    return map

def get_antinode(map, height, width):
    antinodes =[]
    cnt =0
    for element in map:
        for otherElement in map:
            if element == otherElement:
                continue
            if(element[0] == otherElement[0]):                
                nx = element[1]
                ny = element[2]

                if otherElement[1] > element[1]:
                    nx = element[1] - abs(element[1] - otherElement[1])
                elif otherElement[1] < element[1]:
                    nx = element[1] + abs(element[1] - otherElement[1])

                if otherElement[2] > element[2]:
                    ny = element[2] - abs(element[2] - otherElement[2])
                elif otherElement[2] < element[2]:
                    ny = element[2] + abs(element[2] - otherElement[2])

                antinode = ['#', nx, ny]

                if antinode not in antinodes and (-1 < antinode[1] < height) and (-1 < antinode[2] < width):
                    cnt +=1
                    antinodes.append(antinode)                    
    return cnt


def get_antinode_rh(map, height, width):
    antinodes =[]
    cnt =0
    for element in map:
        for otherElement in map:
            if element == otherElement:
                continue
            if(element[0] == otherElement[0]):                
                nx = element[1]
                ny = element[2]

                dx = abs(element[1] - otherElement[1])
                dy = abs(element[2] - otherElement[2])

                if otherElement[1] < element[1]:
                    dx = -dx
                if otherElement[2] < element[2]:
                    dy = -dy
               
                trace = True
                while trace:
                    nx += dx
                    ny += dy
                    antinode = ['#', nx, ny]         

                    trace = (-1 < nx < height) and (-1 < ny < width)

                    if antinode not in antinodes and trace:
                        cnt +=1
                        antinodes.append(antinode)
    return cnt




def print_timing(times: list) -> None:
    """
    Print the provided timing statistics.

    Parameters:
        times (list): A list of timing data in seconds.
    """
    times = [time_val * 1000 for time_val in times]  # Convert seconds to milliseconds

    print("----------- Timing -----------")
    print(" " * 4 + "Loading: {:.3f}ms | First challenge: {:.3f}ms | Second challenge: {:.3f}ms".format(
        (times[1] - times[0]),   # Loading time
        (times[2] - times[1]),   # Valid time
        (times[3] - times[2]),   # Corrected time
    ))
    print(" " * 4 + "Total: {:.3f}ms | Computed: {:.3f}ms".format(
        (times[-1] - times[0]),   # Total time
        (times[-1] - times[1])    # Computed time
    ))
    print("------------------------------")


if __name__ == '__main__':
    # Default file paths
    in_file = "08/inputs.data"
    out_file = "08/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

try:

        times[0] = time.perf_counter()

        # Load inputs
        data = get_inputs(in_file, False)
        times[1] = time.perf_counter()

        map = get_map(data)

        # Compute the 1st challenge
        results[0] = get_antinode(map, len(data), len(data[0]))
        times[2] = time.perf_counter()

        # Compute the 2nd challenge
        results[1] = get_antinode_rh(map, len(data), len(data[0]))
        times[3] = time.perf_counter()

        print(f"First challenge : {results[0]}")
        print(f"Second challenge: {results[1]}")

        # Save the results
        write_out_file(out_file, results)

        # Print timing statistics
        print_timing(times)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

sys.exit()