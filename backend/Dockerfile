FROM python:3.7-alpine

COPY . /wumpus-backend
WORKDIR /wumpus-backend

RUN pip install .
CMD ["wumpus-backend", "--bind localhost:3000"]
