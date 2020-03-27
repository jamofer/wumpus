from wumpus.direction import Direction
from wumpus.game import game_service
from wumpus.game.game import GameStatus, GameOptions
from wumpus.game.game_builder import a_game
from wumpus.vector2d import Vector2D


def it_starts_new_game():
    game_options = GameOptions(columns=4, rows=4)

    game = game_service.start(game_options)

    assert game.status == GameStatus.PLAYING
    assert game.size == [4, 4]


def it_moves_the_player_forward_one_position():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.NORTH).build()

    game_service.move(game)

    assert game.player.position == Vector2D(0, 1)
