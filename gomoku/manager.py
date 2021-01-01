import numpy as np
import sys

from gomoku.agent.base import BaseAgent, RandomAgent, ConsoleAgent
from gomoku.agent.greedy import GreedyAgent, GreedyDefendingAgent
from gomoku.board import GomokuBoard
from gomoku.util import CsvStream, Side

class GameManager:
    def __init__(self, size: int = 19, quiet: bool = False):
        self.__board = GomokuBoard(size, quiet)
        self.__quiet = quiet

    def get_board(self):
        return self.__board

    def get_agent_class(self, name):
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

    def reset_game(self):
        self.__board.reset()

    def add_piece(self, coord: np.array, side: Side) -> (bool, Side, GomokuBoard):
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

        assert side.is_player()

        if not self.__board.add_piece(coord, side):
            return False, Side.NONE, self.__board

        if self.__board.check_win(coord, side):
            winner = side
            if not self.__quiet:
                print(f'{side} wins!')
        elif self.__board.check_tie():
            winner = Side.TIE
            if not self.__quiet:
                print('game tied!')
        else:
            winner = Side.NONE

        return True, winner, self.__board

    def make_agent_move(self, agent: BaseAgent, side: Side, stream: CsvStream = None) -> bool:
        """
        Have an agent make a move

        Parameters
        ----------
        agent : BaseAgent
            agent to make the move
        side : int
            side of the agent
        stream : CsvStream
            stream to output moves

        Returns
        -------
        game_ended: bool
            whether the game has ended after the move
        """
        while True:
            move = agent.move(self.__board)
            success, winner, board = self.add_piece(move, side)
            if stream:
                stream.add_move(side, move, board.get_board(), winner)
            if success:
                return winner != Side.NONE

    def run_game(self, agent_name1: str, agent_name2: str, output: bool, path: str):
        """
        Run a game between two agents

        Parameters
        ----------
        agent_name1 : str
            name of agent to play black
        agent_name2 : str
            name of agent to play white
        output : bool
            whether to output moves to csv
        path : str
            directory of output csv file
        """
        self.reset_game()

        stream = None
        if output:
            stream = CsvStream(path, self.__board.get_size())

        agent1 = self.get_agent_class(agent_name1)(Side(1))
        agent2 = self.get_agent_class(agent_name2)(Side(2))

        while True:
            if self.make_agent_move(agent1, Side(1), stream):
                break
            if self.make_agent_move(agent2, Side(2), stream):
                break
        if not self.__quiet:
            print('Game done')
