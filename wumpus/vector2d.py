from dataclasses import dataclass


@dataclass
class Vector2D(object):
    x: int
    y: int

    def __add__(self, other):
        return Vector2D(
            self.x + other.x,
            self.y + other.y
        )
