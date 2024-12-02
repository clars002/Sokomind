"""
Contains heuristic functions and related.
"""

import actor as act
from actor import Actor
from state import State


def stuck_memoized(box: Actor, state: State, cache):  # Written by ChatGPT
    """
    Memoization layer for stuck() in order to store actors that have
    already been checked.
    """
    key = (box.x_position, box.y_position)
    if key not in cache:
        cache[key] = False
        cache[key] = stuck(box, state, cache)
    return cache[key]


def stuck(box: Actor, state: State, cache):
    """
    Checks if a box is stuck; returns True if so.
    """

    box_x = box.x_position
    box_y = box.y_position

    adjacent_spaces = [None] * 4

    adjacent_spaces[0] = state.mapped_actors[box_y - 1][box_x]
    adjacent_spaces[1] = state.mapped_actors[box_y][box_x + 1]
    adjacent_spaces[2] = state.mapped_actors[box_y + 1][box_x]
    adjacent_spaces[3] = state.mapped_actors[box_y][box_x - 1]

    # A box is stuck if it is blocked in at least two mutually-adjacent
    # directions by immovable objects (i.e. a wall or another stuck box)
    is_immovable = [False] * 4

    for i in range(4):
        if adjacent_spaces[i] == None:
            is_immovable[i] = False
        elif adjacent_spaces[i].symbol == "O":
            is_immovable[i] = True
        elif act.is_box(adjacent_spaces[i]) and stuck_memoized(
            adjacent_spaces[i], state, cache
        ):
            is_immovable[i] = True
        else:
            is_immovable[i] = False

    # Check for stuck objects in mutually-adjacent directions
    for i in range(3):
        if is_immovable[i] and is_immovable[i + 1]:
            return True
    # Wrap back around since 3 (west) is adjacent to 0 (north)
    if is_immovable[3] and is_immovable[0]:
        return True

    return False


def manhattan_heuristic(state: State):
    """
    Returns the sum of the manhattan distance of each box to its
    (nearest) corresponding storage.
    """
    specific_boxes = state.specific_boxes
    specific_storages = state.specific_storages
    generic_boxes = state.generic_boxes
    generic_storages = state.generic_storages

    total_distances_specific = 0
    for i in range(len(specific_boxes)):
        y_distance = abs(specific_boxes[i].y_position - specific_storages[i].y_position)
        x_distance = abs(specific_boxes[i].x_position - specific_storages[i].x_position)
        distance = y_distance + x_distance
        total_distances_specific += distance
    # Generic storages are more complicated since we must find the
    # nearest generic storage for each box.
    total_distances_generic = 0
    for i in range(len(generic_boxes)):
        smallest_distance = -1
        for j in range(len(generic_storages)):
            y_distance = abs(
                generic_boxes[i].y_position - generic_storages[j].y_position
            )
            x_distance = abs(
                generic_boxes[i].x_position - generic_storages[j].x_position
            )
            sum_distance = y_distance + x_distance
            if smallest_distance == -1 or sum_distance < smallest_distance:
                smallest_distance = sum_distance
        if smallest_distance != -1:
            total_distances_generic += smallest_distance

    score = total_distances_specific + total_distances_generic

    return score


def custom_heuristic(state: State):
    """
    The same as the manhattan heuristic, except that if there is at
    least one stuck box in the state, returns -1.
    """
    specific_boxes = state.specific_boxes
    specific_storages = state.specific_storages
    generic_boxes = state.generic_boxes
    generic_storages = state.generic_storages

    stuck_cache = {}

    total_distances_specific = 0
    for i in range(len(specific_boxes)):
        y_distance = abs(specific_boxes[i].y_position - specific_storages[i].y_position)
        x_distance = abs(specific_boxes[i].x_position - specific_storages[i].x_position)
        distance = y_distance + x_distance
        # If the box is not in its storage, check if it's stuck.
        if distance != 0 and stuck_memoized(specific_boxes[i], state, stuck_cache):
            return -1
        total_distances_specific += distance

    total_distances_generic = 0
    for i in range(len(generic_boxes)):
        smallest_distance = -1
        for j in range(len(generic_storages)):
            y_distance = abs(
                generic_boxes[i].y_position - generic_storages[j].y_position
            )
            x_distance = abs(
                generic_boxes[i].x_position - generic_storages[j].x_position
            )
            sum_distance = y_distance + x_distance
            if smallest_distance == -1 or sum_distance < smallest_distance:
                smallest_distance = sum_distance
        if smallest_distance != -1:
            # If the box is not in its storage, check if it's stuck.
            if smallest_distance != 0 and stuck_memoized(
                generic_boxes[i], state, stuck_cache
            ):
                return -1
            total_distances_generic += smallest_distance

    score = total_distances_specific + total_distances_generic

    return score


def null_heuristic(state: State):
    return 0


class HeuristicFactory:
    """
    Factory to enable runtime polymorphism with respect to Heuristic
    """

    @staticmethod
    def create_heuristic(heuristic: str = None):
        if heuristic is not None:
            heuristic = heuristic.strip().lower()

        if heuristic in ("manhattan", "Manhattan", "man", "trivial"):
            return manhattan_heuristic
        if heuristic in ("custom"):
            return custom_heuristic
        elif heuristic == None or heuristic == "None":
            return null_heuristic
        else:
            raise ValueError(f"Unknown heuristic: {heuristic}")
