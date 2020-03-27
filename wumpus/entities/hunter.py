from dataclasses import dataclass

from wumpus.vector2d import Vector2D
from wumpus.entities.entity import Entity


@dataclass
class Hunter(Entity):
    type = 'hunter'

    direction: Vector2D
    arrows_left: int
    has_gold: bool = False
