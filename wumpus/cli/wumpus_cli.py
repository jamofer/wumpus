import cmd
import json

from wumpus.cli import wumpus_cli_command_parser
from wumpus.game import game_service, string_game_renderer
from wumpus.game.game import GameStatus
from wumpus.game.game_options import GameOptions
from wumpus.game.game_service import TurnDirection


def requires_game_started(func):
    def wrapper(self, *args, **kwargs):
        if self.game and self.game.status == GameStatus.PLAYING:
            func(self, *args, **kwargs)
        else:
            print('Game is not running.')
    return wrapper


class WumpusCli(cmd.Cmd):
    prompt = 'Wumpus-CLI$ '
    intro = (
        'Welcome Hunter to Wumpus dungeon,\n'
        'Kill the Wumpus, take the gold and escape! You can ignore him but that\'s for chickens\n'
        'PS: Take care with the bottomless pits :)\n'
        '\n'
        'You can move forward, turn clockwise and anticlockwise.\nIf you think you have in front of '
        'you the Wumpus, take your bow and fire your powerful arrow!\n'
        '\n'
        'Type help or ? to list available commands\n\n'
        'For a new game, type game_start\n'
    )

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.game = None

    def do_exit(self, line):
        'Exit game'
        return True

    def do_quit(self, line):
        'Exit game'
        return True

    def do_EOF(self, line):
        'Exit game'
        return True

    def do_start_game(self, line):
        'Starts new game. Usage: start_game [columns=4] [rows=4] [hunter_arrows=2] [bottomless_pits=4]'
        game_options = GameOptions()

        if line:
            game_options = wumpus_cli_command_parser.parse_game_options(line)

        self.game = game_service.start(game_options)
        print(string_game_renderer.render(self.game))

    @requires_game_started
    def do_turn(self, line):
        'Turn clockwise or anticlockwise, usage: turn [clockwise|anticlockwise]'
        game_service.turn(line, self.game)
        print(string_game_renderer.render(self.game))

    @requires_game_started
    def do_move(self, line):
        'Moves forward one position. take care with your direction. Usage: move'
        game_service.move(self.game)
        print(string_game_renderer.render(self.game))

    @requires_game_started
    def do_fire_arrow(self, line):
        'Fires an arrow until it reaches the Wumpus or a wall. Usage: fire_arrow'
        if self.game.player.arrows_left == 0:
            print('Not enough arrows')
            return

        hit = game_service.fire(self.game)
        print(string_game_renderer.render(self.game))

        if hit:
            print('?: -Aaaaaaaaaaaaaaaaaaaa!!!!!! directly to my heart :(')

    @requires_game_started
    def do_take_the_gold(self, line):
        'Takes the gold if you are in the same position. Usage: take_the_gold'
        game_service.take_gold(self.game)
        print(string_game_renderer.render(self.game))

    @requires_game_started
    def do_leave_the_dungeon(self, line):
        'Leaves the dungeon if you are in the exit position and you have the gold. Usage: leave_the_dungeon'
        game_service.leave_dungeon(self.game)
        print(string_game_renderer.render(self.game))

    def complete_turn(self, text, line, start_index, end_index):
        if not text:
            return [TurnDirection.CLOCKWISE, TurnDirection.ANTICLOCKWISE]

        if TurnDirection.CLOCKWISE.startswith(text.lower()):
            return [TurnDirection.CLOCKWISE]

        if TurnDirection.ANTICLOCKWISE.startswith(text.lower()):
            return [TurnDirection.ANTICLOCKWISE]
