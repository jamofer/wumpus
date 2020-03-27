import math

from wumpus.game.game_builder import a_game
from wumpus.vector2d import Vector2D


def start(options):
    return a_game()\
        .with_table(options.columns, options.rows)\
        .with_hunter(arrows=options.hunter_arrows)\
        .with_bottomless_pits(quantity=options.bottomless_pits)\
        .build()


def move(game):
    game.player.position += game.player.direction


class TurnDirection:
    CLOCKWISE = 'clockwise'
    ANTICLOCKWISE = 'anticlockwise'


def turn(turn_direction, game):
    turn_in_radians = _turn_in_radians(turn_direction)

    turn_cos = math.cos(turn_in_radians)
    turn_sin = math.sin(turn_in_radians)

    game.player.direction = Vector2D(
        round(game.player.direction.x * turn_cos - game.player.direction.y * turn_sin),
        round(game.player.direction.x * turn_sin - game.player.direction.y * turn_cos)
    )


def _turn_in_radians(turn_direction):
    if turn_direction == TurnDirection.CLOCKWISE:
        direction_degrees = -90 * math.pi / 180
    else:
        direction_degrees = 90 * math.pi / 180
    return direction_degrees
