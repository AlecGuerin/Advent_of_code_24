import sys
import requests
from bs4 import BeautifulSoup

CRITICAL =0
ERROR = 1
WARNIING = 2
VERBOSE =3
DEBUG = 4

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


def save_webpage_text(url, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("\n")
        # Send an HTTP GET request to the given URL
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the text displayed in the browser
        page_text = soup.get_text()

        # Write the text content to a file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(page_text.strip())
        
        print(f"Web page text content saved to '{filename}' successfully.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def make_files(start: int):

    for i in range(start, 26):
        stringNum = padded = f"{i:02}"
        save_webpage_text(f"https://adventofcode.com/2024/day/{i}", f"{stringNum}/problem.txt")
        save_webpage_text(f"https://adventofcode.com/2024/day/{i}/input", f"{stringNum}/inputs.data")

def log(level, txt):
    if level == CRITICAL:
        print('\033[31m' + 'CRITICAL\t: '+txt + '\033[0m')
    elif level == ERROR:
        print('\033[31m' + 'ERROR\t: '+txt + '\033[0m')
    elif level == WARNIING:
        print('WARNING\t: '+txt)
    elif level == VERBOSE:
        print('MESAGE: '+txt)
    elif level == DEBUG:
        print('DEBUGs\t: '+txt)