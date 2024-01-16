from dataclasses import dataclass
from utils.compass import Compass

@dataclass(frozen=True)
class Pos:
    row: int
    col: int

    def in_limit(self, other):
        return 0 <= self.row < other.row and 0 <= self.col < other.col
    
    def __sub__(self, other):
        return Pos(self.row - other.row, self.col - other.col)

@dataclass(frozen=True)
class Action:
    pos: Pos
    direction: Compass