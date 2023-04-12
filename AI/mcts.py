from chess_node import *

import os
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


if __name__ == '__main__':
    tree = mcts()

    while True:
        clear()
        tree.current.print_board()
        moves = tree.current.get_legal_moves(chess_syntax=True)
        print("\nPossible Moves:",len(moves))
        print("\n{}\n".format(moves))

        esc = input("Press Enter to continue...")
        if esc == '0':
            break

        tree.checkout((52, 36), add_if_not_exists=True)




