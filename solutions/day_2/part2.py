
def solve(filename):
    power_sum = 0
    with open(filename) as file:
        for line in file:
            # power initialised at 1 for product, greatest dict initialised at 0 for sum
            power = 1
            greatest = {"red": 0, "green": 0, "blue": 0}
            moves = line.strip().split(": ")[1]
            for pull in moves.split("; "):
                for number, colour in [tuple(move.split(" ")) for move in pull.split(", ")]:
                    if greatest[colour] < int(number):
                        greatest[colour] = int(number)
            for v in greatest.values():
                power *= v
            power_sum += power
    return power_sum

if __name__ == "__main__":
    solve("test1.txt")
