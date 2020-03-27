from wumpus.entities.entity import Entity


class Wumpus(Entity):
    type = 'wumpus'

    is_alive: bool = True
