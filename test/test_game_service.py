from wumpus.direction import Direction
from wumpus.entities.bottomless_pit import BottomlessPit
from wumpus.game import game_service
from wumpus.game.game import GameStatus
from wumpus.game.game_builder import a_game
from wumpus.game.game_options import GameOptions
from wumpus.game.game_service import TurnDirection
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


def it_does_not_move_the_player_when_it_reaches_a_wall():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.SOUTH).build()

    game_service.move(game)

    assert game.player.position == Vector2D(0, 0)


def it_kills_player_when_it_moves_to_the_bottomless_pit():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.NORTH).build()
    game.add_bottomless_pit(BottomlessPit(Vector2D(0, 1)))

    game_service.move(game)

    assert game.player.position == Vector2D(0, 1)
    assert game.is_over_bottomless_pit
    assert game.status == GameStatus.LOSS


def it_kills_player_when_it_moves_to_the_wumpus_and_it_is_alive():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.NORTH).build()
    game.wumpus.position = Vector2D(0, 1)

    game_service.move(game)

    assert game.player.position == Vector2D(0, 1)
    assert game.is_over_wumpus
    assert game.status == GameStatus.LOSS


def it_does_not_kill_player_when_it_moves_to_the_wumpus_and_it_is_dead():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.NORTH).build()
    game.wumpus.position = Vector2D(0, 1)
    game.wumpus.is_alive = False

    game_service.move(game)

    assert game.player.position == Vector2D(0, 1)
    assert game.is_over_wumpus
    assert game.status == GameStatus.PLAYING


def it_changes_player_direction_clockwise():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.NORTH).build()

    game_service.turn(TurnDirection.CLOCKWISE, game)
    assert game.player.direction == Direction.EAST

    game_service.turn(TurnDirection.CLOCKWISE, game)
    assert game.player.direction == Direction.SOUTH

    game_service.turn(TurnDirection.CLOCKWISE, game)
    assert game.player.direction == Direction.WEST

    game_service.turn(TurnDirection.CLOCKWISE, game)
    assert game.player.direction == Direction.NORTH


def it_changes_player_direction_anticlockwise():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.NORTH).build()

    game_service.turn(TurnDirection.ANTICLOCKWISE, game)
    assert game.player.direction == Direction.WEST

    game_service.turn(TurnDirection.ANTICLOCKWISE, game)
    assert game.player.direction == Direction.SOUTH

    game_service.turn(TurnDirection.ANTICLOCKWISE, game)
    assert game.player.direction == Direction.EAST

    game_service.turn(TurnDirection.ANTICLOCKWISE, game)
    assert game.player.direction == Direction.NORTH


def it_fires_an_arrow():
    game = a_game().with_hunter(arrows=10).build()

    game_service.fire(game)

    assert game.player.arrows_left == 9


def it_kills_the_wumpus_when_player_fires_an_arrow_in_its_direction():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.NORTH).build()
    game.wumpus.position = Vector2D(0, 3)

    fire_hit = game_service.fire(game)

    assert game.is_wumpus_alive is False
    assert fire_hit


def it_stops_hitting_the_wumpus_on_fire_arrow_when_is_already_dead():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.NORTH).build()
    game.wumpus.position = Vector2D(0, 3)
    game.wumpus.is_alive = False

    fire_hit = game_service.fire(game)

    assert game.is_wumpus_alive is False
    assert fire_hit is False


def it_does_not_kill_the_wumpus_when_player_fires_an_arrow_in_other_direction():
    game = a_game().with_hunter(position=Vector2D(0, 0), direction=Direction.SOUTH).build()
    game.wumpus.position = Vector2D(0, 3)

    fire_hit = game_service.fire(game)

    assert game.is_wumpus_alive
    assert fire_hit is False


def it_does_not_fire_an_arrow_when_no_arrows_left():
    game = a_game().with_hunter(arrows=0, position=Vector2D(0, 0), direction=Direction.NORTH).build()
    game.wumpus.position = Vector2D(0, 3)

    fire_hit = game_service.fire(game)

    assert game.wumpus.is_alive
    assert fire_hit is False


def it_takes_the_gold_if_player_is_in_the_same_position():
    game = a_game().with_hunter(position=Vector2D(0, 0)).build()
    game.gold.position = Vector2D(0, 0)

    game_service.take_gold(game)

    assert game.player_has_gold


def it_does_not_take_the_gold_if_player_is_in_different_position():
    game = a_game().with_hunter(position=Vector2D(0, 0)).build()
    game.gold.position = Vector2D(0, 1)

    game_service.take_gold(game)

    assert game.player_has_gold is False


def it_leaves_dungeon_if_player_is_in_the_same_position_as_the_exit_and_carries_the_gold():
    game = a_game().with_hunter(position=Vector2D(0, 0)).build()
    game.player.has_gold = True

    game_service.leave_dungeon(game)

    assert game.player_has_gold
    assert game.status == GameStatus.WIN


def it_does_not_leave_the_dungeon_if_player_is_in_different_position_as_the_exit():
    game = a_game().with_hunter(position=Vector2D(0, 0)).build()
    game.player.has_gold = True
    game.exit = Vector2D(2, 0)

    game_service.leave_dungeon(game)

    assert game.player_has_gold
    assert game.status == GameStatus.PLAYING
