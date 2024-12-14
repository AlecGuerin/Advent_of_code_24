import os
import sys
import time

from math import gcd

import re
# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file, print_timing


def get_inputs(path: str, test=False):
    """
    Returns the input data.

    Parameter:
        path (str): Input path.
    Return:
        list: Input data.
    """
    data=[]
    
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:
            x = 0
            cnt = 0
            d = []
            for line in file:
                
                pattern = r'X[+=](\d+)|Y[+=](\d+)'
                matches = re.findall(pattern, line)
                if len(matches) > 0:
                    matches = [int(x) for x in [matches[0][0], matches[1][1]]] # Not beautifull but fast implementation
                    d.append(matches)
                    cnt += 1
                    if cnt == 3:
                        data.append(d.copy())
                        cnt = 0
                        d.clear()
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return data


def compute_inputs(data):
    """
    Compute the optimization for inputes using naive aproche.

    Parameter:
        data (list): Equation constraints.

    Return:
        Minimal cost to solve of solvable problems.
    """
    cost = 0
    for d in data:
        known_cost = set()
        combine_path(d, known_cost)
        if len(known_cost)> 0:
            cost += min(known_cost)
    return cost


def combine_path(data, knowCost:set):
    """
    Naivelly find all possible combnaisons and corresponding cost.

    Parameter:
        knowCost (set): Set containing the know cost.

    Return:
        set: Known possible cost.
    """
    i =0
    while i < 100:
        est1 = data[0][0] * i # Estimate current x position with A button
        # if x is more than destination, nothing else can be done!
        if est1 > data[2][0]: 
            break
        j = 0        
        while j < 100:       
            est2 = est1 + data[1][0] * j # Estimate current x position combinaison of both buttons 
            # CHeck if x match destination
            if est2 == data[2][0]:
                yEst = i * data[0][1] + j * data[1][1] # Compute corresponding y
                # If x and y matches: add to known cost
                if yEst == data[2][1]:
                    knowCost.add(i*3 + j)
                # If y is bigger than expected y, no need to go futher in this loop
                elif yEst > data[2][1]:
                    break
            elif est2 > data[2][0]:
                break
            j += 1    
        i +=1


def optimize_long_inputs(data):
    """
    Compute the optimization for inputes using diopantine solver.

    Parameter:
        data (list): Equation constraints.

    Return:
        Minimal cost to solve of solvable problems.
    """
    res =0
    for d in data:
        res += solve_diophantine(d)
    return res


def solve_diophantine(data, cost_a =3, cost_b=1):
    """
    Diopantine solver for contraint equations in form: [(Ax*x + Bx*y = X), (Ay*x + By*y = Y)].

    Parameters:
        data (list): Constraints.
        cost_a (int): Cost of using A button.
        cost_b (int): Cost of using B button.

    Return:
        Minimal cost to solve the probleme if solvable, else 0.
    """

    # Extract x of the constrtained equations:
    # [(Ax*x + Bx*y = X), (Ay*x + By*y = Y)] => (Ax*By − Ay*Bx) * x = X*By − Y*Bx => g1*x = g2
    # x = g2/g1
    g1 = data[0][0] * data[1][1] - data[0][1] * data[1][0] # Denominator
    if g1 == 0:
        return 0 # No unique solution exists (parallel or coincident lines)
    
    g2 = data[2][0] * data[1][1] - data[2][1] * data[1][0] # Numerator

    # Make sur x is integer
    if g2 % g1 != 0:
        return 0 # No integer solution exists

    # Solve x
    x0 = g2 // g1

    # Substitute x into the first equation to find y
    if data[0][0] != 0:
        y0 = (data[2][0] - data[0][0] * x0) // data[1][0] # y0 = X - Ax*x0
    else:
        y0 = (data[2][1] - data[0][1] * x0) // data[1][1] # y0 = Y -Ay*x0

    min_cost = float('inf')
    dsX = (data[1][0] // gcd(data[1][0], data[1][1])) # Diophantine shift in X (Bx / gcd(Bx, By))
    dsY = (data[0][0] // gcd(data[0][0], data[0][1])) # Diophantine shift in Y (Ax / gcd(Ax, Ay))

    # Keep value of optimal x and y
    # optimal_x = -1
    # optimal_y = -1 
    
    # Iterate to minimize cost by incrementing x with possible values and decrementing y by possible values: g1​⋅x=g2
    for i in range(-abs(g1), abs(g1)):
        # Get higer x while having lower y
        x = x0 + i * dsX # x = x0 + i*dsX 
        y = y0 - i * dsY # y = y0 - i*dsY

        # Check [(Ax*x + Bx*y = X), (Ay*x + By*y = Y)]
        if data[0][0] * x + data[1][0] * y == data[2][0] and data[0][1] * x + data[1][1] * y == data[2][1]:  # Verify solutions
            cost = cost_a * x + cost_b * y # Compute cost
            if cost < min_cost:
                min_cost = cost
                # optimal_x = x
                # optimal_y = y

    if min_cost is not float('inf'):
        return min_cost
    else:
        return 0 # No feasible solution exists


def update_data(data):
    """
    Update the data to match 2nd part of problem.
    """
    for d in data:
        d[2][0] += 10000000000000
        d[2][1] += 10000000000000

if __name__ == '__main__':
    # Default file paths
    in_file = "13/inputs.data"
    out_file = "13/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

# try:
    times[0] = time.perf_counter()

    # Load inputs
    data = get_inputs(in_file, False)
    times[1] = time.perf_counter()

    
    # Compute the 1st challenge
    results[0] = compute_inputs(data)
    times[2] = time.perf_counter()

    update_data(data)

    # Compute the 2nd challenge   
    results[1] = optimize_long_inputs(data)
    times[3] = time.perf_counter()

    print(f"First challenge : {results[0]}")
    print(f"Second challenge: {results[1]}")

    # Save the results
    write_out_file(out_file, results)

    # Print timing statistics
    print_timing(times)

# except Exception as e:
#     print(f"An error occurred: {e}")
#     sys.exit(1)

    sys.exit()