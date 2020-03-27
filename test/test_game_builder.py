from pytest import raises

from wumpus.direction import Direction
from wumpus.entities.bottomless_pit import BottomlessPit
from wumpus.game.game import GameStatus
from wumpus.game.game_builder import a_game, GameBuilderError
from wumpus.vector2d import Vector2D


def it_builds_a_game_with_4x4_table():
    game = a_game().with_table(4, 4).build()

    assert game.status == GameStatus.PLAYING
    assert game.size == [4, 4]


def it_builds_a_game_with_10_arrows_for_hunter():
    game = a_game().with_hunter(arrows=10).build()

    expect_quantity_of_arrows_left_for_player_in_game(10, game)


def it_builds_a_game_with_1_bottomless_pit():
    game = a_game().with_bottomless_pits(quantity=1).build()

    expect_quantity_of_bottomless_pits_in_game(1, game)


def it_builds_a_game_with_gold_in_random_position():
    gold_positions = []

    for i in range(100):
        game = a_game().with_table(4000, 4000).build()
        gold_positions.append(game.gold.position)

    assert not all(position == gold_positions[0] for position in gold_positions)


def it_builds_a_game_with_wumpus_in_random_position():
    wumpus_position = []

    for i in range(100):
        game = a_game().with_table(4000, 4000).build()
        wumpus_position.append(game.wumpus.position)

    assert not all(position == wumpus_position[0] for position in wumpus_position)


def it_builds_a_game_with_4x5_table_2_bottomless_pits_and_1_arrow():
    game = a_game()\
        .with_table(4, 5)\
        .with_hunter(arrows=1)\
        .with_bottomless_pits(quantity=2)\
        .build()

    expect_quantity_of_bottomless_pits_in_game(2, game)


def it_builds_a_game_with_hunter_at_position_2x3_and_facing_south():
    game = a_game()\
        .with_hunter(position=Vector2D(2, 3), direction=Direction.SOUTH)\
        .build()

    expect_quantity_of_arrows_left_for_player_in_game(10, game)


def it_builds_a_game_with_bottomless_pits_in_random_positions():
    game = a_game().with_table(200, 200).with_bottomless_pits(quantity=30).build()
    positions = _bottomless_pits_in_game(game)

    other_game = a_game().with_table(200, 200).with_bottomless_pits(quantity=30).build()
    other_positions = _bottomless_pits_in_game(other_game)

    assert positions != other_positions


def it_builds_a_game_with_not_overlapped_entities():
    game = a_game() \
        .with_table(4, 5) \
        .with_hunter(arrows=1) \
        .with_bottomless_pits(quantity=15) \
        .build()

    assert number_of_overlapped_entities_in_game(game) == 0


def it_fails_building_a_game_with_not_overlapped_entities_when_there_is_not_space_left_in_the_table():
    with raises(GameBuilderError):
        a_game().with_table(1, 1).with_bottomless_pits(quantity=15).build()


def expect_quantity_of_arrows_left_for_player_in_game(quantity, game):
    assert game.player.arrows_left == quantity


def expect_quantity_of_bottomless_pits_in_game(quantity, game):
    bottomless_pits = _bottomless_pits_in_game(game)
    assert len(bottomless_pits) == quantity


def number_of_overlapped_entities_in_game(game):
    overlapped_entities = 0
    entities_positions = [entity.position for entity in game.entities]

    for position in entities_positions:
        if entities_positions.count(position) > 1:
            overlapped_entities += 1

    return overlapped_entities


def _bottomless_pits_in_game(game):
    return [entity for entity in game.entities if entity.type == BottomlessPit.type]
