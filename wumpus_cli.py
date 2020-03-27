import cmd

from wumpus.game.game_service import TurnDirection


class WumpusCli(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'Wumpus-CLI$ '

    def do_exit(self, line):
        return True

    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        return True

    def do_start_game(self, line):
        pass

    def do_turn(self, line):
        pass

    def do_turn(self, line):
        pass

    def complete_turn(self, text, line, start_index, end_index):
        if not text:
            return [TurnDirection.CLOCKWISE, TurnDirection.ANTICLOCKWISE]

        if TurnDirection.CLOCKWISE.startswith(text.lower()):
            return [TurnDirection.CLOCKWISE]

        if TurnDirection.ANTICLOCKWISE.startswith(text.lower()):
            return [TurnDirection.ANTICLOCKWISE]


if __name__ == '__main__':
    wumpus_cli = WumpusCli()
    try:
        wumpus_cli.cmdloop()
    except KeyboardInterrupt:
        pass
    finally:
        print('')
