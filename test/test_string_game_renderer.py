from wumpus.direction import Direction
from wumpus.entities.bottomless_pit import BottomlessPit
from wumpus.game import string_game_renderer
from wumpus.game.game import GameStatus
from wumpus.game.game_builder import a_game
from wumpus.vector2d import Vector2D


def it_returns_a_human_readable_string_telling_the_current_game_situation():
    game = a_game().with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 2)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    NORTH\n'
        'Golds:       0\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
        ' * You are in the exit position\n'
    )


def it_returns_a_human_readable_string_without_presences():
    game = a_game().with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 2)
    game.exit = Vector2D(3, 1)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    NORTH\n'
        'Golds:       0\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
    )


def it_returns_a_human_readable_string_with_3_arrows_left():
    game = a_game().with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 2)
    game.player.arrows_left = 3

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    NORTH\n'
        'Golds:       0\n'
        'Arrows left: 3\n'
        '---------------------\n'
        'Presences: \n'
        ' * You are in the exit position\n'
    )


def it_returns_a_human_readable_string_with_gold_presence():
    game = a_game().with_hunter().build()
    game.gold.position = Vector2D(0, 0)
    game.wumpus.position = Vector2D(3, 2)
    game.exit = Vector2D(3, 3)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    NORTH\n'
        'Golds:       0\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
        ' * The gold is here!\n'
    )


def it_returns_a_human_readable_string_with_wumpus_presence():
    game = a_game().with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(0, 1)
    game.exit = Vector2D(3, 3)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    NORTH\n'
        'Golds:       0\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
        ' * Wumpus stink, you are about to poke\n'
    )


def it_returns_a_human_readable_string_with_bottomless_pit_presence():
    game = a_game().with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 3)
    game.add_bottomless_pit(BottomlessPit(Vector2D(1, 0)))
    game.exit = Vector2D(3, 3)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    NORTH\n'
        'Golds:       0\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
        ' * A fresh breeze fills you with determination\n'
    )


def it_returns_a_human_readable_string_when_player_has_gold():
    game = a_game().with_hunter().build()
    game.player.has_gold = True
    game.gold = None
    game.status = GameStatus.PLAYING
    game.wumpus.position = Vector2D(3, 3)
    game.exit = Vector2D(3, 3)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    NORTH\n'
        'Golds:       1\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
    )


def it_returns_a_human_readable_string_when_player_has_fallen_in_the_bottomless_pit():
    game = a_game().with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 3)
    game.add_bottomless_pit(BottomlessPit(Vector2D(0, 0)))

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == string_game_renderer.DEAD_BY_PIT


def it_returns_a_human_readable_string_when_player_has_been_killed_by_wumpus():
    game = a_game().with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(0, 0)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == string_game_renderer.KILLED_BY_WUMPUS


def it_returns_a_human_readable_string_when_player_leaves_successfully_the_dungeon_with_the_gold_and_the_wumpus_alive():
    game = a_game().with_hunter().build()
    game.player.has_gold = True
    game.status = GameStatus.WIN

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == string_game_renderer.WIN_WITHOUT_KILL_WUMPUS


def it_returns_a_human_readable_string_when_player_leaves_successfully_the_dungeon_with_the_gold_and_the_wumpus_dead():
    game = a_game().with_hunter().build()
    game.player.has_gold = True
    game.wumpus.is_alive = False
    game.status = GameStatus.WIN

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == string_game_renderer.WIN_WITH_WUMPUS_DEAD


def it_returns_a_human_readable_string_when_player_is_over_a_dead_wumpus():
    game = a_game().with_hunter().build()
    game.wumpus.is_alive = False
    game.wumpus.position = game.player.position
    game.exit = Vector2D(3, 3)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    NORTH\n'
        'Golds:       0\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
        ' * You feel that Cupid is near after watch that arrow in the Wumpus heart\n'
    )


def it_returns_a_human_readable_string_when_player_is_in_front_of_a_wall():
    game = a_game().with_hunter(direction=Direction.SOUTH).build()
    game.exit = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 3)

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    SOUTH\n'
        'Golds:       0\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
        ' * It feels too strong to pass through... could it be a wall?\n'
    )


def it_returns_many_overlapped_presences():
    game = a_game().with_hunter(direction=Direction.SOUTH).build()
    game.wumpus.is_alive = False
    game.gold.position = game.player.position
    game.wumpus.position = game.player.position
    game.add_bottomless_pit(BottomlessPit(Vector2D(1, 0)))

    human_readable_string = string_game_renderer.render(game)

    assert human_readable_string == (
        '---------------------\n'
        'Position:    [0, 0]\n'
        'Direction    SOUTH\n'
        'Golds:       0\n'
        'Arrows left: 10\n'
        '---------------------\n'
        'Presences: \n'
        ' * You are in the exit position\n'
        ' * A fresh breeze fills you with determination\n'
        ' * You feel that Cupid is near after watch that arrow in the Wumpus heart\n'
        ' * It feels too strong to pass through... could it be a wall?\n'
        ' * The gold is here!\n'
    )
