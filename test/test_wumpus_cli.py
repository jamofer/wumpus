from mock import MagicMock, patch

from wumpus.game.game import GameStatus
from wumpus.game.game_options import GameOptions
from wumpus.cli.wumpus_cli import WumpusCli


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

    def it_does_not_perform_a_game_action_if_game_status_is_not_playing(self):
        self.cli.do_start_game('')

        self.cli.do_move('')
        self.cli.game.status = GameStatus.WIN
        self.move.assert_not_called()

        self.cli.do_turn('clockwise')
        self.cli.game.status = GameStatus.LOSS
        self.turn.assert_not_called()

        self.cli.game = None
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
        self.render.assert_called_once_with(self.cli.game)

    def it_prints_the_game_status_on_game_action(self):
        self.render.return_value = 'Game status rendered'
        self.cli.do_start_game('')

        self.render.reset_mock()
        self.cli.do_start_game('')
        self.cli.do_move('')
        self.render.assert_called_once_with(self.cli.game)

        self.render.reset_mock()
        self.cli.do_start_game('')
        self.cli.do_fire_arrow('')
        self.render.assert_called_once_with(self.cli.game)

        self.render.reset_mock()
        self.cli.do_start_game('')
        self.cli.do_leave_the_dungeon('')
        self.render.assert_called_once_with(self.cli.game)

        self.render.reset_mock()
        self.cli.do_start_game('')
        self.cli.do_take_the_gold('')
        self.render.assert_called_once_with(self.cli.game)

        self.render.reset_mock()
        self.cli.do_start_game('')
        self.cli.do_turn('')
        self.render.assert_called_once_with(self.cli.game)
