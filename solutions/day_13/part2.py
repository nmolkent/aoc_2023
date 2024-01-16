from collections import defaultdict
from solutions.day_13.part1 import find_reflection

def solve(filename):
    arrs = defaultdict(list)
    i = 0
    with open(filename) as file:
        for line in file:
            if len(line.strip()) == 0:
                i += 1
            else:
                arrs[i].append(list(line.strip()))
    total = 0
    for a in arrs.values():
        # part 1 code just works assuming there is only ever 1 swap that will result in a new reflection
        # by considering that a reflection only counts if the total diff at the end is 1 because we have only removed 1 smudge
        total += find_reflection(a, 1)
    return total

if __name__ == "__main__":
    solve("test1.txt")
    