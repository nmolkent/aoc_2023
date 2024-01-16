
def solve(filename):
    valid_moves_sum = 0

    game_rules = {"red": 12, "green": 13, "blue": 14}
    
    with open(filename) as file:
        for line in file:
            game_number, game = tuple(line.strip().split(": "))
            valid = True
            # game is split into pulls each of which may contain multiple colours
            for pull in game.split("; "):
                for number, colour in [tuple(move.split(" ")) for move in pull.split(", ")]:
                    if game_rules[colour] < int(number):
                        valid=False
                        break
            if valid:
                valid_moves_sum += int(game_number.split(" ")[1])
    return valid_moves_sum

if __name__ == "__main__":
    solve("test1.txt")
