from solutions.day_12.part1 import recursive_combinations

def solve(filename: str):
    total = 0
    with open(filename) as file:
        for line in file:
            springs, broken_str = tuple(line.split(" "))
            broken = tuple(map(int, broken_str.split(",")))
            total += recursive_combinations(broken*5, ((springs + "?")*5)[:-1])
    return total
    
if __name__ == "__main__":
    solve("test1.txt")