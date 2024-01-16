
# inspired by factorial style recursion problems
# cache stops this being horribly inefficient and sets initialisation values for the base condition

cache = {0: 0, 1: 1}
def lottorial(i: int)->int:
    if i not in cache:
        cache[i] = lottorial(i-1) * 2
    return cache[i] 

def solve(filename):
    total = 0
    with open(filename) as file:
        for line in file:
            p1, p2 = tuple(line.split(":")[1].strip().split("|"))
            # intersection provides a set of winning tickets
            wins = len(set({c for c in p1.strip().split(" ") if c != ""}).intersection(set({c for c in p2.strip().split(" ") if c != ""})))
            total += lottorial(wins)
    return total

if __name__ == "__main__":
    solve("test1.txt")
