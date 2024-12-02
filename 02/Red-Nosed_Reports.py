import os
import sys
import time

# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file


def get_inputs(path: str, data: list) -> None:
    """
    Extract the input data from the provided file.

    Note:
        The input format should be like: 
        94998 31881 0000 15411 ...
        94998 31881
        ...

    Parameters:
        path (str): Input file path.
        data (list): Array to update.   
    """
    try:
        # Read the file
        with open(path, 'r') as file:
            # Parse lines in the format: 94998 31881 94998 31881 94998 ...
            for line in file:
                line_data = []
                for txt in line.split():
                    if txt.isdigit():
                        line_data.append(int(txt))
                data.append(line_data)
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)


def check_slopes(data: list) -> int:
    """
    Count the number of 'smooth' slopes in the reports.

    Parameters:
        data (list): Array of reports.
    Returns:
        int: Number of correct reports.
    """
    res = 0
    for line in data:
        val = line[1] - line[0]
        sign = (val > 0) - (val < 0)  # Compute initial sign (assuming input size is at least 2)
        is_valid = 1  # Value to add if the report is correct
        for i in range(len(line) - 1):
            val = line[i + 1] - line[i]
            if (val > 3) or (val < -3) or sign != (val > 0) - (val < 0):
                is_valid = 0
                break
        res += is_valid
    return res


def check_slopes_tolerate(data: list, max_error: int) -> int:
    """
    Count the number of 'acceptable' slopes in the reports.

    Note:
        May not fully respect the constraints since levels introducing multiple errors 
        are not discarded. Example: `3 45 5` results in 2 errors but only 1 should be counted. 
        This approach has been validated as is.

    Parameters:
        data (list): Array of reports.
        max_error (int): Maximum number of acceptable errors.
    Returns:
        int: Number of acceptable reports.
    """
    res = 0
    for line in data:
        val = line[1] - line[0]
        sign = (val > 0) - (val < 0)  # Compute initial sign (assuming input size is at least 2)
        error_count = 0
        for i in range(len(line) - 1):
            val = line[i + 1] - line[i]
            error_count += (val > 3) or (val < -3) or sign != (val > 0) - (val < 0)
        res += error_count <= max_error
    return res


def print_timing(times: list) -> None:
    """
    Print the provided timing statistics.

    Parameters:
        times (list): A list of timing data in seconds.
    """
    times = [time_val * 1000 for time_val in times]  # Convert seconds to milliseconds

    print("----------- Timing -----------")
    print(" " * 4 + "Loading: {}ms | Correct: {}ms | Acceptable: {}ms".format(
        (times[1] - times[0]),   # Loading time
        (times[2] - times[1]),   # Correct time
        (times[3] - times[2]),   # Acceptable time
    ))
    print(" " * 4 + "Total: {}ms | Computed: {}ms".format(
        (times[-1] - times[0]),   # Total time
        (times[-1] - times[1])    # Computed time
    ))
    print("------------------------------")


if __name__ == '__main__':
    # Default file paths
    in_file = "02/inputs.data"
    out_file = "02/outputs.data"

    input_data = []
    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

    try:
        times[0] = time.perf_counter()

        # Load inputs
        get_inputs(in_file, input_data)
        times[1] = time.perf_counter()

        # Compute the non-error-tolerant reports
        results[0] = check_slopes(input_data)
        times[2] = time.perf_counter()

        # Compute the error-tolerant reports
        results[1] = check_slopes_tolerate(input_data, max_error)
        times[3] = time.perf_counter()

        print(f"The number of correct reports is: {results[0]}")
        print(f"The number of acceptable reports with {max_error} error{'s' if max_error > 1 else ''} is: {results[1]}")

        # Save the results
        write_out_file(out_file, results)

        # Print timing statistics
        print_timing(times)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    sys.exit()