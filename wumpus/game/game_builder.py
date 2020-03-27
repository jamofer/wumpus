import random

from wumpus.direction import Direction
from wumpus.entities.bottomless_pit import BottomlessPit
from wumpus.entities.gold import Gold
from wumpus.entities.wumpus import Wumpus
from wumpus.game.game import Game
from wumpus.entities.hunter import Hunter
from wumpus.vector2d import Vector2D


class GameBuilder(object):
    def __init__(self):
        self.number_of_bottomless_pits = 0
        self.game = Game()

    def with_table(self, x, y):
        self.game.size = [x, y]
        return self

    def with_hunter(self, position=Vector2D(0, 0), direction=Direction.NORTH, arrows=10):
        self.game.set_hunter(Hunter(position, direction, arrows))
        return self

    def with_bottomless_pits(self, quantity):
        self.number_of_bottomless_pits = quantity
        return self

    def build(self):
        self.game.gold = Gold(self._random_empty_table_position())
        self._add_bottomless_pits()
        self.game.wumpus = Wumpus(self._random_empty_table_position())
        return self.game

    def _add_bottomless_pits(self):
        for i in range(self.number_of_bottomless_pits):
            position = self._random_empty_table_position()
            self.game.add_bottomless_pit(BottomlessPit(position))

    def _random_empty_table_position(self):
        if self._is_maximum_number_of_entities_reached():
            raise GameBuilderError('Unable to allocate random empty table position')

        x = random.randint(0, self.game.size[0])
        y = random.randint(0, self.game.size[1])

        position = Vector2D(x, y)

        if self._is_position_already_taken(position):
            return self._random_empty_table_position()

        return position

    def _is_position_already_taken(self, position):
        return any([entity.position == position for entity in self.game.entities])

    def _is_maximum_number_of_entities_reached(self):
        return len(self.game.entities) > self.game.size[0] * self.game.size[1]


def a_game():
    return GameBuilder()


class GameBuilderError(RuntimeError):
    pass
