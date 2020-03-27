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
    def is_player_at_exit(game):
        return game.player.position == game.exit

    @property
    def player_has_gold(game):
        return game.player.has_gold

    @property
    def is_over_gold(game):
        if game.player_has_gold:
            return False

        return game.player.position == game.gold.position

    @property
    def is_over_wumpus_presence(game):
        position = game.wumpus.position
        return game.player.position in _neighbour_positions(position)

    @property
    def is_over_bottomless_pit_presence(game):
        neighbour_positions = []

        for bottomless_pit in game.bottomless_pits:
            neighbour_positions.extend(
                _neighbour_positions(bottomless_pit.position)
            )

        return game.player.position in neighbour_positions

    @property
    def is_over_bottomless_pit(game):
        return game.player.position in [pit.position for pit in game.bottomless_pits]

    @property
    def is_wumpus_alive(game):
        return game.wumpus.is_alive

    @property
    def is_over_wumpus(game):
        return game.player.position == game.wumpus.position


def _neighbour_positions(position):
    return [
        Vector2D(position.x, position.y + 1),
        Vector2D(position.x + 1, position.y),
        Vector2D(position.x, position.y - 1),
        Vector2D(position.x - 1, position.y),
    ]
