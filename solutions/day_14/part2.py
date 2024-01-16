from solutions.day_14.part1 import Direction

def washing_machine(rolls, blocks, arr_size)->set[tuple[int, int]]:
    for d in Direction:
        rolls = d.roll_loop(rolls, blocks, arr_size)
    return rolls

def solve(filename):
    blocks, rolls = set(), set()
    with open(filename) as file:
        for i, line in enumerate(file):
            for j, char in enumerate(line.strip()):
                if char == "#":
                    blocks.add((i, j))
                elif char == "O":
                    rolls.add((i, j))
    arr_size: tuple[int, int] = (i+1, j+1)

    stored_loops = []
    start = 1000000000
    loopIdx = False
    while not loopIdx:
        # add state to store
        stored_loops.append(rolls)
        # create new state
        rolls: set[tuple[int, int]] = washing_machine(rolls, blocks, arr_size)
        # check if new state matches previous states and store the index if so
        for i, past in enumerate(stored_loops):
            if past == rolls:
                loopIdx = True
                break
        # decrimenting start will allow us to find the remainder
        start -= 1

    infinite_loop = stored_loops[i:]
    result = Direction.North.calc_sum(infinite_loop[start % len(infinite_loop)], arr_size)
    return result

if __name__ == "__main__":
    solve("test1.txt")
