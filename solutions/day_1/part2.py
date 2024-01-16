# assuming zero does not occur in strings
# dict is dual purpose, serving to turn words into respective digits but also provide the full spectrum of matches when using items
digit_dict = {
    "one": "1", 
    "two": "2", 
    "three": "3", 
    "four": "4", 
    "five": "5", 
    "six": "6", 
    "seven": "7", 
    "eight": "8", 
    "nine": "9"
}

# assuming each line has 1 number, start will be lazily set for the first number, end will be greedily set for every number
def getDigit(s):
    start, end = "", ""
    for i in range(len(s)):
         for word, number in digit_dict.items():
            if s[i:].startswith(word) or s[i] == number:
                if len(start) == 0:
                    start = number
                end = number
    return int(start + end)

def solve(filename):
    total = 0
    with open(filename) as file:
        for line in file:
            total += getDigit(line.strip())
    return total

if __name__ == "__main__":
    solve("test1.txt")
