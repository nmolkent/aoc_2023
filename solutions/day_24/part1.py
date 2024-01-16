from itertools import combinations
from fractions import Fraction

def linear_equation(x, y, vx, vy):
    dx: Fraction = Fraction(1, vx)
    m: Fraction = vy * dx
    #  y = mx + c
    c = y + (-x * m)
    # time 0 y = y
    # y - t0y = mx + c
    # t0 = mx + c + y
    return lambda number: (m * number + c)

def solve(filename: str):
    funcs = {}
    with open(filename) as file:
        for line in file:
            starts, velocities = line.split(" @ ")
            px, py, pz = map(int, starts.split(", "))
            vx, vy, vz = map(int, velocities.split(", "))
            # to calculate for y == 0 and x == 0
            funcs[line] = linear_equation(px, py, vx, vy)
    total = 0
    for x, y in combinations(funcs, 2):
        start = min([funcs[x], funcs[y]], key= lambda limit: limit(200000000000000))
        stop = min([funcs[x], funcs[y]], key= lambda limit: limit(400000000000000))
        if start != stop:
            total += 1
    return total

if __name__ == "__main__":
    solve("test1.txt")
