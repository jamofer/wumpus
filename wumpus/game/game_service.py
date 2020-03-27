from wumpus.game.game_builder import a_game


def start(options):
    return a_game()\
        .with_table(options.columns, options.rows)\
        .with_hunter(arrows=options.hunter_arrows)\
        .with_bottomless_pits(quantity=options.bottomless_pits)\
        .build()
