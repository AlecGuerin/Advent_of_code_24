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