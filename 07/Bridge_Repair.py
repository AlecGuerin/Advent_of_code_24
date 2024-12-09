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
    Returns the input string.

    Parameter:
        path (str): Input path.
    Return:
        str: Input string.
    """
    operations=[]
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:
            for line in file:
                line = line.strip().replace(":", "").split()
                operations.append([int(x) for x in line])
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return operations


def operate_am(data, i, initial_value, string):
        """
        Recusive methode to find operators
        """
        res = 0
        r1 = [0, ""]
        r2 = [0, ""]


        t1 = initial_value + data[i]
        t2 = initial_value * data[i]
        next_i = i +1

        #if i == len(data) -1 and (t1 == data[0] or t2 == data[0]):
        if next_i == len(data):
            if t1 == data[0]:
                string += f"+{data[i]}"
                res = data[0]
            elif t2 == data[0]:
                string += f"*{data[i]}"
                res = data[0]

        #if next_i < len(data) and (t1 < data[0] or t2 < data[0]):
        if next_i < len(data):
            r1 = operate_am(data, next_i, t1, f"{string}+{data[i]}")
            r2 = operate_am(data, next_i, t2, f"{string}*{data[i]}")

        #if(r1[0] == data[0] or r2[0] == data[0]):
        if r1[0] == data[0]:
            res = data[0]
            string = r1[1]
        elif r2[0] == data[0]:
            res = data[0]
            string = r2[1]

        return res, string


def find_am_operators(data):
    """
    Get the accumulation of midle value of correct updates.

    Parameters:
        rules (list): List of rules.
        updates (list): Proposed updates.
    
    Return
        int: Result
    """
    res = 0
    p_res = 0
    cnt = 1
    # Go througth all operations
    for operation in data:
        tmp = operate_am(operation, 2, operation[1], f"{operation[0]} = {operation[1]}")
        res += tmp[0]
        if p_res!= res:
            #print(tmp[1])
            cnt += 1
        p_res = res

    print(f"res:{res} with {cnt} valid lines")
    return res


def operate_amc(data, expected_value):

    if len(data) == 1:
        return expected_value == data[0]
    
    t1 =  data[0] + data[1] # add
    t2 = data[0] * data[1] # Mul
    tc = data[0] * 10**(len(str(data[1]))) + data[1] # concatecante

    if operate_amc([t1]+data[2:], expected_value):
        return True
    if operate_amc([t2]+data[2:], expected_value):
        return True
    if operate_amc([tc]+data[2:], expected_value):
        return True
    return False

      


def find_amc_operators(data):
    """
    Get the accumulation of midle value of correct updates.

    Parameters:
        rules (list): List of rules.
        updates (list): Proposed updates.
    
    Return
        int: Result
    """
    res = 0
    p_res = 0
    cnt = 1
    # Go througth all operations
    for operation in data:
        res += operation[0] * operate_amc(operation[1:], operation[0])
        if p_res!= res:
            cnt += 1
        p_res = res

    print(f"res:{res} with {cnt} valid lines")
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
    in_file = "07/inputs.data"
    out_file = "07/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

try:
    times[0] = time.perf_counter()

    # Load inputs
    data = get_inputs(in_file, False)
    times[1] = time.perf_counter()

    # Compute the 1st challenge
    results[0] = find_am_operators(data)
    times[2] = time.perf_counter()

    # Compute the 2nd challenge
    results[1] = find_amc_operators(data)
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