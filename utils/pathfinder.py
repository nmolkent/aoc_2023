from enum import Enum
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Pos:
    row: int
    col: int

    def in_limit(self, other):
        return 0 <= self.row < other.row and 0 <= self.col < other.col 
    
    def move(self, shift_pos):
        return Pos(self.row + shift_pos.row, self.col + shift_pos.col)

class Compass(Enum): 
    # bits represent intensity index, (ie the index of the tuple that represents how far in a direction)
    # pos index (the index that represents different available array positions that a direction can start and end in)
    # and is_start (in order to deternine whether a range will start at 0 or max of the respective array)
    # (i, j) represents a position and is interchangable with the pos class (though indexing has been used to amintain compatibility with both)
    North = int("11", 2)
    West = int("101", 2)
    South = int("10", 2)
    East = int("100", 2)
    Stationary = 0
    
    def symbol(self) -> str:
        return {
            0: "0",
            Compass.North.value: "^",
            Compass.East.value: ">",
            Compass.South.value: "v",
            Compass.West.value: "<"
        }[self.value]

    def intensity_index(self) -> int:
        return int(bool(self.value & int("100", 2)))

    def pos_index(self) -> int:
        return int(bool(self.value & int("10", 2)))
    
    def is_vertical(self):
        return self.pos_index()

    def range_orientation(self) -> int:
        return 1 if self.is_start() else -1
    
    def is_inclusive_turn(self, other):
        # day 18
        return self.is_start() == other.is_start()
    
    def faces_southeast(self):
        return not self.is_start()

    def is_start(self) -> int:
        return self.value & int("1", 2)
    
    def start(self, length: int) -> int:
        return 0 if self.is_start() else length
        
    def stop(self, length: int) -> int:
        return length if self.is_start() else -1
        
    def limit(self, length: int) -> int:
        return 0 if self.is_start() else length - 1
    
    def of_pos(self, pos: Pos, intensity=1)->Pos:
        return Pos(pos.row + (-self.range_orientation() * self.pos_index() * intensity), pos.col + (-self.range_orientation() * self.intensity_index() * intensity))
    
    def turn_with_range_orientation(self):
        return Compass(self.value ^ int("110", 2))

    def turn_against_range_orientation(self):
        return Compass(self.value ^ int("111", 2))
    
    def flip(self):
        return self if self.value == 0 else Compass(self.value ^ int("1", 2))

    def rebuild(self, pos_value: int, intensity_value: int)->Pos:
        return Pos(pos_value, intensity_value) if self.intensity_index() else Pos(intensity_value, pos_value)

@dataclass(frozen=True)
class Action:
    pos: Pos
    direction: Compass
    intensity: int = 0

    def cost(self, other):
        return abs(self.pos.row - other.row) + abs(self.pos.col - other.col)
    
    
@dataclass(order=True)
class PriorityAction:
    priority: int
    action: Action = field(compare=False)