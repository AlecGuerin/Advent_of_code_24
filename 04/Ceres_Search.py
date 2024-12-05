import os
import sys
import time




# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file


def get_inputs(path: str, data: list) -> None:
    """
    Extract the input data from the provided file.

    Parameters:
        path (str): Input file path.
        data (list): Array to update.   
    """
    try:
        # Read the file
        with open(path, 'r') as file:
            # Parse lines in the format: 94998 31881 94998 31881 94998 ...
            for line in file:                
                data.append(line[:-1])
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)


def search_xmas(data: list)-> int:
    """
    Search for XMAS occurences in the file.
    
    Parameter:
        data (list) : Input data
    
    Return:
        int: Count of XMAS found.
    """
    XMAS="XMAS"
    SAMX="SAMX"
    res = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            # Count xmas and masx
            res += data[i][j:j+4] == XMAS or data[i][j:j+4] == SAMX            
            dxmas_r = 0
            dsamx_r = 0
            dxmas_l = 0
            dsamx_l = 0
            vxmas = 0
            vsamx = 0
            for k in range(4):
                if i+k < len(data):
                    if j+k < len(data[0]):
                        # Check for falling XMAS
                        dxmas_r += data[i+k][j+k] == XMAS[k]
                        dsamx_r += data[i+k][j+k] == SAMX[k]
                        # Check for rising XMAS
                        if i+3-k < len(data):
                            dxmas_l += data[i+3-k][j+k] == XMAS[k]
                            dsamx_l += data[i+3-k][j+k] == SAMX[k]
                    # Check for vertial xmas
                    vxmas += data[i+k][j] == XMAS[k]
                    vsamx += data[i+k][j] == SAMX[k]
                res += int(dxmas_r==4) + int(dsamx_r==4) +\
                    int(dxmas_l==4) + int(dsamx_l==4) +\
                    int(vxmas==4) + int(vsamx==4)
    return res

def search_x_mas(data: list)-> int:
    """
    Search for X-MAS occurences in the file.
    
    Parameter:
        data (list) : Input data
    
    Return:
        int: Count of X-MAS found.
    """
    XMAS="MAS"
    SAMX="SAM"
    res = 0
    for i in range(len(data)):
        for j in range(len(data[0])):  
            dxmas_r = 0
            dsamx_r = 0
            dxmas_l = 0
            dsamx_l = 0
            for k in range(3):
                if i+k < len(data):
                    if j+k < len(data[0]):
                        # Check for falling XMAS
                        dxmas_r += data[i+k][j+k] == XMAS[k]
                        dsamx_r += data[i+k][j+k] == SAMX[k]
                        # Check for rising XMAS
                        if i+2-k < len(data):
                            dxmas_l += data[i+2-k][j+k] == XMAS[k]
                            dsamx_l += data[i+2-k][j+k] == SAMX[k]
                oldres = res
                # Res +=1 if both diagonals are ok 
                res += (dxmas_r==3 or dsamx_r==3) and (dxmas_l==3 or dsamx_l==3)
    return res

def print_timing(times: list) -> None:
    """
    Print the provided timing statistics.

    Parameters:
        times (list): A list of timing data in seconds.
    """
    times = [time_val * 1000 for time_val in times]  # Convert seconds to milliseconds

    print("----------- Timing -----------")
    print(" " * 4 + "Loading: {:.3f}ms | XMAS: {:.3f}ms | X-MAS: {:.3f}ms".format(
        (times[1] - times[0]),   # Loading time
        (times[2] - times[1]),   # XMAS time
        (times[3] - times[2]),   # X-MAX time
    ))
    print(" " * 4 + "Total: {:.3f}ms | Computed: {:.3f}ms".format(
        (times[-1] - times[0]),   # Total time
        (times[-1] - times[1])    # Computed time
    ))
    print("------------------------------")

if __name__ == '__main__':
    # Default file paths
    in_file = "04/inputs.data"
    out_file = "04/outputs.data"

    input_data = []
    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

    try:
        times[0] = time.perf_counter()

        # Load inputs
        get_inputs(in_file, input_data)
        times[1] = time.perf_counter()

        # Compute the XMAS occurences
        results[0] = search_xmas(input_data)
        times[2] = time.perf_counter()

        # Compute the X-MAS occurences
        results[1] = search_x_mas(input_data)
        times[3] = time.perf_counter()

        print(f"XMAS count: {results[0]}")
        print(f"X-MAS count: {results[1]}")

        # Save the results
        write_out_file(out_file, results)

        # Print timing statistics
        print_timing(times)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    sys.exit()