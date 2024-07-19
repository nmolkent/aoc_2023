# initial ideas, pathfind both directions at once checking neighbors
# the pos class will help simplify the coordinate math and checks

from typing import List


class Pos:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __add__(self, other):
        return Pos(self.i + other.i, self.j + other.j)
    
    def __sub__(self, other):
        return Pos(self.i - other.i, self.j - other.j)
    
    def inlimits(self, limiti, limitj):
        return 0 <= self.i < limiti and 0 <= self.j < limitj 
    
    def __eq__(self, other):
        return self.i == other.i and self.j == other.j
    
    def __hash__(self):
        return hash((self.i, self.j))
    
    def __repr__(self):
        return f"Pos({self.i}, {self.j})"

class PipeLoop:
    neighbors_list = [Pos(0, 1), Pos(1, 0), Pos(-1, 0), Pos(0, -1)]
    pipes = {
        "-": {Pos(0, -1), Pos(0, 1)},
        "|": {Pos(-1, 0), Pos(1, 0)},
        "L": {Pos(-1, 0), Pos(0, 1)},
        "7": {Pos(1, 0), Pos(0, -1)},
        "J": {Pos(-1, 0), Pos(0, -1)},
        "F": {Pos(1, 0), Pos(0, 1)},
        ".": set()
    }
    def __init__(self, map_array: List[str], start: Pos):
        self.map_array = map_array
        self.start = start
        self.limiti = len(map_array)
        self.limitj = len(map_array[0])
        # the visited set contains only pipe Pos values 
        self.visited_set = {start}
        self.inside_set = set()

    def neighbors(self, pos: Pos):   
        pre_filter = [pos + n for n in self.neighbors_list]
        return [p for p in pre_filter if p.inlimits(self.limiti, self.limitj)]

    def connecting_pipes(self, pos: Pos):
        # assume pipes will always connect from start in a loop
        return {pos + p for p in self.pipes[self.show(pos)]}

    def show(self, pos):
        return self.map_array[pos.i][pos.j]
    
    def colourMeDebug(self, pipe_set, inside_set):
        from termcolor import colored
        # shows the pipemap with tiles considered inside as red
        for i in range(self.limiti):
            for j in range(self.limitj):
                if Pos(i, j) in pipe_set:
                    print(colored(self.show(Pos(i, j)), "blue"), end="")
                elif Pos(i, j) in inside_set:
                    print(colored(self.show(Pos(i, j)), "red"), end="")
                else:
                    print(self.show(Pos(i, j)), end="")
        print()

    def print_solved_map(self):
        self.colourMeDebug(self.visited_set, self.inside_set)
    
    def find_perimiter(self)->None:
        traveled = 0
        # keep track of te left and right pointers simultaneously until 
        left, right = tuple([p for p in self.neighbors(self.start) if self.start in self.connecting_pipes(p)])
        # change the S char in the pipe_map global variable so it reflecs its actual piece otherwise this char represents a break in the pipe
        for char, positions in self.pipes.items():
            if {left - self.start, right - self.start} == positions:
                self.map_array[self.start.i] = self.map_array[self.start.i].replace("S", char)
                assert self.map_array[self.start.i][self.start.j] != "S"

        while not (left in self.visited_set or right in self.visited_set):
            self.visited_set.add(left)
            self.visited_set.add(right)
            traveled += 1
            try:
                left = self.connecting_pipes(left).difference(self.visited_set).pop()
                right = self.connecting_pipes(right).difference(self.visited_set).pop()
            except:
                break
        self.mid_point = traveled

    def find_inside_area(self):
        # find the upper left corner
        min_i = min(self.visited_set, key = lambda x: x.i).i
        first_line = {v for v in self.visited_set if v.i == min_i}
        first_corner = min(first_line, key = lambda x: x.j)

        # before sterting the loop we need to populate both the last state and the next state
        last_piece = first_corner  # F
        last_dir = Pos(0, 1)  # travel right
        next_piece = last_piece + last_dir # the next piece will follow the direction of travel
        # check the possible next directions by excluding the direction that takes you back to where you came from
        next_dir = [d for d in self.pipes[self.show(next_piece)] if d + next_piece != last_piece][0]
        last_check = last_piece + Pos(1, 1) # set the value of last checked for the corner to enforce only inside checks
        # while we haven't actually checked this it will be checked at the last stage of the loop if not beffore then

        # loop to move round the perimiter
        while next_piece != first_corner:
            newly_added = self.positions_to_check(last_check, last_piece, last_dir, next_piece, next_dir)
            check_set = {p for p in newly_added if p not in self.visited_set and p not in self.inside_set}
            # loop to find all neighbours of all values in check_set
            while len(check_set) > 0:
                current_check_pos = check_set.pop()
                self.inside_set.add(current_check_pos)
                for n in self.neighbors(current_check_pos):
                    if n not in self.visited_set and n not in self.inside_set:
                        check_set.add(n)
            # update state for next iteration
            last_piece = next_piece
            last_dir = next_dir
            next_piece = last_piece + last_dir
            next_dir = [d for d in self.pipes[self.show(next_piece)] if d + next_piece != last_piece][0]
            last_check = newly_added[-1]

    def positions_to_check(self, last_check, last_pos, last_dir, next_pos, next_dir) -> List[Pos]:
        # return new tiles to check or the last check if no new tiles to check because we always need a last checked to maintain continuity on the inside
        next_marker = self.show(next_pos)
        last_marker = self.show(last_pos)

        # was inside corner next straight; x == y, return the last check again
        # F-
        # Lx
        if next_marker in ["|", "-"] and last_check in self.neighbors(next_pos):
            return [last_check]
        
        # was either an outside corner or straight, next straight
        # either way theres only 1 last check which would be the same either way, x lastcheck, y next check, direction of travel determines the next check
        # y|
        # xL
        elif next_marker in ["|", "-"]:
            return [last_check + last_dir]
        
        # was an inside corner and next an inside corner; x lastcheck y nextcheck; we want to make the value of last check the diagonal
        # this diagonal will have already been checked or may be part of the pipes
        # next_pos = F, last_pos = L
        # Fx-
        # Ly-
        elif last_marker in ["L", "J", "7", "F"] and next_pos + next_dir == last_check:
            return [last_pos + next_dir]
        
        # was an inside corner next a outside corner x = lastcheck and nextcheck, y = next_check
        # lastpos = J, nextpos = F
        #  y
        # xF-
        # -J
        elif last_marker in ["L", "J", "7", "F"] and next_pos - next_dir == last_check:
            # only need to return y as x already checked
            return [next_pos + last_dir]
        
        # was an outside corner or straight, now an inside corner x = lastcheck and nextcheck
        # nextpos = J lastpos = F
        #  x|
        # -FJ
        elif last_pos + next_dir == last_check:
            return [last_check]
        
        # was an outside corner or straight, now an outside corner or straight
        # nextpos 
        #  y
        # yF
        # xL
        elif last_pos - next_dir == last_check:
            return [last_check + last_dir, next_pos + last_dir]
        
        else:
            raise Exception("Conditions ae not sufficient to find all cases!")

def solve(filename):
    # read the whole map in first as an array of strings (treat it as a 2d array with the sring being a char array)
    pipe_map = []
    with open(filename) as file:
        for i, line in enumerate(file):
            if line.find("S") >= 0:
                start = Pos(i, line.index("S"))
            pipe_map.append(line)
    solver = PipeLoop(pipe_map, start)
    solver.find_perimiter()
    return solver.mid_point

if __name__ == "__main__":
    solve("test1.txt")
