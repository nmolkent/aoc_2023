

def solve(filename: str):
    lead = set()
    lag = set()
    block = set()
    with open(filename) as file:
        for i, line in enumerate(file):
            for j, char in enumerate(line):
                if char == "S" in line:
                    start = (i, j)
                if char == "#":
                    block.add((i, j))
    for i in range(6):
        


    first_move = 0
    second_move = 0
    first_leading_pos
    while i < 
    result = ...
    return result

if __name__ == "__main__":
    solve("test1.txt")
