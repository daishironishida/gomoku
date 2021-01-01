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
    parser.add_argument("-r", "--runs", type=int, default=1, help="number of runs")
    parser.add_argument("-o", "--output", action='store_true', help="output moves to csv file")
    parser.add_argument("-p", "--path", default='data/output', help="directory of csv file (only if -o is specified)")
    parser.add_argument("-q", "--quiet", action='store_true', help="quiet mode")
    args = parser.parse_args()

    # sample run
    game = GameManager(size=args.size, quiet=args.quiet)
    for _ in range(args.runs):
        game.run_game(args.agent1, args.agent2, args.output, args.path)
