import heapq
import string
from collections import deque

from state import State


# Used ChatGPT to help me understand how to apply polymorphism
class Fringe:
    def __bool__(self):
        return bool(self.contents)

    def __len__(self):
        return len(self.contents)

    def add(self, node: State):
        raise NotImplementedError

    def pop(self) -> State:
        raise NotImplementedError


class BFSFringe(Fringe):
    def __init__(self):
        self.contents = deque()

    def add(self, node: State):
        self.contents.append(node)

    def pop(self) -> State:
        return self.contents.popleft()


class DFSFringe(Fringe):
    def __init__(self):
        self.contents = deque()

    def add(self, node: State):
        self.contents.append(node)

    def pop(self) -> State:
        return self.contents.pop()


class PriorityFringe(Fringe):
    def __init__(self):
        self.contents = []

    def add(self, node: State):
        heapq.heappush(self.contents, node)

    def pop(self) -> State:
        return heapq.heappop(self.contents)


class FringeFactory:
    @staticmethod
    def create_fringe(algorithm: str = "BFS"):
        if algorithm == "BFS":
            return BFSFringe()
        elif algorithm == "DFS":
            return DFSFringe()
        elif algorithm in ("GBFS", "A*", "astar"):
            return PriorityFringe()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")


# class Fringe:
#     def __init__(self, algorithm: string = "BFS"):
#         self.algorithm = algorithm
#         self.contents = deque()
#         self.type = 0

#         if algorithm in ("GBFS", "A*"):
#             self.type = 1
#             self.contents = []

#     def __bool__(self):
#         return bool(self.contents)

#     def __len__(self):
#         return len(self.contents)

#     def add(self, node: State):
#         if self.type == 0:
#             self.contents.append(node)
#         else:
#             heapq.heappush(self.contents, node)

#     def pop(self) -> State:
#         if self.algorithm == "BFS":
#             return self.contents.popleft()
#         elif self.algorithm == "DFS":
#             return self.contents.pop()
#         else:
#             return heapq.heappop(self.contents)
