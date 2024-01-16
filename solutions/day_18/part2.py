from utils.pathfinder import Pos, Compass
from solutions.day_18.part1 import get_area


def solve(filename: str):
    compass_dirction = {
        "0": Compass.East,
        "1": Compass.South,
        "2": Compass.West,
        "3": Compass.North
    }
    lead_pos = Pos(0, 0)
    visited: dict[Pos, tuple[Compass, int]] = {}
    reversed: dict[Pos, tuple[Compass, int]] = {}
    with open(filename) as file:
        for line in file:
            hex = line.strip().split("#")[-1][:-1]
            intensity = int(hex[:-1], 16)
            direction = compass_dirction[hex[-1]]
            visited[lead_pos] = (direction, intensity)
            lead_pos = direction.of_pos(lead_pos, intensity)        
            reversed[lead_pos] = (direction.flip(), intensity)
    reversed[Pos(0, 0)] = (direction.flip(), intensity)
    paired = {}
    # realign positions to zero
    shift_pos = Pos(
        -min(visited.keys(), key=lambda x: x.row).row,
        -min(visited.keys(), key=lambda x: x.col).col
    )
    limit_pos = Pos(
        shift_pos.row + max(visited.keys(), key=lambda x: x.row).row + 1,
        shift_pos.col + max(visited.keys(), key=lambda x: x.col).col + 1
    )
    print(shift_pos)
    print(limit_pos)

    for k, v in reversed.items():
        paired[k.move(shift_pos)] = (v, visited[k])

    # show(limit_pos, set(paired.keys()))
    result = get_area(limit_pos, paired)
    return result

if __name__ == "__main__":
    solve("test1.txt")
