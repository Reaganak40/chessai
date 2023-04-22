from chess_node import *

import os
import random

clear = lambda: os.system('cls')


class mcts():

    def __init__(self):
        self.root = ChessNode()
        self.current = self.root

    def reset_current(self):
        self.current = self.root

    def checkout(self, chessMove : tuple, add_if_not_exists : bool = False):

        child = self.current.get_child(chessMove)

        if child is None:
            if add_if_not_exists:
                self.current.create_child(chessMove)
                child = self.current.get_child(chessMove)
            else:
                raise Exception("Child from move {} is not defined.".format(chessMove))
        
        self.current = child

    def make_random_moves(self):
        self.reset_current()
        ret_input = ""

        while True:
            # get current moves
            moves = self.current.get_legal_moves(chess_syntax=True)

            # print current board state
            self.current.print_board()
            print("Last Move:", self.current.get_last_move(chess_syntax=True))
            print("Possible Moves:",len(moves))
            print("\n{}".format(moves))

            # wait before continuing
            ret_input = input("Press enter to continue...")
            clear()

            if ret_input == '0':
                break

            # select random move
            chosen_move = random.randint(0, len(moves) - 1)

            self.checkout(moves[chosen_move], add_if_not_exists=True)

if __name__ == '__main__':

    tree = mcts()
    
    tree.make_random_moves()
    quit()

    test_board = ChessNode.get_starting_board()

    node = ChessNode(import_board=test_board)
    node = node.create_child(('e2', 'e3'))
    node = node.create_child(('d7', 'd6'))
    node = node.create_child(('h2', 'h3'))
    node = node.create_child(('c7', 'c5'))
    node = node.create_child(('f1', 'b5'))

    node.print_board()
    moves = node.get_legal_moves(chess_syntax=True)
    print("\nPossible Moves:",len(moves))
    print("\n{}".format(moves))




