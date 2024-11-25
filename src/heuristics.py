from state import State


def manhattan_heuristic(state: State):
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


def null_heuristic(state: State):
    return 0


class HeuristicFactory:
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
