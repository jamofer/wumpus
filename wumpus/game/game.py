from wumpus.direction import Direction
from wumpus.vector2d import Vector2D

DEFAULT_SIZE = [4, 4]


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

    @property
    def is_player_at_exit(self):
        return self.player.position == self.exit

    @property
    def player_has_gold(self):
        return self.player.has_gold

    @property
    def is_player_over_gold(self):
        if self.player_has_gold:
            return False

        return self.player.position == self.gold.position

    @property
    def is_player_over_wumpus_presence(self):
        position = self.wumpus.position
        return self.player.position in _neighbour_positions(position)

    @property
    def is_player_over_bottomless_pit_presence(self):
        neighbour_positions = []

        for bottomless_pit in self.bottomless_pits:
            neighbour_positions.extend(
                _neighbour_positions(bottomless_pit.position)
            )

        return self.player.position in neighbour_positions

    @property
    def is_player_over_bottomless_pit(self):
        return self.player.position in [pit.position for pit in self.bottomless_pits]

    @property
    def is_wumpus_alive(self):
        return self.wumpus.is_alive

    @property
    def is_player_over_wumpus(self):
        return self.player.position == self.wumpus.position

    @property
    def is_player_in_front_of_a_wall(self):
        position_target = self.player.position + self.player.direction
        return not self.is_position_in_game_table(position_target)

    def is_position_in_game_table(self, position):
        return (
                0 <= position.x < self.size[0] and
                0 <= position.y < self.size[1]
        )


def _neighbour_positions(position):
    return [
        position + Direction.NORTH,
        position + Direction.EAST,
        position + Direction.SOUTH,
        position + Direction.WEST,
    ]
