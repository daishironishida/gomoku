import argparse
import numpy as np

from gomoku.board import GomokuBoard
from gomoku.manager import GameManager
from gomoku.util import Side

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", type=int, default=7, help="number of rows/columns of the board")
    parser.add_argument("-1", "--agent1", default="console", help="type of agent 1")
    parser.add_argument("-2", "--agent2", default="console", help="type of agent 2")
    args = parser.parse_args()

    # sample run
    game = GameManager(args.size)
    game.run_game(args.agent1, args.agent2)
