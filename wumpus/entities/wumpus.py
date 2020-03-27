from wumpus.entities.entity import Entity


class WumpusStatus:
    ALIVE = 'alive'
    DEAD = 'dead'


class Wumpus(Entity):
    type = 'wumpus'

    status: str = WumpusStatus.ALIVE
