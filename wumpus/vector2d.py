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

    def copy(self):
        return Vector2D(self.x, self.y)


@dataclass(frozen=True)
class ConstantVector2D(object):
    x: int
    y: int
