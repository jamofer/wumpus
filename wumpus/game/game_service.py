import math

from wumpus.game.game import GameStatus
from wumpus.game.game_builder import a_game
from wumpus.vector2d import Vector2D


class TurnDirection:
    CLOCKWISE = 'clockwise'
    ANTICLOCKWISE = 'anticlockwise'


def start(options):
    return a_game()\
        .with_table(options.columns, options.rows)\
        .with_hunter(arrows=options.hunter_arrows)\
        .with_bottomless_pits(quantity=options.bottomless_pits)\
        .build()


def move(game):
    position = game.player.position
    direction = game.player.direction

    if _is_position_in_game_table(game, position + direction):
        game.player.position += direction

    if game.is_over_bottomless_pit or (game.is_wumpus_alive and game.is_over_wumpus):
        game.status = GameStatus.LOSS


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


def fire(game):
    if game.player.arrows_left <= 0:
        return False

    game.player.arrows_left -= 1
    arrow_position = game.player.position.copy()

    while _is_position_in_game_table(game, arrow_position):
        arrow_position += game.player.direction
        if game.wumpus.position == arrow_position:
            game.wumpus.is_alive = False
            return True

    return False


def _is_position_in_game_table(game, position):
    return (
        0 <= position.x < game.size[0] and
        0 <= position.y < game.size[1]
    )


def take_gold(game):
    if game.is_over_gold:
        game.player.has_gold = True
        game.gold = None


def leave_dungeon(game):
    if game.is_player_at_exit and game.player_has_gold:
        game.status = GameStatus.WIN
