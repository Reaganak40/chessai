from chess_node import *
from naive_bot import NaiveBot

import os
import sys
import random
import pickle
from pathlib import Path
import datetime
import traceback
import math

clear = lambda: os.system('cls')

recursion_limit = 10000
sys.setrecursionlimit(recursion_limit)


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

        print("Number of Moves:", len(game_moves))

        self.reset_current()
        ret_input = ""
        #first_time = False

        for move in game_moves:

            # if self.current.get_last_move(chess_syntax=True) != ('h3', 'd7') and not first_time:
            #     self.checkout(move, add_if_not_exists=False)
            #     continue
            # else:
            #     first_time = True
                

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

    def monte_carlo_tree_search(self, new_game=True):
        if new_game:
            self.reset_current()
        
        policy = NaiveBot.suggest_move_from_options
        
        # * Step 1. Selection
        # traverse down using UCT (and policy for tie-breakers) until leaf node found
        while len(self.current.children.keys()) > 0:
            moves, state = self.define_state()

            potential_moves = []
            max_move_score = 0
            
            # check all current node's possible next states
            for move in moves:
                child = self.current.children.get(move)
                if child is None:
                    # there are move(s) that have not been checked (infinite potential)    
                    if max_move_score < float('inf'):
                        max_move_score = float('inf')
                        potential_moves = []
                    potential_moves.append(move)
                else:
                    
                    # stands for the number of simulations for the node considered after the i-th move
                    n_i = sum(child.stats)
                    
                    # the win rate of the child state for whoever turn it is
                    win_rate = child.stats[0] if child.move == Turn.White.value else child.stats[1]
                    win_rate += child.stats[2] / 2 # add half points for draws
                    win_rate /= n_i
                    
                    # stands for the total number of simulations after the i-th move run by the parent node of the one considered
                    N_i = sum(self.current.stats)
                    
                    # Upper Confidence Bound 1 equation
                    move_score = win_rate + (math.sqrt(2) * math.sqrt(math.log(N_i) / n_i))
                    
                    if move_score > max_move_score:
                        max_move_score = move_score
                        potential_moves = [move]
                    elif move_score == max_move_score:
                        potential_moves.append(move)
                
                if len(potential_moves) > 1:
                    suggested_move = policy(self.current, potential_moves)
                else:
                    suggested_move = potential_moves[0]
                
            self.checkout(suggested_move, add_if_not_exists=True)
            
        #* Step 2. Expansion
        moves, state = self.define_state()

        # use policy to expand
        suggested_move = policy(self.current, moves)

        self.checkout(suggested_move, add_if_not_exists=True)
        new_leaf_node = self.current

        #* Step 3. Simulation

        # simulate to terminal state using policy
        while True:
            moves, state = self.define_state()

            if state != StateEvaluation.PLAY.value:
                break

            try:
                suggested_move = NaiveBot.suggest_move_from_options(self.current, moves, random_move_odds=4)
            except Exception:
                self.save_tree(tree_name='mcts_tree.obj')
                print("Failure to suggest with Naive Bot")
                traceback.print_exc()
                quit()
            
            try:
                self.checkout(suggested_move, add_if_not_exists=True)
            except Exception:
                self.save_tree(tree_name='mcts_tree.obj')
                print("Failure to Create Child")
                traceback.print_exc()
                quit()
        
        #* Step 4. Backpropagation
        # win-loss-tie stats are updated automatically when a termination state is detected
        # cut off random simulation from tree
        new_leaf_node.children = {}
        
        # save updated mcts model
        self.save_tree(tree_name='mcts_tree.obj')



    def naive_bot_game(self, new_game=True):
        if new_game:
            self.reset_current()
        
        while True:
            
            moves, state = self.define_state()

            if state != StateEvaluation.PLAY.value:
                break

            try:
                suggested_move = NaiveBot.suggest_move_from_options(self.current, moves, random_move_odds=4)
            except Exception:
                self.save_tree(tree_name='mcts_tree.obj')
                print("Failure to suggest with Naive Bot")
                traceback.print_exc()
                quit()
            
            try:
                self.checkout(suggested_move, add_if_not_exists=True)
            except Exception:
                self.save_tree(tree_name='mcts_tree.obj')
                print("Failure to Create Child")
                traceback.print_exc()
                quit()

    
    def make_random_moves(self, new_game=True):
        if new_game:
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

    
    def define_state(self, save_on_termination_state=False):
        
        try:
            moves = self.current.get_legal_moves() # gets moves and updates state evaluation
        except Exception:
                self.save_tree(tree_name='mcts_tree.obj')
                print("Failure to get move list")
                traceback.print_exc()
                quit()
        
        node_evaluation = self.current.get_state_evaluation()

        if node_evaluation != StateEvaluation.PLAY.value:
            print("Termination state reached:", node_evaluation)
            print("Number of Moves:", len(self.game_path))
            print("Root states:", self.root.stats)

            if save_on_termination_state:
                self.save_tree(tree_name='mcts_tree.obj')
        
        return moves, node_evaluation


if __name__ == '__main__':

    replay = False
    load = True

    if replay:
        tree = mcts(import_tree_file='model/mcts_tree.obj')
        tree.replay_game()

    elif load:

        tree = mcts(import_tree_file='model/mcts_tree.obj')

        print(len(tree.root.children.keys()))
        for key, value in tree.root.children.items():
            print("{}: {}  --> Explored {} times".format(key, value.stats, sum(value.stats)))

        # node = tree.root.children[(51, 43)]
        # print(len(node.children.keys()))
        # for key, value in node.children.items():
        #     print("{}: {}".format(key, value.stats))

        
        # node = node.children[(50, 42)]
        # print(len(node.children.keys()))
        # for key, value in node.children.items():
        #     print("{}: {}".format(key, value.stats))

        # node = node.children[(11, 27)]
        # print(len(node.children.keys()))
        # for key, value in node.children.items():
        #     print("{}: {}".format(key, value.stats))

        quit()
        for _ in range(1000):
            tree.monte_carlo_tree_search(new_game=True)
    else:
        tree = mcts()
        for _ in range(100):
            tree.monte_carlo_tree_search(new_game=True)
    quit()

    test_board = [PieceType.E.value] * 64
    test_board[56] = PieceType.WK.value
    test_board[16] = PieceType.BK.value
    test_board[49] = PieceType.BP.value

    node = ChessNode(import_board=test_board)

    node.print_board()
    moves = node.get_legal_moves(chess_syntax=True)
    print("\nPossible Moves:",len(moves))
    print("\n{}".format(moves))




