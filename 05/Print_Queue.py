import os
import sys
import time
import re


# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file

def get_inputs(path: str):
    """
    Returns the input string.

    Parameter:
        path (str): Input path.
    Return:
        str: Input string.
    """
    rules=[]
    updates=[]
    try:
        # Read the file
        with open(path, 'r') as file:
            for line in file:
                # Get the rules
                tmp = line.split("|")
                if len(tmp) == 2: #read rules
                    rules.append([int(tmp[0]), int(tmp[1])])
                    continue
                # Get the upates
                tmp = line.split(",")
                if len(tmp) < 2:
                    continue
                updates.append([int(numeric_string) for numeric_string in tmp])                
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return rules, updates


def get_midle_ok_rules_acc(rules, updates):
    """
    Get the accumulation of midle value of correct updates.

    Parameters:
        rules (list): List of rules.
        updates (list): Proposed updates.
    
    Return
        int: Accumulation of all valid updates (value in the midle of the array).
    """
    res=0    
    for update in updates: # Go throught all updates
        ok=True
        for i in range(len(update)): # Go throught all update elements
            for rule in rules: # Go througth all rules
                if rule[0] in update and rule[1] in update:
                    if update.index(rule[0]) > update.index(rule[1]):
                        ok = False
                        break
            if not ok:
                break
        if ok:
            res += update[len(update)//2] #Accumulate if the update is valid
    return res

def get_midle_updated_acc(rules, updates):
    """
    Get the accumulation of midle value of corrected updates.

    Parameters:
        rules (list): List of rules.
        updates (list): Proposed updates.
    
    Return
        int: Accumulation of all valid updates (value in the midlle of the array).
    """
    res=0    
    for update in updates: # Go throught all updates
        ok=False
        for i in range(len(update)): # Go throught all update elements
            for rule in rules: # Go througth all rules
                if rule[0] in update and rule[1] in update:
                    ir0 = update.index(rule[0]) # get index 1st rul
                    ir1 =update.index(rule[1]) # Get index rule 1
                    if  ir0 > ir1:
                        ok = True
                        # Perform the permutation
                        tmp = update[ir0]
                        update[ir0] = update[ir1]
                        update[ir1] = tmp
        if ok:
            res += update[len(update)//2] # Accumulate if the update has been updated
    return res

def print_timing(times: list) -> None:
    """
    Print the provided timing statistics.

    Parameters:
        times (list): A list of timing data in seconds.
    """
    times = [time_val * 1000 for time_val in times]  # Convert seconds to milliseconds

    print("----------- Timing -----------")
    print(" " * 4 + "Loading: {:.3f}ms | Valid: {:.3f}ms | Corrected: {:.3f}ms".format(
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
    in_file = "05/inputs.data"
    out_file = "05/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

    try:
        times[0] = time.perf_counter()

        # Load inputs
        rules, updates = get_inputs(in_file)
        times[1] = time.perf_counter()

        # Compute the 1st challenge
        results[0] = get_midle_ok_rules_acc(rules, updates)
        times[2] = time.perf_counter()

        # Compute the 2nd challenge
        results[1] = get_midle_updated_acc(rules, updates)
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