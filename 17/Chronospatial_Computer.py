import os
import sys
import time

# Quick and dirty
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from advent_utilities import write_out_file, print_timing, log
from advent_utilities import CRITICAL, ERROR, WARNIING, VERBOSE, DEBUG




def get_inputs(path: str, test=False):
    """
    Returns the input data.

    Parameter:
        path (str): Input path.
    Return:
        list: Input data.
    """
    prog=[]
    reg = [0,0,0]
    l = 0
    if test:
        path = path.split(".data")[0] + "_test.data"
    try:
        # Read the file
        with open(path, 'r') as file:
            for line in file:
                
                if 'Register A: 'in line:
                    reg[0] = int(line.split('Register A: ')[1])
                elif 'Register B: ' in line:
                    reg[1] = int(line.split('Register B: ')[1])
                elif 'Register C: ' in line:
                    reg[2] = int(line.split('Register C: ')[1])
                elif 'Program: ' in line:
                    prog.extend([int(x) for x in (line.split('Program: ')[1].split(','))])

                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        sys.exit(1)

    return prog, reg


def operand(opc: int, reg:list):
    if opc < 4:
        return opc
    elif opc == 4:
        return reg[0]
    elif opc == 5:
        return reg[1]
    elif opc== 6:
        return reg[2]
    else:
        log(ERROR, "Unknown OP code")


def operation(pc:int, ins:int, opc:int, reg:list, res: list ):

    # adv
    if ins == 0:
        reg[0] = int(reg[0]/2**operand(opc, reg))
    # blx
    elif ins == 1:
        reg[1] = int(reg[1] ^ opc)
    # bst
    if ins == 2:
        reg[1] = int((operand(opc, reg)%8) & 0b111)
    # jnz
    elif ins == 3:
        if reg[0] != 0:
            return opc             
    # bxc
    elif ins == 4:
        reg[1] = int(reg[1]^reg[2])
    # out
    elif ins == 5:
        res.append(int(operand(opc, reg)%8))
    # bdv
    elif ins == 6:
        reg[1] = int(reg[0]/2**operand(opc, reg))
    # cdv
    elif ins == 7:
        reg[2] = int(reg[0]/2**operand(opc, reg))

    pc += 2
    return pc

def run_program(program, reg, res):
    pc = 0
    while pc < len(prog)-1:
        pc = operation(pc, prog[pc], prog[pc+1], reg, res)

if __name__ == '__main__':
    # Default file paths
    in_file = "17/inputs.data"
    out_file = "17/outputs.data"

    results = [0, 0]
    times = [0., 0., 0., 0.]

    max_error = 1

# try:
    times[0] = time.perf_counter()

    # Load inputs
    prog, reg = get_inputs(in_file, False)
    times[1] = time.perf_counter()

    # Compute the 1st challenge
    res = []
    run_program(prog, reg, res)

    results[0] = str(res) # 4,6,3,5,6,3,5,2,1,0
    times[2] = time.perf_counter()

    # Compute the 2nd challenge
    results[1] = get_best_res(validPath)
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