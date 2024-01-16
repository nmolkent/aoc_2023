
from collections import defaultdict

# default dict assumes we start with 1 of each lottery ticket
# on each iteration future lotery tickets can have coppies made
copies = defaultdict(lambda: 1)

# for the current ticket lookahead according to the number of wins
# for each ticket in the lookahead we add another ticket for each copy we have of this ticket
def jackpot(this_ticket: int, wins: int):
    for i in range(this_ticket, this_ticket + wins):
        copies[i + 1] += copies[this_ticket]
    return copies[this_ticket] # will initialise copies with 1 if there are no wins

def solve(filename):
    with open(filename) as file:
        for i, line in enumerate(file, start=1):
            p1, p2 = tuple(line.split(":")[1].strip().split("|"))
            # intersection provides a set of winning tickets
            wins = len(set({c for c in p1.strip().split(" ") if c != ""}).intersection(set({c for c in p2.strip().split(" ") if c != ""})))
            jackpot(i, wins)
    return sum(copies.values())

if __name__ == "__main__":
    solve("test1.txt")
