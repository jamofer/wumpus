from wumpus.cli.wumpus_cli import WumpusCli


def run():
    wumpus_cli = WumpusCli()
    try:
        wumpus_cli.cmdloop()
    except KeyboardInterrupt:
        pass
    finally:
        print('')


if __name__ == '__main__':
    run()
