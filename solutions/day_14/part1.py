from functools import cache
from enum import Enum

class Direction(Enum):
    # bits represent weight index, pos index and is_start respectively
    # (i, j) represents a position and directions each store a binary representation of range details
    North = int("11", 2)
    West = int("101", 2)
    South = int("10", 2)
    East = int("100", 2)

    def weight_index(self) -> int:
        return int(bool(self.value & int("100", 2)))

    def pos_index(self) -> int:
        return int(bool(self.value & int("10", 2)))

    def range_orientation(self) -> int:
        return 1 if self.is_start() else -1

    def is_start(self) -> int:
        return self.value & int("1", 2)
    
    def start(self, length: int) -> int:
        return 0 if self.is_start() else length
        
    def stop(self, length: int) -> int:
        return length if self.is_start() else -1
        
    def limit(self, length: int) -> int:
        return 0 if self.is_start() else length - 1
    
    def of_pos(self, pos: tuple[int, int]):
        return pos[0] + (-self.range_orientation() * self.pos_index()), pos[1] + (-self.range_orientation() * self.weight_index())
    
    def turn_with_range_orientation(self):
        return Direction(self.value ^ int("110", 2))

    def turn_against_range_orientation(self):
        return Direction(self.value ^ int("111", 2))
    
    def flip(self):
        return Direction(self.value ^ int("1", 2))


    def rebuild(self, pos: int, weight: int)->tuple[int, int]:
        return (pos, weight) if self.weight_index() else (weight, pos)

    def calc_sum(self, rolls, arr_size)->int:
        weight = arr_size[self.weight_index()]
        total = 0
        for i in range(arr_size[0]):
            for j in range(arr_size[1]):
                if (i, j) in rolls:
                    total += weight + ((i, j)[self.weight_index()] * -self.range_orientation())
        return total

    def roll_loop(self, rolls: set[tuple[int, int]], blocks: set[tuple[int, int]], arr_size: tuple[int, int]) -> set[tuple[int, int]]:
        new_rolls = set()
        length = arr_size[self.weight_index()]

        # each pos_index represents a line rolling in the same direction
        for pos in range(arr_size[self.pos_index()]):
            # initialise the range and limit
            limit: int = self.limit(length)
            for weight in range(self.start(length), self.stop(length), self.range_orientation()):
                if self.rebuild(pos, weight) in rolls:
                    # add blocks in order they were encountered, the limit will increase by the number added
                    new_rolls.add(self.rebuild(pos, limit))
                    limit += self.range_orientation()
                if self.rebuild(pos, weight) in blocks:
                    # the limit will increase to the blok + the direction of the range
                    limit = weight + self.range_orientation() 
        return new_rolls

def show(rolls: set[tuple[int, int]], blocks: set[tuple[int, int]], arr_size: tuple[int, int]) -> None:
    for i in range(arr_size[0]):
        for j in range(arr_size[1]):
            if (i, j) in rolls:
                print("O", end="")
            elif (i, j) in blocks:
                print("#", end="")
            else:
                print(".", end="")
        print()

def solve(filename: str):
    blocks, rolls = set(), set()
    with open(filename) as file:
        for i, line in enumerate(file):
            for j, char in enumerate(line.strip()):
                if char == "#":
                    blocks.add((i, j))
                elif char == "O":
                    rolls.add((i, j))
    arr_size: tuple[int, int] = (i+1, j+1)
    d = Direction.North
    n: set[tuple[int, int]] = d.roll_loop(rolls, blocks, arr_size)
    result = d.calc_sum(n, arr_size)
    return result

if __name__ == "__main__":
    solve("test1.txt")
