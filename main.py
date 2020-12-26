import argparse
import numpy as np
import sys

from gomoku.agent.base import BaseAgent, RandomAgent, ConsoleAgent
from gomoku.agent.greedy import GreedyAgent, GreedyDefendingAgent
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
    def make_agent_move(game, agent, side):
        board = game.get_board()
        while True:
            move = agent.move(board)
            success, winner, board = game.add_piece(move, side)
            if success:
                return winner != Side.NONE

    def get_agent_class(name):
        if name == "random":
            return RandomAgent
        elif name == "console":
            return ConsoleAgent
        elif name == "greedy":
            return GreedyAgent
        elif name == "greedy_defender":
            return GreedyDefendingAgent
        else:
            print(f'Invalid agent type: {name}')
            sys.exit()

    game = GameManager(args.size)
    agent1 = get_agent_class(args.agent1)(Side(1))
    agent2 = get_agent_class(args.agent2)(Side(2))

    while True:
        if make_agent_move(game, agent1, Side(1)):
            break
        if make_agent_move(game, agent2, Side(2)):
            break
    print('Game done')
