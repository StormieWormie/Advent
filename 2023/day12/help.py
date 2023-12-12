import numpy as np
import re

def process_input(line):
    info = line.split()
    slots = re.findall('[#/?]+',info[0])
    values = [int(i) for i in info[1].split(',')]
    return slots, values

def fit_value2slot(slot,value):
    n = len(slot)
    if n<value:
        return 0    #doesn't fit
    if n==value:
        return 1    #perfectly fits
    if '#' not in slot:
        return 1 + (n-value)
    mandatory = np.argwhere([s=='#' for s in slot]).flatten()
    left,right = mandatory[0], mandatory[-1]
    mandatory_size = 1+(right-left)
    if mandatory_size > value:
        return 0
    overflow = value-mandatory_size
    L,R = min(left,overflow),min(right,overflow)
    return 1 + (L+R-overflow)

def fit_value2slots(slots,value):
    # print(slots,value)
    N = len(slots)
    if N==0:
        return 0
    if N==1:
        return fit_value2slot(slots[0],value)
    mandatory = ['#' in slot for slot in slots]
    Nmand = sum(mandatory)
    if Nmand > 1:
        return 0    #Too many mandatory slots
    if Nmand == 1:
        I = np.argwhere(mandatory).flatten()[0]
        return fit_value2slot(slots[I],value)
    count = 0
    for slot in slots:
        n = len(slot)
        if n >= value:
            count += 1 + (n-value)
    return count
    
def cut_slots(slots, cut):
    N = len(slots)
    slot = slots[0]
    n = len(slot)
    if n<cut:
        print("Should not be reached! (cut_slots)")
        return None
    elif n<=cut+1:
        if N==1:
            return []
        else:
            return slots[1:]
    else:
        if N==1:
            return [slot[cut+1:]]
        else:
            return [slot[cut+1:]] + slots[1:]

    

def fit_values2slots(slots,values):
    N = len(slots)
    V = len(values)
    if N==0 or V==0:
        # print("Nothing to be done", slots, values)
        return 0
    value = values[0]
    if V==1:
        return fit_value2slots(slots,value)
    
    worth = True
    count = 0
    for s in range(N):
        slot = slots[s]
        n = len(slot)
        if value<=n:
            for i in range(n-value+1):
                misfit = False
                cut = value+i
                if cut < n: #if not, we are on the end of the slot so the following token is '.' 
                    if slot[cut] == '#':
                        misfit = True #If true, the next token is '#' so value should move up as it would force the '#' to '.' (impossible)
                if not misfit:
                    new_slots = cut_slots(slots[s:],cut)
                    # print('-sub_call',new_slots, values[1:])
                    add_count = fit_values2slots(new_slots,values[1:])
                    count += add_count
                    # print('--sub_result',new_slots, values[1:],add_count)
                    if add_count == 0:
                        worth = False
                        break

                if slot[i] == '#':
                    worth = False #If the leftmost token is mandatory, I cannot move the leftmost value to the right
                    break
        else:
            pass
            # print(value, ' doesnt fit in ', slot)
        if '#' in slot:
            worth = False #If there are mandatory tokens in this slot, I cannot skip it so no need to look at further slots for the leftmost value
            break
    return count

def part1(filename):
    file = open(filename)
    p1 = 0
    for line in file.readlines():
        slots, values = process_input(line)
        ap1 = fit_values2slots(slots,values)
        p1 += ap1
        # print(line.removesuffix('\n'), '->', ap1)
    return p1

if __name__ == "__main__":
    part1_result = part1('input.txt')
    print(part1_result)