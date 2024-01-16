from collections import deque

def solve(filename):
    # Why count indexes by hand [=
    i1 = len("HFF") 
    i2 = len("HFF = (")
    i3 = len("HFF = (HRR")
    i4 = len("HFF = (HRR, ")
    i5 = len("HFF = (HRR, BSG")

    nodes = {}
    with open(filename) as file:
        for i, line in enumerate(file):
            if i < 1:
                # we can rotate a deque and set it to be fixed size making it efficient to check 
                dirs = deque([int(l == "R") for l in line.strip()], len(line.strip())) 
            elif i > 1:
                name = line[:i1]
                left = line[i2:i3]
                right = line[i4:i5]
                nodes[name] = (left, right)
    root = "AAA"
    i = 0
    while root != "ZZZ":
        dir = dirs.popleft()
        dirs.append(dir)
        root = nodes[root][dir]
        i += 1
    return i

if __name__ == "__main__":
    solve("test1.txt")
