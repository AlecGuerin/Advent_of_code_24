import sys
import time
import numpy as np


def get_inputs(path: str):
    """
    Extract the input data from the provided file.

    Note:
        The input format should be like: 
        94998   31881
        0000    15411
        ...

    Parameters:
        path (str): Input file path.

    Returns:
        (np.ndarray, np.ndarray): Tuple containing:
            - Left array (np.ndarray)
            - Right array (np.ndarray)
    """
    array_left = []
    array_right = []
    
    try:
        # Read the file
        with open(path, 'r') as file:
            # Parse line format: 94998   31881
            for line in file:
                is_right = True
                for txt in line.split():
                    if txt.isdigit():
                        val = int(txt)
                        if is_right:
                            array_left.append(val)
                            is_right = False
                        else:
                            array_right.append(val)
                            break
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)
    
    return np.array(array_left), np.array(array_right)


def get_diff_acc(s_ar_l: np.ndarray, s_ar_r: np.ndarray) -> int:
    """
    Compute the accumulation of the absolute difference element-wise of the provided arrays.

    Parameters:
        s_ar_l (np.ndarray): Left array.
        s_ar_r (np.ndarray): Right array.

    Returns:
        int: Sum of the absolute differences element-wise of the provided arrays.
    """
    if s_ar_l.size != s_ar_r.size:
        raise ValueError("Arrays must have the same size.")
    
    res = 0
    for i in range(s_ar_l.size):
        res += abs(s_ar_l[i] - s_ar_r[i])

    return res


def get_weighted_correspondence(sorted_left: np.ndarray, sorted_right: np.ndarray) -> int:
    """
    Compute the accumulation of the weighted correspondence between two sorted arrays.

    Parameters:
        sorted_left (np.ndarray): Sorted left array.
        sorted_right (np.ndarray): Sorted right array.

    Returns:
        int: Weighted correspondence result.
    """
    filtered_left = []
    res = 0
    last_ind = 0
    curent_val = 0

    # Go through all left array elements
    for i in range(sorted_left.size):
        same_cnt = 0
        # Check if the value has already been counted using the ordered property of left array
        if curent_val == sorted_left[i]:
            continue
        else:
            curent_val = sorted_left[i] # Update the value to check
            while last_ind < sorted_right.size and sorted_right[last_ind] <= sorted_left[i]:
                same_cnt += sorted_left[i] == sorted_right[last_ind]
                last_ind += 1  # Update the next index to check on the right

            res += sorted_left[i] * same_cnt  # Compute the result

        # Check if all right array elements have been processed
        if last_ind >= sorted_right.size:
            break
    
    return res


def write_out_file(file: str, output):
    """
    Write the output file with the provided output.

    Parameters:
        file (str): File path.
        output (list): List of values to write.
    """
    try:
        with open(file, "w") as f:
            for data in output:
                f.write(str(data) + "\n")
    except Exception as e:
        print(f"Error writing to file '{file}': {e}")
        sys.exit(1)


def print_timing(times):
    times = [time_val * 1000 for time_val in times]

    print("----------- Timing -----------")
    print(" "*4 + "Loading: {}ms | Sorting: {}ms | Difference: {}ms | Weight: {}ms".format(
        (times[1] - times[0]),   # Loading time
        (times[2] - times[1]),   # Sorting time
        (times[3] - times[2]),   # Difference time
        (times[4] - times[3])    # Weight time
    ))
    print(" "*4 + "Total: {}ms | Computed: {}ms".format(
        (times[4] - times[0]),   # Total time
        (times[4] - times[1])    # Computed time
    ))
    print("------------------------------")


if __name__ == '__main__':

    # Get default paths
    in_file = "inputs.data"
    out_file = "outputs.data"

    res = []
    times = [0, 0, 0, 0, 0]

    try:
        times[0] = time.perf_counter()
        # Get the inputs as left and right numpy arrays
        ar_l, ar_r = get_inputs(in_file)

        times[1] = time.perf_counter()
        # Sort the arrays
        sorted_left = np.sort(ar_l)
        sorted_right = np.sort(ar_r)

        times[2] = time.perf_counter()
        # Get the accumulated distances element-wise of the arrays
        res.append(get_diff_acc(sorted_left, sorted_right))

        times[3] = time.perf_counter()
        # Get the accumulation of the weighted correspondence
        res.append(get_weighted_correspondence(sorted_left, sorted_right))
        times[4] = time.perf_counter()

        print(f"The accumulated distances element-wise of the arrays is: {res[0]}")
        print(f"The accumulated weighted correspondence of the arrays is: {res[1]}")

        # Save the results
        write_out_file(out_file, res)

        print_timing(times)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    sys.exit()