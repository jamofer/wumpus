from dataclasses import dataclass

from wumpus.vector2d import Vector2D


@dataclass
class Entity(object):
    position: Vector2D
