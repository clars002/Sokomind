"""
Defines the actor class and related methods.
"""

import string


class Actor:
    def __init__(
        self,
        symbol: string = "|",
        y_position: int = -1,
        x_position: int = -1,
        standing_on=None,
    ):
        # Character (str) representing the actor
        self.symbol = symbol
        # Coordinates
        self.y_position = y_position
        self.x_position = x_position
        # If sharing a space with a storage, log that here
        self.standing_on = standing_on

    def __str__(self):
        return f"Symbol: {self.symbol} - at position ({self.y_position}, {self.x_position})"


def is_box(actor: Actor):
    return actor.symbol.isupper() and actor.symbol not in ("R", "S")


def is_storage(actor: Actor):
    return actor.symbol.islower() or actor.symbol == "S"
