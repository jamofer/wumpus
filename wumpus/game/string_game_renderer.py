from wumpus.direction import Direction
from wumpus.game.game import GameStatus


DIRECTION_STRING = {
    Direction.NORTH: 'NORTH',
    Direction.EAST: 'EAST',
    Direction.SOUTH: 'SOUTH',
    Direction.WEST: 'WEST',
}

DEAD_BY_PIT = (
    'Hunter: -AAAAAAAAAaaaaaaaaaaaaaaaaaaaaa!!!!!!!!!!!!!!!\n'
    'Narrator: -Poor soul, he felt in the forat. It\'s better gold in hand than a hundred in the pit\n'
    'You lose!\n'
    '\n'
)
KILLED_BY_WUMPUS = (
    'Hunter: -Heyy Wumpus, show me your moves!\n'
    '(CHRUP CHRUP)\n'
    'Wumpus: -Mmmmm... Human meat <3\n'
    'Narrator: -Poor soul, now the legend of the Hunter is inside the Wumpus\'s stomach\n'
    'You lose!\n'
    '\n'
)

WIN_WITHOUT_KILL_WUMPUS = (
    'Wumpus: -Heyy Hunter, show me your moves!\n'
    'Narrator: Hunter takes the gold cowardly and runs to the exit (faster than Speedy Gonzalez).\n'
    'Wumpus: -NOOooOoOoooooo!!! :(\n'
    'You win!\n'
    '\n'
)
WIN_WITH_WUMPUS_DEAD = (
    'Narrator: Toss a coin to your Hunter\n'
    'Narrator: Oh, valley of plenty\n'
    'Narrator: Oh, valley of plenty, oh\n'
    'Narrator: Toss a coin to your Hunter\n'
    'Narrator: ... Nevermind\n'
    'You win!\n'
    '\n'
)


def render(game):
    position = game.player.position
    direction = game.player.direction

    if game.is_over_bottomless_pit:
        return DEAD_BY_PIT

    if game.is_wumpus_alive and game.is_over_wumpus:
        return KILLED_BY_WUMPUS

    if game.status == GameStatus.WIN and game.is_wumpus_alive:
        return WIN_WITHOUT_KILL_WUMPUS

    if game.status == GameStatus.WIN and not game.is_wumpus_alive:
        return WIN_WITH_WUMPUS_DEAD

    position_message = 'You are in the exit position' if game.is_player_at_exit else ''
    gold_message = '1' if game.player_has_gold else '0'
    presence_message = _render_presence_message(game)

    return (
        f'Position [{position.x}, {position.y}]. {position_message}\n'
        f'Direction {DIRECTION_STRING[direction]}\n'
        f'Golds: {gold_message}\n'
        f'Arrows left: {game.player.arrows_left}\n'
        f'Presence: {presence_message}\n'
    )


def _render_presence_message(game):
    presence_message = ''

    if game.is_over_gold:
        presence_message = 'The gold is here!'

    if game.is_over_wumpus_presence:
        presence_message = 'Wumpus stink, you are about to poke'

    if game.is_over_bottomless_pit_presence:
        presence_message = 'A fresh breeze fills you with determination'

    return presence_message


def _format_presences_messages(presences_messages):
    return ''.join(f' * {msg}\n' for msg in presences_messages)
