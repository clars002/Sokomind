class State:
    def __init__(
        self,
        mapped_actors,
        robot,
        specific_boxes,
        generic_boxes,
        specific_storages,
        generic_storages,
        parent=None,
        last_move=None,
        heuristic_score=0,
        move_count=0,
    ):
        self.mapped_actors = mapped_actors
        self.robot = robot
        self.specific_boxes = specific_boxes
        self.generic_boxes = generic_boxes
        self.specific_storages = specific_storages
        self.generic_storages = generic_storages
        self.parent = parent
        self.last_move = last_move
        self.heuristic_score = heuristic_score
        self.move_count = move_count

    def __str__(self) -> str:
        output = ""
        for row in self.mapped_actors:
            for col in row:
                if col != None:
                    output += col.symbol
                else:
                    output += " "
            output += "\n"
        output += str(self.robot)
        return output

    def __eq__(self, other):  # Written by ChatGPT
        if not isinstance(other, State):
            return False

        if (
            self.robot.x_position != other.robot.x_position
            or self.robot.y_position != other.robot.y_position
        ):
            return False

        if len(self.specific_boxes) != len(other.specific_boxes):
            return False
        for box, other_box in zip(self.specific_boxes, other.specific_boxes):
            if (
                box.x_position != other_box.x_position
                or box.y_position != other_box.y_position
            ):
                return False

        if len(self.generic_boxes) != len(other.generic_boxes):
            return False
        for box, other_box in zip(self.generic_boxes, other.generic_boxes):
            if (
                box.x_position != other_box.x_position
                or box.y_position != other_box.y_position
            ):
                return False
            
        return True

    def __hash__(self):  # Written by ChatGPT
        return hash(
            (
                self.robot.x_position,
                self.robot.y_position,
                tuple((box.x_position, box.y_position) for box in self.specific_boxes),
                tuple((box.x_position, box.y_position) for box in self.generic_boxes),
            )
        )

    def is_goal(self):
        solved = True
        for i in range(len(self.specific_boxes)):
            box = self.specific_boxes[i]
            storage = self.specific_storages[i]
            if (
                box.x_position != storage.x_position
                or box.y_position != storage.y_position
            ):
                solved = False
                break
        for box in self.generic_boxes:
            stored = False
            for storage in self.generic_storages:
                if (
                    box.x_position == storage.x_position
                    and box.y_position == storage.y_position
                ):
                    stored = True
            if stored == False:
                solved = False
                break

        return solved

    def __lt__(self, other):
        return self.heuristic_score < other.heuristic_score
