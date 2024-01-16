from dataclasses import dataclass, field
from utils.pathfinder import Compass, Pos, Action, PriorityAction
from collections import deque
import heapq


def valid_next_nodes(latest: Action, limit: Pos, goal: Pos, came_from: dict[Action, Action], total_weights: dict[Action, int], city_block: list[list[int]]):
    # the left/head of the actions deque in path contains the current action
    # however the Path object stores the next intended direction and its weight
    for d in Compass:
        if d.value == 0 or d == latest.direction.flip() or (d == latest.direction and latest.intensity <= 0):
            continue
        new_pos = d.of_pos(latest.pos)
        if not new_pos.in_limit(limit):
            continue
        moves_left = latest.intensity - 1 if d == latest.direction else 2
        possible_action = Action(new_pos, d,  moves_left)
        weight = city_block[new_pos.row][new_pos.col]
        if possible_action in came_from and total_weights[latest] + weight + possible_action.cost(goal) > total_weights[possible_action]:
            continue
        yield PriorityAction(total_weights[latest] + weight, possible_action)


def shortest_path(city_block):
    limit = Pos(len(city_block), len(city_block[0]))
    goal = limit.move(Pos(-1, -1))

    start: PriorityAction = PriorityAction(0, Action(Pos(0, 0), Compass.Stationary, 3))
    paths = [start]
    heapq.heapify(paths)

    came_from = {}
    came_from[start.action] = None
    path_weights = {}
    path_weights[start.action] = 0

    while len(paths) != 0:
        node_to_check = heapq.heappop(paths)
        if node_to_check.action.pos == goal:
            return node_to_check
        for new_node in valid_next_nodes(node_to_check.action, limit, goal, came_from, path_weights, city_block):
            # print(new_node)
            came_from[new_node.action] = node_to_check.action
            path_weights[new_node.action] = new_node.priority
            heapq.heappush(paths, new_node)

                
def solve(filename: str):
    city_block = []
    with open(filename) as file:
        city_block = [list(map(int, (line.strip()))) for line in file]
    result = shortest_path(city_block)
    if result is None:
        raise Exception("unable to find path to goal")
    return result.priority

if __name__ == "__main__":
    solve("test1.txt")
