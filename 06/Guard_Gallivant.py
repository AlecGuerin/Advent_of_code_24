import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, Manager

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
    map=[]
    intiPos=[]
    try:
        # Read the file
        with open(path, 'r') as file:
            for line in file:
                tmp = line.strip()
                if len(intiPos) < 1:
                    for i in range(len(tmp)):
                        # Left
                        if ("<" == tmp[i]):
                            intiPos = [len(map), i, -1]
                            break
                        # Right
                        if (">" == tmp[i]):
                            intiPos = [len(map),i,  1]
                            break
                        #top
                        if ("^" == tmp[i]):
                            intiPos = [len(map),i,  -2]
                            break
                        # Botom TODO find chat
                        if ("v" == tmp[i]):
                            intiPos = [len(map), i, 2]
                            break
                            
                map.append(tmp)
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return map, intiPos


def count_visited_pos(map, initPos):
    """
    Get the accumulation of midle value of correct updates.

    Parameters:
        rules (list): List of rules.
        updates (list): Proposed updates.
    
    Return
        int: Accumulation of all valid updates (value in the midle of the array).
    """
    res = 0
    count=0
    curPos = initPos
    visited =[]

    next_Dir = [0, 2, -1, 0, 1, -2] # Compute the next direction from the index of current direction
    
    while True:
        nextPos=[]
        # Update visited and update visited count
        if [curPos[0], curPos[1]] not in visited:
            visited.append([curPos[0], curPos[1]])
            res += 1
        # Compute next position
        if -2 < curPos[2] < 2:
            nextPos = [curPos[0], curPos[1]+ curPos[2], curPos[2]]
        else:
            nextPos = [curPos[0] + curPos[2]//2, curPos[1], curPos[2]]

        if nextPos[0] >= len(map[0]) or nextPos[1] >= len(map) or nextPos[0] < 0 or nextPos[1] < 0:
            break

        if(map[nextPos[0]][nextPos[1]] == "#"):
            next_dir = curPos[2]
            nextPos = [curPos[0], curPos[1], next_Dir[curPos[2]]]

        curPos = nextPos
        count +=1
    return res, visited


def make_all_loops(map, initPos, visited):
    """
    Get the accumulation of midle value of corrected updates.

    Parameters:
        rules (list): List of rules.
        updates (list): Proposed updates.
    
    Return
        int: Accumulation of all valid updates (value in the midlle of the array).
    """
    res=0
    count=0
    tries = 0
    next_Dir = [0, 2, -1, 0, 1, -2] # Compute the next direction from the index of current direction
    gRun = True
    
    visited.pop(0)

        # Functions
    def print_data():
        while gRun:
            time.sleep(0.5)
            sys.stdout.write(
                f"\r>>Tries: {tries}/{len(visited)} | Operation: {count}"
            )
            sys.stdout.flush()

    printTh = threading.Thread(target=print_data)
    printTh.start()

    # Parcour visited:
    for potentialPos in visited:
        curPos = initPos
        newllyVisited=[]
        
        while True:
            nextPos=[]
            # Update visited and update visited count
            if [curPos[0], curPos[1], curPos[2]] not in newllyVisited:
                newllyVisited.append([curPos[0], curPos[1], curPos[2]])                
            else:
                res += 1
                break

            # Compute next position
            if -2 < curPos[2] < 2:
                nextPos = [curPos[0], curPos[1]+ curPos[2], curPos[2]]
            else:
                nextPos = [curPos[0] + curPos[2]//2, curPos[1], curPos[2]]

            if nextPos[0] >= len(map[0]) or nextPos[1] >= len(map) or nextPos[0] < 0 or nextPos[1] < 0:
                break

            # 
            if map[nextPos[0]][nextPos[1]] == "#" or [nextPos[0], nextPos[1]] == potentialPos:
                next_dir = curPos[2]
                nextPos = [curPos[0], curPos[1], next_Dir[curPos[2]]]

            curPos = nextPos
            count +=1
        tries += 1

    gRun = False
    printTh.join()

    return res


def loops_mt(map, initPos, potentialPos):
    """
    Simulate the loops_mt logic. Replace this with your actual computation logic.
    """
    curPos = initPos
    newlyVisited = []
    next_Dir = [0, 2, -1, 0, 1, -2]  # Compute the next direction from the index of current direction

    while True:
        if [curPos[0], curPos[1], curPos[2]] not in newlyVisited:
            newlyVisited.append([curPos[0], curPos[1], curPos[2]])                
        else:
            return 1

        if -2 < curPos[2] < 2:
            nextPos = [curPos[0], curPos[1] + curPos[2], curPos[2]]
        else:
            nextPos = [curPos[0] + curPos[2] // 2, curPos[1], curPos[2]]

        if nextPos[0] >= len(map[0]) or nextPos[1] >= len(map) or nextPos[0] < 0 or nextPos[1] < 0:
                break

        if map[nextPos[0]][nextPos[1]] == "#" or [nextPos[0], nextPos[1]] == potentialPos:
            next_dir = curPos[2]
            nextPos = [curPos[0], curPos[1], next_Dir[curPos[2]]]

        curPos = nextPos

    return 0


def make_all_loops_mp(map, initPos, visited, print_progress=False):
    """
    Perform all path search in different processes using multiprocessing with optional printing.
    """
    visited.pop(0)
    visitedLen = len(visited)

    gRes = 0

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
                [(map, initPos, v, progress, lock) for v in visited]
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
    in_file = "06/inputs.data"
    out_file = "06/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

    try:
        times[0] = time.perf_counter()

        # Load inputs
        map, initPos = get_inputs(in_file)
        times[1] = time.perf_counter()

        # Compute the 1st challenge
        results[0], visited = count_visited_pos(map, initPos)
        times[2] = time.perf_counter()

        # Compute the 2nd challenge
        #results[1] = make_all_loops(map, initPos, visited)
        results[1] = make_all_loops_mp(map, initPos, visited, True)
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