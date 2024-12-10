import sys


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
        (times[2] - times[1]),   # 1st challenge time
        (times[3] - times[2]),   # 2nd challenge time
    ))
    print(" " * 4 + "Total: {:.3f}ms | Computed: {:.3f}ms".format(
        (times[-1] - times[0]),   # Total time
        (times[-1] - times[1])    # Computed time
    ))
    print("------------------------------")