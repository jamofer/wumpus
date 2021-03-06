import re

from wumpus.game.game_options import GameOptions
from wumpus.game.game_service import TurnDirection


GAME_OPTIONS_ARGUMENTS = ['columns', 'rows', 'hunter_arrows', 'bottomless_pits']
TURN_OPTIONS_ARGUMENTS = [TurnDirection.CLOCKWISE, TurnDirection.ANTICLOCKWISE]


def parse_game_value_options(command_line):
    keyword_values = _parse_keyword_number_values(command_line)

    game_options_descriptor = {
        k: v for k, v in keyword_values.items()
        if k in GAME_OPTIONS_ARGUMENTS
    }

    return GameOptions(**game_options_descriptor)


def _parse_keyword_number_values(line):
    keyword_values = re.findall(r'(\w+)=(\d+)', line)
    return {keyword: int(value) for keyword, value in keyword_values}
