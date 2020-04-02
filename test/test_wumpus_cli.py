import mock
from mock import MagicMock, patch

from wumpus.cli import wumpus_cli_command_parser
from wumpus.game.game import GameStatus
from wumpus.game.game_builder import GameBuilderError
from wumpus.game.game_options import GameOptions
from wumpus.cli.wumpus_cli import WumpusCli, game_action
from wumpus.game.game_service import TurnDirection


class TestWumpusCli(object):
    def setup(self):
        self.cli = WumpusCli()
        self.game = MagicMock()
        self.start = patch('wumpus.game.game_service.start', return_value=self.game).start()
        self.move = patch('wumpus.game.game_service.move').start()
        self.turn = patch('wumpus.game.game_service.turn').start()
        self.fire = patch('wumpus.game.game_service.fire').start()
        self.take_gold = patch('wumpus.game.game_service.take_gold').start()
        self.leave_dungeon = patch('wumpus.game.game_service.leave_dungeon').start()
        self.render = patch('wumpus.game.string_game_renderer.render').start()

    def teardown(self):
        patch.stopall()

    def it_starts_a_new_game_with_default_values(self):
        self.cli.do_start_game('')

        self.start.assert_called_once_with(GameOptions())
        assert self.cli.game == self.game

    def it_starts_a_new_game_with_1_hunter_arrow(self):
        self.cli.do_start_game('hunter_arrows=1')

        self.start.assert_called_once_with(GameOptions(hunter_arrows=1))

    def it_starts_a_new_game_with_2_bottomless_pits(self):
        self.cli.do_start_game('bottomless_pits=2')

        self.start.assert_called_once_with(GameOptions(bottomless_pits=2))

    def it_starts_a_new_game_with_3_bottomless_pits_4_hunter_arrows_in_a_3x5_table(self):
        self.cli.do_start_game('bottomless_pits=2 hunter_arrows=4 columns=3 rows=5')

        self.start.assert_called_once_with(
            GameOptions(bottomless_pits=2, hunter_arrows=4, columns=3, rows=5)
        )

    def it_ignores_extra_spaces_starting_a_new_game_with_custom_options(self):
        self.cli.do_start_game('bottomless_pits=2  hunter_arrows=4   rows=1')

        self.start.assert_called_once_with(
            GameOptions(bottomless_pits=2, hunter_arrows=4, rows=1)
        )

    def it_uses_default_game_options_starting_new_game_when_custom_options_format_is_not_valid(self):
        self.cli.do_start_game('bottomless_p=iaats= 2= afghg ')

        self.start.assert_called_once_with(GameOptions())

    def it_warns_starting_new_game_when_custom_options_does_not_fit_constraints(self):
        self.start.side_effect = GameBuilderError
        self.cli.do_start_game('bottomless_pits=100 columns=0 rows=1')

        self.start.assert_called_once_with(GameOptions(bottomless_pits=100, columns=0, rows=1))
        assert self.cli.game is None

    def it_does_not_perform_a_game_action_if_game_status_is_not_playing(self):
        self.given_game_status(GameStatus.WIN)
        self.cli.do_move('')
        self.move.assert_not_called()

        self.given_game_status(GameStatus.LOSS)
        self.cli.do_turn('clockwise')
        self.turn.assert_not_called()

        self.given_game_not_started()
        self.cli.do_fire_arrow('')
        self.fire.assert_not_called()

        self.cli.do_leave_the_dungeon('')
        self.leave_dungeon.assert_not_called()

        self.cli.do_take_the_gold('')
        self.take_gold.assert_not_called()

    def it_prints_the_game_status_on_start_game(self):
        self.render.return_value = 'Game status rendered'
        self.cli.do_start_game('')

        self.start.assert_called_once_with(GameOptions())
        self.render.assert_called_once_with(self.game)

    def it_prints_the_game_status_on_game_action(self):
        self.render.return_value = 'Game status rendered'
        self.given_game_status(GameStatus.PLAYING)

        self.render.reset_mock()
        self.cli.do_move('')
        self.render.assert_called_once_with(self.game)

        self.render.reset_mock()
        self.cli.do_fire_arrow('')
        self.render.assert_called_once_with(self.game)

        self.render.reset_mock()
        self.cli.do_leave_the_dungeon('')
        self.render.assert_called_once_with(self.game)

        self.render.reset_mock()
        self.cli.do_take_the_gold('')
        self.render.assert_called_once_with(self.game)

        self.render.reset_mock()
        self.cli.do_turn('')
        self.render.assert_called_once_with(self.game)

    def it_not_fires_arrow_when_no_arrows_left(self):
        self.given_game_status(GameStatus.PLAYING)
        self.game.player.arrows_left = 0

        self.cli.do_fire_arrow('')
        self.fire.assert_not_called()

    def it_preserves_docstring_using_game_action_decorator(self):
        @game_action
        def dummy_do_action_function(self, line):
            """doc string"""

        assert dummy_do_action_function.__doc__ == 'doc string'

    def it_autocompletes_turn_command_with_empty_arguments(self):
        result = given_complete_command_text(text='', complete_method=self.cli.complete_turn)

        assert result == wumpus_cli_command_parser.TURN_OPTIONS_ARGUMENTS

    def it_autocompletes_turn_command_when_partial_argument_starts_with_desired_argument(self):
        result = given_complete_command_text(text='clock', complete_method=self.cli.complete_turn)
        assert result == [TurnDirection.CLOCKWISE]

        result = given_complete_command_text(text='an', complete_method=self.cli.complete_turn)
        assert result == [TurnDirection.ANTICLOCKWISE]

    def it_autocompletes_start_game_command_with_empty_arguments(self):
        result = given_complete_command_text(text='', complete_method=self.cli.complete_start_game)

        assert result == wumpus_cli_command_parser.GAME_OPTIONS_ARGUMENTS

    def it_autocompletes_start_game_command_when_partial_argument_starts_with_desired_argument(self):
        result = given_complete_command_text(text='col', complete_method=self.cli.complete_start_game)
        assert result == ['columns=']

        result = given_complete_command_text(text='ro', complete_method=self.cli.complete_start_game)
        assert result == ['rows=']

        result = given_complete_command_text(text='h', complete_method=self.cli.complete_start_game)
        assert result == ['hunter_arrows=']

        result = given_complete_command_text(text='bot', complete_method=self.cli.complete_start_game)
        assert result == ['bottomless_pits=']

    def it_closes_the_game(self):
        assert self.cli.do_exit('')
        assert self.cli.do_quit('')
        assert self.cli.do_EOF('')

    def it_does_nothing_on_empty_cli_line(self):
        self.cli.emptyline()

    def given_game_status(self, status):
        self.cli.do_start_game('')
        self.game.status = status

    def given_game_not_started(self):
        self.cli.game = None


def given_complete_command_text(text, complete_method):
    return complete_method(text, line=mock.ANY, start_index=mock.ANY, end_index=mock.ANY)
