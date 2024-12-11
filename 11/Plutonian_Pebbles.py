import os
import sys
import time

from multiprocessing import Pool, Manager

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
    
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:
            for line in file:
                tmp = line.strip().split()
                data.extend([int(x) for x in tmp])
                #data.extend(tmp)
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return data


def apply_rules(data, count):
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

    for i in range(count):
        d = 0
        while d < len(data):
            if data[d] == 0:
                data[d] = 1
            elif len(str(data[d]))%2 == 0:
                tmp = str(data[d])
                data[d] = int(tmp[:len(tmp)//2]) # Left half
                d+=1 # Update d
                data.insert(d, int(tmp[len(tmp)//2:])) # Right half
            else:
                data[d] *= 2024
            d+=1
    res = len(data)
    return res


def rule_rec(data, step, known):
    """
    Perform the rules recurssively and keep track of known results.

    Parameters:
        data (int): Value to check.
        step (int): Current step.
        known (dict): Already known results.

    Return:
        number of elements.
    """

    # Check if result is already known
    if (data, step) in known:
        return known[(data, step)]

    res = 0

    # Reached last step
    if step == 0:
        res = 1
    # Data is 0 so turned to 1
    elif data == 0:
        res = rule_rec(1, step-1, known)
    # Half rule
    elif len(str(data))%2 == 0:
        strData = str(data) # string to easilly separate the integer
        res = rule_rec(int(strData[:len(strData)//2]), step-1, known)
        res += rule_rec(int(strData[len(strData)//2:]), step-1, known)
    # Multiplication rule
    else:
        res = rule_rec(data * 2024, step-1, known)

    known[(data, step)] = res # Update the know results
    return res


def apply_rule_rec(data, count):
    """
    Apply the rules to to given array.

    Parameters:
        data (list): Inuts data as integer array.
        count (int): Number of steps to perform.

    Return:
        int: Number of ellement in final array.
    """
    res = 0
    i = 1
    knownResDict = {}
    for d in data:
        res += rule_rec(d, count, knownResDict)
        print(f"{i}/{len(data)} : {d}")
        i+=1
    return res


def make_all_loops_mp(data, cnt, print_progress=False):
    """
    Perform all path search in different processes using multiprocessing with optional printing.
    """

    gRes = 0
    visitedLen = cnt

    # Shared manager dictionary for progress tracking
    with Manager() as manager:
        progress = manager.dict({"completed": 0})
        lock = manager.Lock()

        # Printing function
        def print_status():
            while progress["completed"] < visitedLen:
                time.sleep(0.5)
                with lock:
                    print(f"\rProgress: {progress['completed']}/{visitedLen} tasks completed.", end="")
            print("\nAll tasks completed.")

        # Start the printing thread if needed
        if print_progress:
            from threading import Thread
            print_thread = Thread(target=print_status)
            print_thread.start()

        # Use multiprocessing pool
        with Pool() as pool:
            results = pool.map(
                loops_mt_wrapper,
                []
            )

        # Wait for printing to finish
        if print_progress:
            print_thread.join()

        gRes = sum(results)

    return gRes


def loops_mt_wrapper(args):
    """
    Wrapper function for multiprocessing to handle arguments unpacking and progress updates.
    """
    map, initPos, potentialPos, progress, lock = args
    result = loops_mt(map, initPos, potentialPos)
    with lock:
        progress["completed"] += 1
    return result


if __name__ == '__main__':
    # Default file paths
    in_file = "11/inputs.data"
    out_file = "11/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

# try:
    times[0] = time.perf_counter()

    # Load inputs
    data = get_inputs(in_file, False)
    times[1] = time.perf_counter()

    # Compute the 1st challenge
    results[0] = apply_rule_rec(data, 25)
    times[2] = time.perf_counter()

    # Compute the 2nd challenge
    results[1] = apply_rule_rec(data, 75)
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