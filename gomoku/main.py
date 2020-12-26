import argparse
import numpy as np
import sys

from board import GomokuBoard
from agent.base import BaseAgent, RandomAgent, ConsoleAgent
from agent.greedy import GreedyAgent, GreedyDefendingAgent

class GameManager:
    def __init__(self, size=19):
        self.__board = GomokuBoard(size)

    def get_board(self):
        return self.__board

    def add_piece(self, coord, side):
        """
        Place a piece on the board and check ending criteria

        Parameters
        ----------
        coord : np.array
            coordinate to place the piece
        side : int
            side of the piece

        Returns
        -------
        success: bool
            validity of the move
        winner: int
            winning side if it exists, -1 if tied, 0 otherwise
        board: GomokuBoard
            state of the board after the move
        """

        if not self.__board.add_piece(coord, side):
            return False, 0, self.__board

        if self.__board.check_win(coord, side):
            winner = side
            print(f'{side} wins!')
        elif self.__board.check_tie():
            winner = -1
            print('game tied!')
        else:
            winner = 0

        return True, winner, self.__board

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
                return winner != 0

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
    agent1 = get_agent_class(args.agent1)(1)
    agent2 = get_agent_class(args.agent2)(2)

    while True:
        if make_agent_move(game, agent1, 1):
            break
        if make_agent_move(game, agent2, 2):
            break
    print('Game done')
