from solutions.day_14.part1 import Direction
from collections import deque

class Mirror:
    def __init__(self, type: str, pos: tuple[int, int]):
        self.type = type
        self.pos = pos
    
    def get_next_directions(self, current_dir: Direction):
        if self.type == "|":
            return [d for d in Direction if d.pos_index() if d != current_dir.flip()]
        elif self.type == "-":
            return [d for d in Direction if d.weight_index() if d != current_dir.flip()]
        elif self.type == "\\":
            return [current_dir.turn_with_range_orientation()]
        elif self.type == "/":
            return [current_dir.turn_against_range_orientation()]
        else:
            raise Exception(f"unsupported mirror type: {self.type}")
        
def inlimits(pos, limit) -> bool:
    return 0 <= pos[0] < limit[0] and 0 <= pos[1] < limit[1]

def show(energised_tiles: set[tuple[int, int]], arr_size: tuple[int, int]) -> None:
    for i in range(arr_size[0]):
        for j in range(arr_size[1]):
            if (i, j) in energised_tiles:
                print("#", end="")
            else:
                print(".", end="")
        print()

def find_energised_tiles(initial_pos: tuple[int, int], initial_dir: Direction, mirrors: dict[tuple[int, int], Mirror], arr_limits: tuple[int, int]):
    heads = deque()
    heads.append((initial_dir, initial_pos))
    states = set()
    while len(heads):
        check_dir, check_pos = heads.popleft()
        if (check_dir, check_pos) not in states and inlimits(check_pos, arr_limits):
            states.add((check_dir, check_pos))
            if check_pos in mirrors:
                for d in mirrors[check_pos].get_next_directions(check_dir):
                    heads.append((d, d.of_pos(check_pos)))
            else:
                heads.append((check_dir, check_dir.of_pos(check_pos)))
    return {s[1] for s in states}


def solve(filename: str):
    mirrors: dict[tuple[int, int], Mirror] = {}
    with open(filename) as file:
        for i, line in enumerate(file):
            for j, char in enumerate(line.strip()):
                if char != ".":
                    mirrors[(i, j)] = Mirror(char, (i, j))
    arr_size: tuple[int, int] = (i+1, j+1)
    initial_pos: tuple[int, int] = (0, 0)
    energised = find_energised_tiles(initial_pos, Direction.East, mirrors, arr_size)
    return len(energised)

if __name__ == "__main__":
    solve("test1.txt")
