import string


class Actor:
    def __init__(
        self,
        symbol: string = "|",
        y_position: int = -1,
        x_position: int = -1,
        standing_on=None,
    ):
        self.symbol = symbol
        self.y_position = y_position
        self.x_position = x_position
        self.standing_on = standing_on

    def __str__(self):
        return f"Symbol: {self.symbol} - at position ({self.y_position}, {self.x_position})"


def is_box(actor: Actor):
    return actor.symbol.isupper() and actor.symbol not in ("R", "S")


def is_storage(actor: Actor):
    return actor.symbol.islower() or actor.symbol == "S"


# class Storage(Actor):
#     def __init__(self, symbol: string = "_", y_position: int = -2, x_position: int = -2, fulfilled: bool = False):
#         super().__init__(symbol, y_position, x_position)
#         self.fulfilled = fulfilled
