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
    res =""
    try:
        # Read the file
        with open(path, 'r') as file:
            for line in file:
               res+=line
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)
    return res


def compute_mull(str_of_interest: str, mull_regex = r"mul\(([0-9]{1,3}),([0-9]{1,3})\)"):
    """
    Compute the mulltiplications in the provided string.

    Parameters:
        str_of_interest (str): String to analyse.
        mull_regex (str): Regex string to find mulltiplication. Default checks for 3 digits inputs.
    
    Return
        int: Accumulation of all valid mulltiplications.
    """
    data = re.findall(mull_regex, str_of_interest) # Get the mulltiplications (list of "mull(x,y)")
    integers = [[int(x), int(y)] for x, y in data] # Extract the integer values from previous list
    res =0
    # Perform the mulltiplication and accumulate results.
    for mull in integers:
        res += mull[0]*mull[1]
    return res


def comput_mull_cond(str_of_interest):
    """
    Compute the mulltiplications between enabled intersections.

    Parameter:
        str_of_interest (str): String to check.
    
    Return:
        int: Result of the accumulated valid mulltiplications.
    """
    enable_str = ""
    do_ind =[match.start() for match in re.finditer("do", str_of_interest)] # Get 'do' indexes:

    enable_str += str_of_interest[0:do_ind[0]] # Get the begining of the string before the first do.
    i = 0 # Interation index
    last_do = -1 # Last do to check end of string if needed (Not tested)
    
    # Check all 'do' indexes
    while i < len(do_ind):
        ind_enable = -1
        
        # Check for do() to enable 
        if str_of_interest[do_ind[i]+2:do_ind[i]+4] == "()":
            ind_enable = do_ind[i] # Save the begining index
            last_do = ind_enable
            i+=1
            # Check for next don't()
            while(i < len(do_ind)):
                if str_of_interest[do_ind[i]+2:do_ind[i]+7] == "n't()":
                    enable_str += str_of_interest[ind_enable: do_ind[i]] # Update string of interest
                    i+=1
                    break
                i+=1                
        else:
            i+=1

    # Add the end of string if last tag was a 'do'
    if last_do == do_ind[len(do_ind)-1]:
        enable_str += str_of_interest[last_do:]

    return compute_mull(enable_str) # Compute the mulltiplications


def print_timing(times: list) -> None:
    """
    Print the provided timing statistics.

    Parameters:
        times (list): A list of timing data in seconds.
    """
    times = [time_val * 1000 for time_val in times]  # Convert seconds to milliseconds

    print("----------- Timing -----------")
    print(" " * 4 + "Loading: {:.3f}ms | Total: {:.3f}ms | Valid: {:.3f}ms".format(
        (times[1] - times[0]),   # Loading time
        (times[2] - times[1]),   # Total time
        (times[3] - times[2]),   # Valid time
    ))
    print(" " * 4 + "Total: {:.3f}ms | Computed: {:.3f}ms".format(
        (times[-1] - times[0]),   # Total time
        (times[-1] - times[1])    # Computed time
    ))
    print("------------------------------")


if __name__ == '__main__':
    # Default file paths
    in_file = "03/inputs.data"
    out_file = "03/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

    try:
        times[0] = time.perf_counter()

        # Load inputs
        input_data = get_inputs(in_file)
        times[1] = time.perf_counter()

        # Compute the mulltiplications
        results[0] = compute_mull(input_data)
        times[2] = time.perf_counter()

        # Compute the acceptable mulltiplications
        results[1] = comput_mull_cond(input_data)
        times[3] = time.perf_counter()

        print(f"Accumulation of all mulltiplications: {results[0]}")
        print(f"Accumulation of all valid mulltiplications: {results[1]}")

        # Save the results
        write_out_file(out_file, results)

        # Print timing statistics
        print_timing(times)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    sys.exit()