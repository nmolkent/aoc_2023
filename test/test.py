import unittest
import os
from importlib import import_module

class GeneralTestCase(unittest.TestCase):
    def __init__(self, methodName, day: int):
        super(GeneralTestCase, self).__init__(methodName)
        self.day = day

    def __test_builder(self, part: int, test: bool):
        message = "standard test data" if test else "personal input data"
        test_path = f"data/day_{self.day}/test{part}.txt" if test else "data/day_{self.day}/data.txt"
        solution = get_solution_record(self.day, part, test)
        if not solution:
            self.fail(f"A solution for day {self.day}, part {part}, {test_path} does not exist")
        else:
            module = import_module(f"solutions.day_{self.day}.part{part}")
            result = module.solve(test_path)
            self.assertEqual(str(result), solution, f"Day {self.day} part 1 failed on {message}")


    def part1Test(self):
        self.__test_builder(1, True)

    def part1Completed(self):
        self.__test_builder(1, False)

    def part2Test(self):
        self.__test_builder(2, True)

    def part2Completed(self):
        self.__test_builder(1, False)


def load_tests(loader, tests, pattern):

    days_with_solutions = 18

    test_suite = unittest.TestSuite()
    for i in range(1, days_with_solutions+1):
        test_suite.addTest(GeneralTestCase('part1Test', i))
        test_suite.addTest(GeneralTestCase('part2Test', i))
        test_suite.addTest(GeneralTestCase('part1Completed', i))
        test_suite.addTest(GeneralTestCase('part2Completed', i))
    return test_suite

def get_solution_record(day: int, part: int, test=False):
    file_prefix = "test" if test else "part"
    record_location = os.path.join(os.path.dirname(__package__), f"data/day_{day}/{file_prefix}{part}_solution.txt")
    with open(record_location) as file:
        try:
            recorded_solution = file.read().strip()
        except FileNotFoundError:
            recorded_solution = None

    return recorded_solution

if __name__ == '__main__':
    unittest.main()