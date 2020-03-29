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
    '\n'
    'You lose!\n'
)
KILLED_BY_WUMPUS = (
    'Hunter: -Heyy Wumpus, show me your moves!\n'
    '(CHRUP CHRUP)\n'
    'Wumpus: -Mmmmm... Human meat <3\n'
    'Narrator: -Poor soul, now the legend of the Hunter is inside the Wumpus\'s stomach\n'
    '\n'
    'You lose!\n'
)

WIN_WITHOUT_KILL_WUMPUS = (
    'Wumpus: -Heyy Hunter, show me your moves!\n'
    'Narrator: Hunter takes the gold cowardly and runs to the exit (faster than Speedy Gonzalez).\n'
    'Wumpus: -NOOooOoOoooooo!!! :(\n'
    '\n'
    'You win!\n'
)
WIN_WITH_WUMPUS_DEAD = (
    'Narrator: Toss a coin to your Hunter\n'
    'Narrator: Oh, valley of plenty\n'
    'Narrator: Oh, valley of plenty, oh\n'
    'Narrator: Toss a coin to your Hunter\n'
    'Narrator: ... Nevermind\n'
    '\n'
    'You win!\n'
)


def render(game):
    if game.is_player_over_bottomless_pit:
        return DEAD_BY_PIT

    if game.is_wumpus_alive and game.is_player_over_wumpus:
        return KILLED_BY_WUMPUS

    if game.status == GameStatus.WIN and game.is_wumpus_alive:
        return WIN_WITHOUT_KILL_WUMPUS

    if game.status == GameStatus.WIN and not game.is_wumpus_alive:
        return WIN_WITH_WUMPUS_DEAD

    return _render_player_status(game)


def _render_player_status(game):
    position = game.player.position
    direction = game.player.direction

    gold = '1' if game.player_has_gold else '0'
    presence_messages = _render_presence_message(game)

    return (
        '---------------------\n'
        f'Position:    [{position.x}, {position.y}]\n'
        f'Direction    {DIRECTION_STRING[direction]}\n'
        f'Golds:       {gold}\n'
        f'Arrows left: {game.player.arrows_left}\n'
        '---------------------\n'
        f'Presences: \n'
        f'{presence_messages}'
    )


def _render_presence_message(game):
    presence_messages = []

    if game.is_player_at_exit:
        presence_messages.append('You are in the exit position')

    if game.is_player_over_bottomless_pit_presence:
        presence_messages.append('A fresh breeze fills you with determination')

    if game.is_player_over_wumpus_presence:
        presence_messages.append('Wumpus stink, you are about to poke')

    if game.is_player_over_wumpus:
        presence_messages.append(
            'You feel that Cupid is near '
            'after watch that arrow in the Wumpus heart'
        )

    if game.is_player_in_front_of_a_wall:
        presence_messages.append('It feels strong enough to pass through... could it be a wall?')

    if game.is_player_over_gold:
        presence_messages.append('The gold is here!')

    return _format_presences_messages(presence_messages)


def _format_presences_messages(presences_messages):
    return ''.join(f' * {msg}\n' for msg in presences_messages)
