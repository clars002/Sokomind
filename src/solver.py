import copy
import os
import string
import sys
import time
from collections import deque

import psutil

import actor as act
import fringe as fr
import heuristics as heur
from actor import Actor
from state import State

directions = {0: "North", 1: "East", 2: "South", 3: "West"}


def shift_state(state: State, direction: int) -> State:
    new_map, new_robot, new_specific_boxes, new_generic_boxes = copy.deepcopy((state.mapped_actors, state.robot, state.specific_boxes, state.generic_boxes))

    new_state = State(
        mapped_actors=new_map,
        robot=new_robot,
        specific_boxes=new_specific_boxes,
        generic_boxes=new_generic_boxes,
        specific_storages=state.specific_storages,
        generic_storages=state.generic_storages,
        parent=state,
        last_move=direction
    )

    robot_y_position = state.robot.y_position
    robot_x_position = state.robot.x_position

    if move_actor(new_state, robot_y_position, robot_x_position, direction):
        return new_state
    
    return None


def move_actor(
    state: State, initial_y_position: int, initial_x_position: int, direction: int
) -> bool:
    x_offset = 0
    y_offset = 0
    if direction == 0:  # 0 => north
        y_offset = -1
    elif direction == 1:  # 1 => east
        x_offset = 1
    elif direction == 2:  # 2 => south
        y_offset = 1
    elif direction == 3:  # 3 => west
        x_offset = -1

    actor = state.mapped_actors[initial_y_position][initial_x_position]

    destination = state.mapped_actors[initial_y_position + y_offset][
        initial_x_position + x_offset
    ]

    if destination != None:
        if destination.symbol == "O" or (act.is_box(actor) and act.is_box(destination)):
            return False
        elif actor.symbol == "R" and act.is_box(destination):
            push_block = move_actor(
                state, destination.y_position, destination.x_position, direction
            )
            if push_block == False:
                return False
            elif push_block == True:
                move_actor(state, initial_y_position, initial_x_position, direction)
                return True

    previously_occupied = actor.standing_on

    if destination is not None and act.is_storage(destination):
        actor.standing_on = destination
    else:
        actor.standing_on = None

    actor.x_position += x_offset
    actor.y_position += y_offset

    state.mapped_actors[initial_y_position + y_offset][
        initial_x_position + x_offset
    ] = actor

    state.mapped_actors[initial_y_position][
        initial_x_position
    ] = previously_occupied  # Todo: Restore standing_on functionality

    return True


def recover_solution_path(solution_state):  # Written by ChatGPT
    path = []
    current_state = solution_state
    while current_state is not None:
        path.append(current_state)
        current_state = current_state.parent
    # Reverse the path to get it from start to solution
    path.reverse()
    return path


def print_solution(solution_path):
    step_count = 0
    print("Solution path:\n---------------------------------")
    for state in solution_path:
        last_direction = None

        if state.last_move != None:
            last_direction = directions[state.last_move]

        print(f"Step {step_count} - ", end="")
        if last_direction != None:
            print(f"Move {last_direction}:")
        else:
            print("")

        print(state)
        step_count += 1
        print("---------------------------------")
    print("Solved! Full solution path above.")


def initialize_puzzle(filepath: string = "puzzles/mini.txt"):
    # https://www.programiz.com/python-programming/examples/read-line-by-line
    with open(filepath) as puzzle:
        map = puzzle.readlines()
        map_rows = [row.strip() for row in map]

    map_height = len(map_rows)
    map_width = len(map_rows[0])

    robot = Actor("R", -1, -1)
    specific_boxes = [None] * 255
    specific_storages = [None] * 255

    generic_boxes = []
    generic_storages = []

    mapped_actors = [[None for column in range(map_width)] for row in range(map_height)]

    for i in range(map_height):
        for j in range(map_width):
            current_tile = map_rows[i][j]
            new_actor = None
            if current_tile != " ":
                new_actor = Actor(current_tile, i, j)
                if current_tile == "R":
                    robot = new_actor
                elif current_tile == "S":
                    generic_storages.append(new_actor)
                elif current_tile == "X":
                    generic_boxes.append(new_actor)
                elif current_tile != "O":
                    if current_tile.isupper():
                        specific_boxes[ord(current_tile)] = new_actor
                    else:
                        specific_storages[ord(current_tile)] = new_actor
            mapped_actors[i][j] = new_actor

    specific_boxes = [actor for actor in specific_boxes if actor is not None]
    specific_storages = [
        receptacle for receptacle in specific_storages if receptacle is not None
    ]

    start_state = State(
        mapped_actors,
        robot,
        specific_boxes,
        generic_boxes,
        specific_storages,
        generic_storages,
    )

    return start_state


