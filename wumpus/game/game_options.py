from dataclasses import dataclass


@dataclass
class GameOptions(object):
    columns: int = 4
    rows: int = 4
    hunter_arrows: int = 2
    bottomless_pits: int = 4
