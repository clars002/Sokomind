"""
Defines the Fringe interface and Fringe classes. Uses the factory
design pattern to enable runtime polymorphism
"""

import heapq
import string
from collections import deque

from state import State


# ChatGPT helped me recall the factory paradigm, but I wrote the code.
class Fringe:
    """
    Abstract base class that defines the Fringe interface.
    """

    def __bool__(self):
        return bool(self.contents)

    def __len__(self):
        return len(self.contents)

    def add(self, node: State):
        raise NotImplementedError

    def pop(self) -> State:
        raise NotImplementedError


class BFSFringe(Fringe):
    """
    Fringe for BFS
    """

    def __init__(self):
        self.contents = deque()

    def add(self, node: State):
        self.contents.append(node)

    def pop(self) -> State:
        return self.contents.popleft()


class DFSFringe(Fringe):
    """
    Fringe for DFS
    """

    def __init__(self):
        self.contents = deque()

    def add(self, node: State):
        self.contents.append(node)

    def pop(self) -> State:
        return self.contents.pop()


class PriorityFringe(Fringe):
    """
    Fringe for GBFS or A*
    """

    def __init__(self):
        self.contents = []

    def add(self, node: State):
        heapq.heappush(self.contents, node)

    def pop(self) -> State:
        return heapq.heappop(self.contents)


class FringeFactory:
    """
    Factory to enable runtime polymorphism with respect to Fringe
    """

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
