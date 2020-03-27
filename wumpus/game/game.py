from dataclasses import dataclass

from wumpus.direction import Direction
from wumpus.entities.hunter import Hunter
from wumpus.vector2d import Vector2D

DEFAULT_SIZE = [4, 4]
DEFAULT_AVAILABLE_ARROWS = 2

@dataclass
class GameOptions(object):
    columns: int = 0
    rows: int = 0
    hunter_arrows: int = 0
    bottomless_pits: int = 0


class GameStatus:
    PLAYING = 'playing'
    WIN = 'win'
    LOSS = 'loss'


class Game(object):
    def __init__(self):
        self.status = GameStatus.PLAYING
        self.player = None
        self.gold = None
        self.wumpus = None
        self.bottomless_pits = []
        self.size = DEFAULT_SIZE
        self.exit = None

    def set_hunter(self, hunter):
        self.player = hunter
        self.exit = hunter.position

    def add_bottomless_pit(self, bottomless_pit):
        self.bottomless_pits.append(bottomless_pit)

    @property
    def entities(self):
        entities = [self.player, self.gold, self.wumpus] + self.bottomless_pits
        return [entity for entity in entities if entity is not None]
