from solutions.day_10.part1 import PipeLoop, Pos

# reflections: This was prety tough. findig the loop was required for both parts so initially I didn't split into part 1 and 2
# during the refactor I decided to use oop as the implementation was heavy on stateful changes
# the colourmedubug function was a nice idea for debugging and can show the solution nicely

def solve(filename):
    pipe_map = []
    with open(filename) as file:
        for i, line in enumerate(file):
            if line.find("S") >= 0:
                start = Pos(i, line.index("S"))
            pipe_map.append(line)
    pipes = PipeLoop(pipe_map, start)
    pipes.find_perimiter()

    # part 2 solution explained

    # find the top left corner pipe which will by design be an F pipe
    # we know that the inside of this piece will be diagonally down and right
    # if we travel round the pipes visited only looking inwards we will find internal spaces/pipes 
    # (yes pipes not connected to the loop can be inside the pipe loop, fortunately if they are themselves loops they do not block the inside!)
    # we use the last and next to create a state for each time we look inwards (current state keeps changing so last and next actully helped me overcome alot of confusion)
    # when looking inwards if we find a position that is not in the pipes visited set we enter a find loop
    # in the find loop we will add positions to the inside set
    # the inside set becomes a part of the PipeLoop object
    # the coloured map is quite nice to see in the terminal too

    pipes.find_inside_area()
    return len(pipes.inside_set)

if __name__ == "__main__":
    solve("test1.txt")