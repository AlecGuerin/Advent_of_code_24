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
                line = line.strip()
                ind = 0
                for i in range(len(line)):
                    if i % 2:
                        for j in range(int(line[i])):
                            data.append(-1)                            
                    else:
                        for j in range(int(line[i])):
                            data.append(ind)
                        ind += 1                            
                    
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
    i = 0
    while i < len(data):
        tmp = [data[i], i , 1] # [ID, pos, length]
        while i < len(data)-1 and tmp[0] == data[i+1]:
            tmp[2] += 1
            i +=1
        map.append(tmp)
        i+=1
    return map


def fill_blank(data: list)-> int:
    """
    Fill all the blank with last availlable data.

    Parameter:
        data (list): list of integer of the input.

    return:
        int Checksum compuetd.
    """
    res = 0
    permutedInd=0
    last = len(data) -1
    for i in range(len(data)):
        if(data[i] == -1):
            while data[last] == -1:
                last -=1
            data[i] = data[last]
            data[last] = -1
            last -= 1
            if last < i:
                break
        res += i * data[i]
    return res


def ckc_sum(element: list)->int:
    """
    Compute the check sum with the provided map element.

    Parameter:
        element (list): map elemement ([id, pos, length]).

    return:
        Computed check sum.
    """
    res =0
    for i in range(element[1], element[1]+element[2]):
        res += element[0] * i
    return res


def relocate_block(map: list):
    """
    Fill the first available blank if last data fits.

    Parameter:
        map (list): Input mapped.
    return:
        int Checksum compuetd.
    """
    res = 0
    
    last = len(map) - 1
    first_empty = 0

    while last >= 0:
        update = True
        i = first_empty
        if map[last][0] != -1:
            while i < last:
                if map[i][0] != -1:                   
                    pass
                elif map[last][2] < map[i][2]:
                    newLen = map[i][2] - map[last][2]                    
                    map[i][0] = map[last][0]
                    map[i][2] = map[last][2]
                    map[last][0] = -1
                    # Add new blank
                    map.insert(i+1, [-1, map[i][1]+map[i][2], newLen])
                    last +=1 # Update last with the added element
                    break
                elif map[last][2] == map[i][2]:
                    map[i][0] = map[last][0]
                    map[last][0] = -1                    
                    break
                
                if map[i][0] == -1 and update:
                    first_empty = i
                    update = False
                i += 1

        last -=1
    # Compute the check sum
    for element in map:
        if element[0] == -1:
            continue
        res += ckc_sum(element)
    return res


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
    in_file = "09/inputs.data"
    out_file = "09/outputs.data"

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
    results[0] = fill_blank(data)
    times[2] = time.perf_counter()

    # Compute the 2nd challenge
    results[1] = relocate_block(map)
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