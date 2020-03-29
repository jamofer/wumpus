from wumpus.vector2d import ConstantVector2D


class Direction:
    NORTH = ConstantVector2D(0, 1)
    EAST = ConstantVector2D(1, 0)
    WEST = ConstantVector2D(-1, 0)
    SOUTH = ConstantVector2D(0, -1)
