from collections import deque
from math import lcm

# only additional consideration on this round is first, to pop the initial chalenge solution into a function in order to use it repeatedly
# second use lcm to find the lowest comon multiple of all the solutions (the length of the dirs reppeating pattern should be included)
def solve(filename):
    i1 = len("HFF")
    i2 = len("HFF = (")
    i3 = len("HFF = (HRR")
    i4 = len("HFF = (HRR, ")
    i5 = len("HFF = (HRR, BSG")

    nodes = {}
    with open(filename) as file:
        for i, line in enumerate(file):
            if i < 1:
                dirs = deque([int(l == "R") for l in line.strip()], len(line.strip()))
            elif i > 1:
                name = line[:i1]
                left = line[i2:i3]
                right = line[i4:i5]
                nodes[name] = (left, right)
    
    lengths = [len(dirs)]
    for n in nodes:
        if n[2] == "A":
            l = find_path(n, dirs.copy(), nodes)
            lengths.append(l)
    result = lcm(*lengths)
    return result

def find_path(root, dirs, nodes):
    i = 0
    while root[2] != "Z":
        dir = dirs.popleft()
        dirs.append(dir)
        root = nodes[root][dir]
        i += 1
    return i

if __name__ == "__main__":
    solve("test1.txt")