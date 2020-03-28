from wumpus.entities.bottomless_pit import BottomlessPit
from wumpus.game import string_game_renderer
from wumpus.game.game import GameStatus
from wumpus.game.game_builder import a_game
from wumpus.vector2d import Vector2D


def it_returns_a_human_readable_string_telling_the_current_game_situation():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 2)

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == (
        'Position [0, 0]. You are in the exit position\n'
        'Direction NORTH\n'
        'Golds: 0\n'
        'Arrows left: 10\n'
        'Presence: \n'
    )


def it_returns_a_human_readable_string_without_presences_entities_and_exit_position():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 2)
    game.exit = Vector2D(3, 1)

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == (
        'Position [0, 0]. \n'
        'Direction NORTH\n'
        'Golds: 0\n'
        'Arrows left: 10\n'
        'Presence: \n'
    )


def it_returns_a_human_readable_string_with_3_arrows_left():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 2)
    game.player.arrows_left = 3

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == (
        'Position [0, 0]. You are in the exit position\n'
        'Direction NORTH\n'
        'Golds: 0\n'
        'Arrows left: 3\n'
        'Presence: \n'
    )


def it_returns_a_human_readable_string_with_gold_presence():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.gold.position = Vector2D(0, 0)
    game.wumpus.position = Vector2D(3, 2)

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == (
        'Position [0, 0]. You are in the exit position\n'
        'Direction NORTH\n'
        'Golds: 0\n'
        'Arrows left: 10\n'
        'Presence: The gold is here!\n'
    )


def it_returns_a_human_readable_string_with_wumpus_presence():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(0, 1)

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == (
        'Position [0, 0]. You are in the exit position\n'
        'Direction NORTH\n'
        'Golds: 0\n'
        'Arrows left: 10\n'
        'Presence: Wumpus stink, you are about to poke\n'
    )


def it_returns_a_human_readable_string_with_bottomless_pit_presence():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 3)
    game.add_bottomless_pit(BottomlessPit(Vector2D(1, 0)))

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == (
        'Position [0, 0]. You are in the exit position\n'
        'Direction NORTH\n'
        'Golds: 0\n'
        'Arrows left: 10\n'
        'Presence: A fresh breeze fills you with determination\n'
    )


def it_returns_a_human_readable_string_when_player_has_fallen_in_the_bottomless_pit():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(3, 3)
    game.add_bottomless_pit(BottomlessPit(Vector2D(0, 0)))

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == string_game_renderer.DEAD_BY_PIT


def it_returns_a_human_readable_string_when_player_has_been_killed_by_wumpus():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.gold.position = Vector2D(3, 3)
    game.wumpus.position = Vector2D(0, 0)

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == string_game_renderer.KILLED_BY_WUMPUS


def it_returns_a_human_readable_string_when_player_leaves_successfully_the_dungeon_with_the_gold_and_the_wumpus_alive():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.player.has_gold = True
    game.status = GameStatus.WIN

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == string_game_renderer.WIN_WITHOUT_KILL_WUMPUS


def it_returns_a_human_readable_string_when_player_leaves_successfully_the_dungeon_with_the_gold_and_the_wumpus_dead():
    game = a_game().with_table(4, 4).with_hunter().build()
    game.player.has_gold = True
    game.wumpus.is_alive = False
    game.status = GameStatus.WIN

    human_readeable_string = string_game_renderer.render(game)

    assert human_readeable_string == string_game_renderer.WIN_WITH_WUMPUS_DEAD