def clear_screen():  # By ChatGPT
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Unix/Linux/Mac
    else:
        os.system("clear")


def process_arguments():
    puzzle = "puzzles/tiny.txt"
    algorithm = "BFS"
    heuristic = "Manhattan"
    optimizations = True
    print_interval = 0.2
    sleep_duration = 0

    argument_count = len(sys.argv)

    if argument_count > 1:
        puzzle = sys.argv[1]
    if argument_count > 2:
        algorithm = sys.argv[2]
    if argument_count > 3:
        print_interval = float(sys.argv[3])
    if argument_count > 4:
        sleep_duration = float(sys.argv[4])
    if argument_count > 5:
        heuristic = sys.argv[5]
    if argument_count > 6:
        optimizations = bool(sys.argv[6])

    if algorithm in ("BFS", "DFS"):
        heuristic = None

    return puzzle, algorithm, print_interval, sleep_duration, heuristic, optimizations


def print_update(start_time, process, fringe, current_state, iterations):
    clear_screen()

    elapsed = time.time() - start_time
    memory_usage = process.memory_info().rss
    memory_usage_mb = memory_usage / (1024**2)

    print("Processing state:")
    print(current_state)
    print(f"Heuristic score: {current_state.heuristic_score}")
    print(f"{iterations} states examined")
    print(f"Fringe length: {len(fringe)}")
    print(f"Time elapsed: {elapsed:.4f} seconds")
    print(f"Memory usage: {memory_usage_mb:.2f} MB")


# def fringe_pop(fringe: deque, algorithm: string = "BFS") -> State:
#     if algorithm in ("DFS"):
#         return fringe.pop()
#     else:
#         return fringe.popleft()


def main():
    start_time = time.time()
    process = psutil.Process(os.getpid())  # ChatGPT

    puzzle, algorithm, print_interval, sleep_duration, heuristic, optimizations = (
        process_arguments()
    )

    start_state = initialize_puzzle(puzzle)
    fringe = fr.FringeFactory.create_fringe(algorithm)
    closed_set = set()

    heuristic_function = heur.HeuristicFactory.create_heuristic(heuristic)

    fringe.add(start_state)

    solved = False
    current_state: State = None
    iterations = 0
    print_time = time.time()

    while solved == False and fringe:

        print_now = time.time() - print_time >= print_interval

        current_state = fringe.pop()
        closed_set.add(current_state)

        solved = current_state.is_goal()
        iterations += 1

        if print_now:
            print_time = time.time()
            print_update(start_time, process, fringe, current_state, iterations)

        # generate new states
        for i in range(4):
            new_state = shift_state(current_state, i)
            if new_state != None and new_state not in closed_set:
                new_state.heuristic_score = heuristic_function(new_state)
                closed_set.add(new_state)
                fringe.add(new_state)

        time.sleep(sleep_duration)

    if solved == True:
        print("A solution has been found!\n")
        path = recover_solution_path(current_state)
        print_solution(path)

    elif not fringe:
        print("The fringe has run dry; we seem to be stuck.")

    runtime = time.time() - start_time
    print(f"Total runtime: {runtime:.4f} seconds")


if __name__ == "__main__":
    main()
