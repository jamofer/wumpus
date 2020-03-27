FROM python:3.8-slim

COPY . /wumpus-game
WORKDIR /wumpus-game

RUN pip install -U .

ENTRYPOINT [ "/wumpus-game/wumpus_game.py" ]
