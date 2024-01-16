import argparse
import sys
import os
from importlib import import_module

parser = argparse.ArgumentParser(
    prog="aoc_2023",
    usage='%(prog)s [day] [part] --filename',
    description="runs solutions for the 2023 advent of code challenge. Solutions written by neilmolky"
)
parser.add_argument(
    "day", nargs=1, type=int, choices=list(range(1, 26))
)
parser.add_argument(
    "part", nargs=1, type=int, choices=list(range(1, 3)),
    help="part: "
)
parser.add_argument(
    "--filename", "-f", nargs=1, type=str, choices=["data.txt"] + [f"test{i}.txt" for i in range(9)], # for now i can't forsee any more than 9 toy datasets for dev purposes 
    default=["data.txt"], required=False
)
if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = parser.parse_args(args)
    module = import_module(f"solutions.day_{cmd.day[0]}.part{cmd.part[0]}")
    path = os.path.join(os.path.dirname(__package__), f"data/day_{cmd.day[0]}/{cmd.filename[0]}") 
    result = module.solve(path)
    print(result)
