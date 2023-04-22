from chess_node import *

import os
import random
import pickle
from pathlib import Path
import datetime

clear = lambda: os.system('cls')

# find or create directory to save objects through pickle
default_save_dir = Path(os.path.realpath(os.path.dirname(__file__))).absolute().joinpath('model')

class mcts():

    def __new__(cls, import_tree_file=None, *args, **kwargs):
        if import_tree_file is not None:
            with open(import_tree_file, 'rb') as ifile:
                inst = pickle.load(ifile)

                if not isinstance(inst, cls):
                    raise TypeError('Unpickled object is not of type {}'.format(cls))
        
        else:
            inst = super(mcts, cls).__new__(cls, *args, **kwargs)
        return inst
    
    def __init__(self, import_tree_file : str = None, save_dir=None):

        if import_tree_file is not None:
            # __new__() should have already been called
            return 
            
        self.root = ChessNode()
        self.current = self.root
        self.game_path = []
        
        if save_dir is None:
            self.save_dir = default_save_dir
        else:
            self.save_dir = save_dir
        
        if not self.save_dir.exists():
            self.save_dir.mkdir()

    def reset_current(self):
        self.current = self.root
        self.game_path = []

    def checkout(self, chessMove : tuple, add_if_not_exists : bool = False):

        child = self.current.get_child(chessMove)

        if child is None:
            if add_if_not_exists:
                self.current.create_child(chessMove)
                child = self.current.get_child(chessMove)
            else:
                raise Exception("Child from move {} is not defined.".format(chessMove))
        
        self.game_path.append(chessMove)
        self.current = child
    
    def show_game_state(self):
        moves = self.current.get_legal_moves(chess_syntax=True)

        # print current board state
        self.current.print_board()
        print("Last Move:", self.current.get_last_move(chess_syntax=True))
        print("Possible Moves:",len(moves))
        print("\n{}".format(moves))

        return moves
    
    def replay_game(self, game_moves : List[tuple] = None):
        if game_moves is None:
            game_moves = self.game_path[:]

        self.reset_current()
        
        for move in game_moves:
            self.show_game_state()

            # wait before continuing
            ret_input = input("Press enter to continue...")
            clear()
            
            if ret_input == '0':
                break

            if ret_input == '1':
                self.save_tree(tree_name='mcts_tree.obj')
            
            self.checkout(move, add_if_not_exists=False)
        self.show_game_state()

    def make_random_moves(self):
        self.reset_current()
        ret_input = ""

        while True:
            # get current moves
            moves = self.show_game_state()

            # wait before continuing
            ret_input = input("Press enter to continue...")
            clear()

            if ret_input == '1':
                self.save_tree(tree_name='mcts_tree.obj')

            if ret_input == '0':
                break

            # select random move
            chosen_move = random.randint(0, len(moves) - 1)

            self.checkout(moves[chosen_move], add_if_not_exists=True)

    def save_tree(self, tree_name : str = str(datetime.datetime.now()).replace(':', '.') + ".obj"):

        tree_name = str(self.save_dir.joinpath(tree_name))
        with open(tree_name, 'wb+') as ofile:
            pickle.dump(self, ofile)

if __name__ == '__main__':

    replay = False
    load = True

    if replay:
        tree = mcts(import_tree_file='model/mcts_tree.obj')
        tree.replay_game()

    elif load:
        tree = mcts(import_tree_file='model/mcts_tree.obj')
        tree.make_random_moves()
    else:
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




