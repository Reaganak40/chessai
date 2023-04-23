
from enum import Enum
from typing import List

from colorama import just_fix_windows_console
from termcolor import colored
import sys

 
class StateEvaluation(Enum):
    """ Contains enumerator class definitions to identify state evaluations
    """

    PLAY = 0
    DRAW = 1
    CHECKMATE = 2
    STALEMATE = 3


class PieceType(Enum):
    """ Contains enumerator class definitions to identify pieces in a chess grid
    """
    E = 0
    WK = 1
    WQ = 2
    WB = 3
    WN = 4
    WR = 5
    WP = 6
    BK = 7
    BQ = 8
    BB = 9
    BN = 10
    BR = 11
    BP = 12

class Turn(Enum):
    """ Contains enumerator class definitions to determine whether it is white or black's turn.
    """
    White = 0
    Black = 1

class ChessNode():
    """ Chess Node containing all chess data for a given configuration
    """

    def __init__(self, import_board : List[int] = None, last_move : tuple = None, state_evaluation : int = StateEvaluation.PLAY.value, last_progress : int = 0):
        self.children : dict[tuple, ChessNode] = {}
        self.move = Turn.White.value
        self.white_can_castle = True
        self.black_can_castle = True

        self.last_move = last_move
        self.state_evaluation = state_evaluation
        self.last_progress = last_progress
        
        if import_board is None:
            self.board = ChessNode.get_starting_board()

            self.black_piece_value = 39
            self.white_piece_value = 39

        else:
            self.board = import_board[:]

            self.black_piece_value = 0
            self.white_piece_value = 0
            
            for piece in self.board:
                if piece == PieceType.WQ.value:
                    self.white_piece_value += 9
                elif piece == PieceType.WR.value:
                    self.white_piece_value += 5
                elif piece == PieceType.WN.value or piece == PieceType.WB.value:
                    self.white_piece_value += 3
                elif piece == PieceType.WP.value:
                    self.white_piece_value += 1
                
                elif piece == PieceType.BQ.value:
                    self.black_piece_value += 9
                elif piece == PieceType.BR.value:
                    self.black_piece_value += 5
                elif piece == PieceType.BN.value or piece == PieceType.BB.value:
                    self.black_piece_value += 3
                elif piece == PieceType.BP.value:
                    self.black_piece_value += 1

    
    def get_starting_board():
        board = [PieceType.E.value] * 64

        # Setup the chess pieces according to a new game
        board[0] = PieceType.BR.value
        board[7] = PieceType.BR.value
        board[1] = PieceType.BN.value
        board[6] = PieceType.BN.value
        board[2] = PieceType.BB.value
        board[5] = PieceType.BB.value
        board[3] = PieceType.BQ.value
        board[4] = PieceType.BK.value

        for index in range(8, 16):
            board[index] = PieceType.BP.value
        for index in range(48, 56):
            board[index] = PieceType.WP.value
        
        board[56] = PieceType.WR.value
        board[63] = PieceType.WR.value
        board[57] = PieceType.WN.value
        board[62] = PieceType.WN.value
        board[58] = PieceType.WB.value
        board[61] = PieceType.WB.value
        board[59] = PieceType.WQ.value
        board[60] = PieceType.WK.value

        return board

    def board_piece_value(self, color : int):

        if color == Turn.White.value:
            return self.white_piece_value
        
        return self.black_piece_value

    def get_state_evaluation(self):
        return self.state_evaluation

    def get_child(self, chessMove : tuple):

        if type(chessMove[0]) is not int:
            chessMove = (self.square_to_board_index(chessMove[0]), self.square_to_board_index(chessMove[1]))

        node = self.children.get(chessMove)

        return node
    
    def create_child(self, chessMove : tuple, make_orphan=False):

        if self.children.get(chessMove) is not None:
            raise Exception("Tried to create child board state but it already exists!")
        
        if type(chessMove[0]) is not int:
            chessMove = (self.square_to_board_index(chessMove[0]), self.square_to_board_index(chessMove[1]))
    
        piece_to_be_taken = self.board[chessMove[1]]
        
        new_board = self.board[:]
        new_board[chessMove[1]] = new_board[chessMove[0]]
        new_board[chessMove[0]] = PieceType.E.value
            
        new_node = ChessNode(import_board=new_board, last_move=chessMove, state_evaluation=self.state_evaluation, last_progress=self.last_progress + 1)
        new_node.move = Turn.Black.value if self.move == Turn.White.value else Turn.White.value
        
        if piece_to_be_taken != PieceType.E.value:
            new_node.last_progress = 0 # reset move draw counter

            if piece_to_be_taken == PieceType.WK.value:
                raise Exception("White King was about to be taken.")
            elif piece_to_be_taken == PieceType.WQ.value:
                new_node.white_piece_value -= 9
            elif piece_to_be_taken == PieceType.WR.value:
                new_node.white_piece_value -= 5
            elif piece_to_be_taken == PieceType.WN.value or piece_to_be_taken == PieceType.WB.value:
                new_node.white_piece_value -= 3
            elif piece_to_be_taken == PieceType.WP.value:
                new_node.white_piece_value -= 1
            
            if piece_to_be_taken == PieceType.BK.value:
                raise Exception("Black King was about to be taken.")
            elif piece_to_be_taken == PieceType.BQ.value:
                new_node.black_piece_value -= 9
            elif piece_to_be_taken == PieceType.BR.value:
                new_node.black_piece_value -= 5
            elif piece_to_be_taken == PieceType.BN.value or piece_to_be_taken == PieceType.BB.value:
                new_node.black_piece_value -= 3
            elif piece_to_be_taken == PieceType.BP.value:
                new_node.black_piece_value -= 1

            if new_node.black_piece_value == 0 and new_node.white_piece_value == 0: # took last takable piece
                new_node.state_evaluation = StateEvaluation.DRAW.value
        
        elif new_node.last_progress >= 50: # 50 moves with no progress
            new_node.state_evaluation = StateEvaluation.DRAW.value
        
        if make_orphan:
            return new_node

        self.children[chessMove] = new_node

        return self.children[chessMove]

    def get_last_move(self, chess_syntax=False):
        if self.last_move is None:
            return None
        
        if chess_syntax:
            return (self.board_index_to_square(self.last_move[0]), self.board_index_to_square(self.last_move[1]))
        
        return self.last_move

    def print_board(self):
        print("______________________")
        for row in range(8):
            print("|", end='')
            for col in range(8):
                piece = self.board[row * 8 + col]
                # no piece
                if piece == PieceType.E.value:
                    piece_str = colored('\u2654', 'black')
                # white piece -- blue
                elif piece == PieceType.WK.value:
                    piece_str = colored("\u2654", 'light_blue')
                elif piece == PieceType.WQ.value:
                    piece_str = colored("\u2655", 'light_blue')
                elif piece == PieceType.WR.value:
                    piece_str = colored("\u2656", 'light_blue')
                elif piece == PieceType.WN.value:
                    piece_str = colored("\u2658", 'light_blue')
                elif piece == PieceType.WB.value:
                    piece_str = colored("\u2657", 'light_blue')
                elif piece == PieceType.WP.value:
                    piece_str = colored("\u2659", 'light_blue')
                
                # black piece -- red
                elif piece == PieceType.BK.value:
                    piece_str = colored("\u2654", 'light_yellow')
                elif piece == PieceType.BQ.value:
                    piece_str = colored("\u2655", 'light_yellow')
                elif piece == PieceType.BR.value:
                    piece_str = colored("\u2656", 'light_yellow')
                elif piece == PieceType.BN.value:
                    piece_str = colored("\u2658", 'light_yellow')
                elif piece == PieceType.BB.value:
                    piece_str = colored("\u2657", 'light_yellow')
                elif piece == PieceType.BP.value:
                    piece_str = colored("\u2659", 'light_yellow')
                
                print(piece_str, end = '|')
            print("")
        for _ in range(22):
            print("\u203E", end='')
        print("")

    def board_index_to_square(self, index : int):
        col = chr(ord('a') + index % 8)
        row = chr(ord('0') + 8 - int((index / 8)))
        return str(col + row)
    
    def square_to_board_index(self, square : str):
        if len(square) != 2:
            err_msg = f'[{square}] must be of str len 2 to be square coordinate.'
            raise Exception(err_msg)
        
        return ((ord('8') - ord(square[1])) * 8) +  (ord(str.lower(square[0])) - ord('a')) 

    def is_same_color(self, piece1 : int, piece2 : int):
        if piece1 <= PieceType.WP.value and piece1 > PieceType.E.value:
            if piece2 <= PieceType.WP.value and piece2 > PieceType.E.value:
                return True
        
        if piece1 <= PieceType.BP.value and piece1 > PieceType.WP.value:
            if piece2 <= PieceType.BP.value and piece2 > PieceType.WP.value:
                return True
        return False

    def get_checks_and_pins(self, king_square, return_check_bool = False):

        pinned_squares = []
        in_check = False
        check_path = []

        valid_king_directions = [True] * 8 # [top-left, top, top-right, left, right, bottom-left, bottom, bottom-right]

        #* check rook and queen attacks

        # check left
        other_square = king_square - 1
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square >= 0 and (other_square % 8) < 7:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(self.board[king_square], self.board[other_square]):
                # if this is the second piece to be added, end path here (no check or pins here)
                if(len(ally_piece) > 0):
                    break
                ally_piece.append(other_square)
            
            # if piece encountered in path is an enemy piece
            elif self.board[other_square] != PieceType.E.value:
                    if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BQ.value or self.board[other_square] == PieceType.BR.value)) or\
                    (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WQ.value or self.board[other_square] == PieceType.WR.value)):
                        if(len(ally_piece) == 1):
                            pinned_squares.append(ally_piece[0])
                        else:
                            if return_check_bool:
                                return True
                            in_check = True                                               # king is in check
                            check_path.extend(piece_path)                                 # add path from enemy piece to king for check block
                            
                            if other_square == king_square - 1:
                                valid_king_directions[4] = False # Make enemy square valid if the king can take it.
                            else:
                                valid_king_directions[3] = valid_king_directions[4] = False   # take away the horizontal plane from available chess moves
                        break
                    else:
                        break

            other_square -= 1 # continue down path
        
        # check right
        other_square = king_square + 1
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square < 64 and (other_square % 8) > 0:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(self.board[king_square], self.board[other_square]):
                # if this is the second piece to be added, end path here (no check or pins here)
                if(len(ally_piece) > 0):
                    break
                ally_piece.append(other_square)
            
            # if piece encountered in path is an enemy piece
            elif self.board[other_square] != PieceType.E.value:
                    if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BQ.value or self.board[other_square] == PieceType.BR.value)) or\
                    (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WQ.value or self.board[other_square] == PieceType.WR.value)):
                        if(len(ally_piece) == 1):
                            pinned_squares.append(ally_piece[0])
                        else:
                            if return_check_bool:
                                return True
                            in_check = True                         # king is in check
                            check_path.extend(piece_path)           # add path from enemy piece to king for check block
                            
                            if other_square == king_square + 1:
                                valid_king_directions[3] = False # Make enemy square valid if the king can take it.
                            else:
                                valid_king_directions[3] = valid_king_directions[4] = False   # take away the horizontal plane from available chess moves
                        break
                    else:
                        break
            
            other_square += 1 # continue down path
        
        # check up
        other_square = king_square - 8
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square >= 0:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(self.board[king_square], self.board[other_square]):
                # if this is the second piece to be added, end path here (no check or pins here)
                if(len(ally_piece) > 0):
                    break
                ally_piece.append(other_square)
            
            # if piece encountered in path is an enemy piece
            elif self.board[other_square] != PieceType.E.value:
                    if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BQ.value or self.board[other_square] == PieceType.BR.value)) or\
                    (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WQ.value or self.board[other_square] == PieceType.WR.value)):
                        if(len(ally_piece) == 1):
                            pinned_squares.append(ally_piece[0])
                        else:
                            if return_check_bool:
                                return True
                            in_check = True                         # king is in check
                            check_path.extend(piece_path)           # add path from enemy piece to king for check block
                            
                            if other_square == king_square - 8:
                                valid_king_directions[6] = False # Make enemy square valid if the king can take it.
                            else:
                                valid_king_directions[1] = valid_king_directions[6] = False   # take away the horizontal plane from available chess moves
                        break
                    else:
                        break
            
            other_square -= 8 # continue down path
        
        # check down
        other_square = king_square + 8
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square < 64:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(self.board[king_square], self.board[other_square]):
                # if this is the second piece to be added, end path here (no check or pins here)
                if(len(ally_piece) > 0):
                    break
                ally_piece.append(other_square)
            
            # if piece encountered in path is an enemy piece
            elif self.board[other_square] != PieceType.E.value:
                    if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BQ.value or self.board[other_square] == PieceType.BR.value)) or\
                    (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WQ.value or self.board[other_square] == PieceType.WR.value)):
                        if(len(ally_piece) == 1):
                            pinned_squares.append(ally_piece[0])
                        else:
                            if return_check_bool:
                                return True
                            in_check = True                         # king is in check
                            check_path.extend(piece_path)           # add path from enemy piece to king for check block
                            
                            if other_square == king_square + 8:
                                valid_king_directions[1] = False # Make enemy square valid if the king can take it.
                            else:
                                valid_king_directions[1] = valid_king_directions[6] = False   # take away the horizontal plane from available chess moves
                        break
                    else:
                        break
            
            other_square += 8 # continue down path
        
        #* check bishop and queen attacks

        # check upper-left
        other_square = king_square - 9
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square >= 0 and (other_square % 8) < 7:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(self.board[king_square], self.board[other_square]):
                # if this is the second piece to be added, end path here (no check or pins here)
                if(len(ally_piece) > 0):
                    break
                ally_piece.append(other_square)
            
            # if piece encountered in path is an enemy piece
            elif self.board[other_square] != PieceType.E.value:
                    if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BQ.value or self.board[other_square] == PieceType.BB.value)) or\
                    (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WQ.value or self.board[other_square] == PieceType.WB.value)):
                        if(len(ally_piece) == 1):
                            pinned_squares.append(ally_piece[0])
                        else:
                            if return_check_bool:
                                return True
                            in_check = True                         # king is in check
                            check_path.extend(piece_path)           # add path from enemy piece to king for check block
                            
                            if other_square == king_square - 9:
                                valid_king_directions[7] = False # Make enemy square valid if the king can take it.
                            else:
                                valid_king_directions[0] = valid_king_directions[7] = False   # take away the horizontal plane from available chess moves
                        break
                    else:
                        break
            
            other_square -= 9 # continue down path
        
        # check upper-right
        other_square = king_square - 7
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square >= 0 and (other_square % 8) > 0:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(self.board[king_square], self.board[other_square]):
                # if this is the second piece to be added, end path here (no check or pins here)
                if(len(ally_piece) > 0):
                    break
                ally_piece.append(other_square)
            
            # if piece encountered in path is an enemy piece
            elif self.board[other_square] != PieceType.E.value:
                    if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BQ.value or self.board[other_square] == PieceType.BB.value)) or\
                    (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WQ.value or self.board[other_square] == PieceType.WB.value)):
                        if(len(ally_piece) == 1):
                            pinned_squares.append(ally_piece[0])
                        else:
                            if return_check_bool:
                                return True
                            in_check = True                         # king is in check
                            check_path.extend(piece_path)           # add path from enemy piece to king for check block
                            
                            if other_square == king_square - 7:
                                valid_king_directions[5] = False # Make enemy square valid if the king can take it.
                            else:
                                valid_king_directions[2] = valid_king_directions[5] = False   # take away the horizontal plane from available chess moves
                        break
                    else:
                        break
            
            other_square -= 7 # continue down path
        
        # check lower-left
        other_square = king_square + 7
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square < 64 and (other_square % 8) < 7:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(self.board[king_square], self.board[other_square]):
                # if this is the second piece to be added, end path here (no check or pins here)
                if(len(ally_piece) > 0):
                    break
                ally_piece.append(other_square)
            
            # if piece encountered in path is an enemy piece
            elif self.board[other_square] != PieceType.E.value:
                    if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BQ.value or self.board[other_square] == PieceType.BB.value)) or\
                    (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WQ.value or self.board[other_square] == PieceType.WB.value)):
                        if(len(ally_piece) == 1):
                            pinned_squares.append(ally_piece[0])
                        else:
                            if return_check_bool:
                                return True
                            in_check = True                         # king is in check
                            check_path.extend(piece_path)           # add path from enemy piece to king for check block
                            
                            if other_square == king_square + 7:
                                valid_king_directions[2] = False # Make enemy square valid if the king can take it.
                            else:
                                valid_king_directions[2] = valid_king_directions[5] = False   # take away the horizontal plane from available chess moves
                        break
                    else:
                        break
            
            other_square += 7 # continue down path
        
        # check lower-right
        other_square = king_square + 9
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square < 64 and (other_square % 8) > 0:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(self.board[king_square], self.board[other_square]):
                # if this is the second piece to be added, end path here (no check or pins here)
                if(len(ally_piece) > 0):
                    break
                ally_piece.append(other_square)
            
            # if piece encountered in path is an enemy piece
            elif self.board[other_square] != PieceType.E.value:
                    if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BQ.value or self.board[other_square] == PieceType.BB.value)) or\
                    (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WQ.value or self.board[other_square] == PieceType.WB.value)):
                        if(len(ally_piece) == 1):
                            pinned_squares.append(ally_piece[0])
                        else:
                            if return_check_bool:
                                return True
                            in_check = True                         # king is in check
                            check_path.extend(piece_path)           # add path from enemy piece to king for check block
                            
                            if other_square == king_square + 9:
                                valid_king_directions[0] = False # Make enemy square valid if the king can take it.
                            else:
                                valid_king_directions[0] = valid_king_directions[7] = False   # take away the horizontal plane from available chess moves
                        break
                    else:
                        break
            
            other_square += 9 # continue down path

        #* check knight attacks

        # 2-up, 1-left
        other_square = king_square - 17
        if other_square >= 0 and (other_square % 8) < 7:
            if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BN.value)) or\
                (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WN.value)):
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
                    

        # 1-up, 2-left
        other_square = king_square - 10
        if other_square >= 0 and (other_square % 8) < 6:
            if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BN.value)) or\
                (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WN.value)):
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
        
        # 1-down, 2-left
        other_square = king_square + 6
        if other_square < 64 and (other_square % 8) < 6:
            if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BN.value)) or\
                (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WN.value)):
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
        
        # 2-down, 1-left
        other_square = king_square + 15
        if other_square < 64 and (other_square % 8) < 7:
           if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BN.value)) or\
                (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WN.value)):
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
        
            
        # 2-up, 1-right
        other_square = king_square - 15
        if other_square >= 0 and (other_square % 8) > 0:
            if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BN.value)) or\
                (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WN.value)):
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
        
        # 1-up, 2-right
        other_square = king_square - 6
        if other_square >= 0 and (other_square % 8) > 1:
            if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BN.value)) or\
                (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WN.value)):
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
        
        # 1-down, 2-right
        other_square = king_square + 10
        if other_square < 64 and (other_square % 8) > 1:
            if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BN.value)) or\
                (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WN.value)):
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
        
        # 2-down, 1-right
        other_square = king_square + 17
        if other_square < 64 and (other_square % 8) > 0:
            if (self.move == Turn.White.value and (self.board[other_square] == PieceType.BN.value)) or\
                (self.move == Turn.Black.value and (self.board[other_square] == PieceType.WN.value)):
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block

        #* check pawn attacks

        if self.move == Turn.White.value and king_square > 15:
            # if white move and white king could potentially be attacked by a black pawn

            if king_square % 8 != 0:
                other_square = king_square - 9
                if self.board[other_square] == PieceType.BP.value:
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
            
            if king_square % 8 != 7:
                other_square = king_square - 7
                if self.board[other_square] == PieceType.BP.value:
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
        
        elif self.move == Turn.Black.value and king_square < 48:
            # if white move and white king could potentially be attacked by a black pawn

            if king_square % 8 != 0:
                other_square = king_square + 7
                if self.board[other_square] == PieceType.WP.value:
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block
            
            if king_square % 8 != 7:
                other_square = king_square + 9
                if self.board[other_square] == PieceType.WP.value:
                    if return_check_bool:
                        return True
                    in_check = True                         # king is in check
                    check_path.extend([other_square])       # add path from enemy piece to king for check block

        
        if return_check_bool:
            return in_check
        
        # restrict king when on edge
        if king_square % 8 == 0:
            valid_king_directions[0] = valid_king_directions[3] = valid_king_directions[5] = False
        
        if king_square % 8 == 0:
            valid_king_directions[2] = valid_king_directions[4] = valid_king_directions[7] = False

        if int(king_square / 8) == 0:
            valid_king_directions[0] = valid_king_directions[1] = valid_king_directions[2] = False
        
        if int(king_square / 8) == 7:
            valid_king_directions[5] = valid_king_directions[6] = valid_king_directions[7] = False


        other_king_val = PieceType.BK.value if self.move == Turn.White.value else PieceType.WK.value
        for index, valid in enumerate(valid_king_directions):

            if(valid):

                if index == 0: #* upper-left from king square
                    other_square = king_square - 9
                    # up
                    if (other_square - 8) >= 0 and self.board[other_square - 8] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # upper-left
                    if (other_square - 9) >= 0 and ((other_square - 9) % 8) < 7 and self.board[other_square - 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # upper-right
                    if (other_square - 7) >= 0 and ((other_square - 7) % 8) > 0 and self.board[other_square - 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # left
                    if (other_square - 1) >= 0 and ((other_square - 1) % 8) < 7 and self.board[other_square - 1] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # lower-left
                    if (other_square + 7) < 64 and ((other_square + 7) % 8) < 7 and self.board[other_square + 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    continue
                if index == 1: #* up from king square
                    other_square = king_square - 8
                    # up
                    if (other_square - 8) >= 0 and self.board[other_square - 8] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # upper-left
                    if (other_square - 9) >= 0 and ((other_square - 9) % 8) < 7 and self.board[other_square - 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # upper-right
                    if (other_square - 7) >= 0 and ((other_square - 7) % 8) > 0 and self.board[other_square - 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    continue
                if index == 2: #* upper-right from king square
                    other_square = king_square - 7
                    # up
                    if (other_square - 8) >= 0 and self.board[other_square - 8] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # upper-left
                    if (other_square - 9) >= 0 and ((other_square - 9) % 8) < 7 and self.board[other_square - 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # upper-right
                    if (other_square - 7) >= 0 and ((other_square - 7) % 8) > 0 and self.board[other_square - 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # right
                    if (other_square + 1) < 64 and ((other_square + 1) % 8) > 0 and self.board[other_square + 1] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # lower-right
                    if (other_square + 9) < 64 and ((other_square + 9) % 8) > 0 and self.board[other_square + 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    continue
                if index == 3: #* left from king square
                    other_square = king_square - 1
                    # upper-left
                    if (other_square - 9) >= 0 and ((other_square - 9) % 8) < 7 and self.board[other_square - 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # left
                    if (other_square - 1) >= 0 and ((other_square - 1) % 8) < 7 and self.board[other_square - 1] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # lower-left
                    if (other_square + 7) < 64 and ((other_square + 7) % 8) < 7 and self.board[other_square + 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    continue
                if index == 4: #* right from king square
                    other_square = king_square + 1
                    # upper-right
                    if (other_square - 7) >= 0 and ((other_square - 7) % 8) > 0 and self.board[other_square - 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # right
                    if (other_square + 1) < 64 and ((other_square + 1) % 8) > 0 and self.board[other_square + 1] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # lower-right
                    if (other_square + 9) < 64 and ((other_square + 9) % 8) > 0 and self.board[other_square + 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    continue
                if index == 5: #* lower-left from king square
                    other_square = king_square + 7
                    # upper-left
                    if (other_square - 9) >= 0 and ((other_square - 9) % 8) < 7 and self.board[other_square - 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # left
                    if (other_square - 1) >= 0 and ((other_square - 1) % 8) < 7 and self.board[other_square - 1] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # lower-left
                    if (other_square + 7) < 64 and ((other_square + 7) % 8) < 7 and self.board[other_square + 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # down
                    if (other_square + 8) < 64 and self.board[other_square + 8] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # lower-right
                    if (other_square + 9) < 64 and ((other_square + 9) % 8) > 0 and self.board[other_square + 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    continue
                if index == 6: #* down from king square
                    other_square = king_square + 8
                    # lower-left
                    if (other_square + 7) < 64 and ((other_square + 7) % 8) < 7 and self.board[other_square + 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # down
                    if (other_square + 8) < 64 and self.board[other_square + 8] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # lower-right
                    if (other_square + 9) < 64 and ((other_square + 9) % 8) > 0 and self.board[other_square + 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    continue
                if index == 7: #* lower-right from king square
                    other_square = king_square + 9
                    # lower-left
                    if (other_square + 7) < 64 and ((other_square + 7) % 8) < 7 and self.board[other_square + 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # down
                    if (other_square + 8) < 64 and self.board[other_square + 8] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # lower-right
                    if (other_square + 9) < 64 and ((other_square + 9) % 8) > 0 and self.board[other_square + 9] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # upper-right
                    if (other_square - 7) >= 0 and ((other_square - 7) % 8) > 0 and self.board[other_square - 7] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    # right
                    if (other_square + 1) < 64 and ((other_square + 1) % 8) > 0 and self.board[other_square + 1] == other_king_val:
                        valid_king_directions[index] = False
                        continue
                    continue

        return in_check, check_path, pinned_squares, valid_king_directions
        
    def get_king_moves(self):
        king_moves = []

        king_square = -1
        for index, piece in enumerate(self.board):
            if self.move == Turn.White.value:
                if piece == PieceType.WK.value:
                    king_square = index
                    break
            elif self.move == Turn.Black.value:
                if piece == PieceType.BK.value:
                    king_square = index
                    break
            else:
                raise Exception(self.move, "does not correlate with black or white's turn.")
        
        if king_square == -1:
            err_msg = "King for {} not found on board.".format('white' if self.move == Turn.White.value else 'black')
            raise Exception(err_msg)

        in_check, check_path, pinned_squares, valid_king_directions = self.get_checks_and_pins(king_square)
        double_check = False

        if in_check:
            piece_found = False
            # check double check
            for board_index in check_path:
                if self.board[board_index] != PieceType.E.value:

                    if piece_found:
                        double_check = True
                        break
                    piece_found = True
        
        for index, safe in enumerate(valid_king_directions):
            
            # if moving to that square does not run into checks, add it to the king move options
            if(safe):
                
                # upper-left
                other_square = king_square - 9
                if index == 0 and (other_square >= 0 and (other_square % 8) < 7) and not self.is_same_color(self.board[king_square], self.board[other_square]):
                    saved_piece = self.board[other_square]
                    self.board[other_square] = self.board[king_square]
                    self.board[king_square] = PieceType.E.value
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                    self.board[king_square] = self.board[other_square]
                    self.board[other_square] = saved_piece
                    continue
                
                # up
                other_square = king_square - 8
                if index == 1 and (other_square >= 0) and not self.is_same_color(self.board[king_square], self.board[other_square]):
                    saved_piece = self.board[other_square]
                    self.board[other_square] = self.board[king_square]
                    self.board[king_square] = PieceType.E.value
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                    self.board[king_square] = self.board[other_square]
                    self.board[other_square] = saved_piece
                    continue
                
                # upper-right
                other_square = king_square - 7
                if index == 2 and (other_square >= 0 and (other_square % 8) > 0) and not self.is_same_color(self.board[king_square], self.board[other_square]):
                    saved_piece = self.board[other_square]
                    self.board[other_square] = self.board[king_square]
                    self.board[king_square] = PieceType.E.value
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                    self.board[king_square] = self.board[other_square]
                    self.board[other_square] = saved_piece
                    continue
                
                # left
                other_square = king_square - 1
                if index == 3 and (other_square >= 0 and (other_square % 8) < 7) and not self.is_same_color(self.board[king_square], self.board[other_square]):
                    saved_piece = self.board[other_square]
                    self.board[other_square] = self.board[king_square]
                    self.board[king_square] = PieceType.E.value
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                    self.board[king_square] = self.board[other_square]
                    self.board[other_square] = saved_piece
                    continue
                
                # right
                other_square = king_square + 1
                if index == 4 and (other_square < 64 and (other_square % 8) > 0) and not self.is_same_color(self.board[king_square], self.board[other_square]):
                    saved_piece = self.board[other_square]
                    self.board[other_square] = self.board[king_square]
                    self.board[king_square] = PieceType.E.value
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                    self.board[king_square] = self.board[other_square]
                    self.board[other_square] = saved_piece
                    continue
                
                # lower-left
                other_square = king_square + 7
                if index == 5 and (other_square < 64 and (other_square % 8) < 7) and not self.is_same_color(self.board[king_square], self.board[other_square]):
                    saved_piece = self.board[other_square]
                    self.board[other_square] = self.board[king_square]
                    self.board[king_square] = PieceType.E.value
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                    self.board[king_square] = self.board[other_square]
                    self.board[other_square] = saved_piece
                    continue
                
                # bottom
                other_square = king_square + 8
                if index == 6 and (other_square < 64) and not self.is_same_color(self.board[king_square], self.board[other_square]):
                    saved_piece = self.board[other_square]
                    self.board[other_square] = self.board[king_square]
                    self.board[king_square] = PieceType.E.value
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                    self.board[king_square] = self.board[other_square]
                    self.board[other_square] = saved_piece
                    continue

                # lower-right
                other_square = king_square + 9
                if index == 7 and (other_square < 64 and (other_square % 8) > 0) and not self.is_same_color(self.board[king_square], self.board[other_square]):
                    saved_piece = self.board[other_square]
                    self.board[other_square] = self.board[king_square]
                    self.board[king_square] = PieceType.E.value
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                    self.board[king_square] = self.board[other_square]
                    self.board[other_square] = saved_piece
                    continue
            
        return king_moves, in_check, double_check, check_path, pinned_squares

    def check_axis_vertical_horizontal(self, move_list : List, current_square : int, piece : int, check_path : List[int]):
        # check left
        other_square = current_square - 1
        while other_square >= 0 and (other_square % 8) < 7:
            if self.is_same_color(piece, self.board[other_square]):
                break
            if len(check_path) > 0 and other_square not in check_path:
                other_square -= 1
                continue
            
            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square -= 1
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break
        
        # check right
        other_square = current_square + 1
        while other_square < 64 and (other_square % 8) > 0:
            if self.is_same_color(piece, self.board[other_square]):
                break
            if len(check_path) > 0 and other_square not in check_path:
                other_square += 1
                continue

            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square += 1
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break
        
        # check up
        other_square = current_square - 8
        while other_square >= 0:
            if self.is_same_color(piece, self.board[other_square]):
                break
            if len(check_path) > 0 and other_square not in check_path:
                other_square -= 8
                continue
            
            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square -= 8
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break
        
        # check down
        other_square = current_square + 8
        while other_square < 64:
            if self.is_same_color(piece, self.board[other_square]):
                break
            if len(check_path) > 0 and other_square not in check_path:
                other_square += 8
                continue
            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square += 8
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break

    def check_axis_diagonal(self,  move_list : List, current_square : int, piece : int, check_path : List[int]):
        # check upper-left
        other_square = current_square - 9
        while other_square >= 0 and (other_square % 8) < 7:
            if self.is_same_color(piece, self.board[other_square]):
                break
            if len(check_path) > 0 and other_square not in check_path:
                other_square -= 9
                continue

            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square -= 9
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break
        
        # check upper-right
        other_square = current_square - 7
        while other_square >= 0 and (other_square % 8) > 0:
            if self.is_same_color(piece, self.board[other_square]):
                break
            if len(check_path) > 0 and other_square not in check_path:
                other_square -= 7
                continue

            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square -= 7
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break
        
        # check lower-left
        other_square = current_square + 7
        while other_square < 64 and (other_square % 8) < 7:
            if self.is_same_color(piece, self.board[other_square]):
                break
            if len(check_path) > 0 and other_square not in check_path:
                other_square += 7
                continue

            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square += 7
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break
        
        # check lower-right
        other_square = current_square + 9
        while other_square < 64 and (other_square % 8) > 0:
            if self.is_same_color(piece, self.board[other_square]):
                break
            if len(check_path) > 0 and other_square not in check_path:
                other_square += 9
                continue

            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square += 9
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break

    def check_knight_moves(self,  move_list : List, current_square : int, piece : int, check_path : List[int]):
        # 2-up, 1-left
        other_square = current_square - 17
        if other_square >= 0 and (other_square % 8) < 7:
            if len(check_path) == 0 or other_square in check_path:
                if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                    move_list.append((current_square, other_square))

        # 1-up, 2-left
        other_square = current_square - 10
        if other_square >= 0 and (other_square % 8) < 6:
            if len(check_path) == 0 or other_square in check_path:
                if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                    move_list.append((current_square, other_square))
        
        # 1-down, 2-left
        other_square = current_square + 6
        if other_square < 64 and (other_square % 8) < 6:
            if len(check_path) == 0 or other_square in check_path:
                if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                    move_list.append((current_square, other_square))
            
        # 2-down, 1-left
        other_square = current_square + 15
        if other_square < 64 and (other_square % 8) < 7:
            if len(check_path) == 0 or other_square in check_path:
                if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                    move_list.append((current_square, other_square))
            
        # 2-up, 1-right
        other_square = current_square - 15
        if other_square >= 0 and (other_square % 8) > 0:
            if len(check_path) == 0 or other_square in check_path:
                if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                    move_list.append((current_square, other_square))
            
        # 1-up, 2-right
        other_square = current_square - 6
        if other_square >= 0 and (other_square % 8) > 1:
            if len(check_path) == 0 or other_square in check_path:
                if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                    move_list.append((current_square, other_square))

        # 1-down, 2-right
        other_square = current_square + 10
        if other_square < 64 and (other_square % 8) > 1:
            if len(check_path) == 0 or other_square in check_path:
                if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                    move_list.append((current_square, other_square))
            
        # 2-down, 1-right
        other_square = current_square + 17
        if other_square < 64 and (other_square % 8) > 0:
            if len(check_path) == 0 or other_square in check_path:
                if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                    move_list.append((current_square, other_square))
        
    def check_pawn_moves(self,  move_list : List, current_square : int, piece : int, check_path : List[int]):
        
        # check if black pawn
        if piece == PieceType.BP.value:
            if int(current_square / 8) == 1:
                # black pawn can make two forward moves (first move)
                if self.board[current_square + 8] == PieceType.E.value:
                    if len(check_path) == 0 or (current_square + 8 in check_path):
                        move_list.append((current_square, current_square + 8))
                    
                    if self.board[current_square + 16] == PieceType.E.value:
                        if len(check_path) == 0 or (current_square + 16 in check_path):
                            move_list.append((current_square, current_square + 16))
            else:
                # black pawn can only move forward one square
                if self.board[current_square + 8] == PieceType.E.value:
                    if len(check_path) == 0 or (current_square + 8 in check_path):
                        move_list.append((current_square, current_square + 8))

            # check if can take at diagonal
            if current_square % 8 > 0 and self.board[current_square + 7] != PieceType.E.value and not self.is_same_color(piece, self.board[current_square + 7]):
                if len(check_path) == 0 or (current_square + 7 in check_path):
                    move_list.append((current_square, current_square + 7))
            
            if current_square % 8 < 7 and self.board[current_square + 9] != PieceType.E.value and not self.is_same_color(piece, self.board[current_square + 9]):
                if len(check_path) == 0 or (current_square + 9 in check_path):
                    move_list.append((current_square, current_square + 9))

        # check if white pawn
        elif piece == PieceType.WP.value:
            if int(current_square / 8) == 6:
                # black pawn can make two forward moves (first move)
                if self.board[current_square - 8] == PieceType.E.value:
                    if len(check_path) == 0 or (current_square - 8 in check_path):
                        move_list.append((current_square, current_square - 8))
                    
                    if self.board[current_square - 16] == PieceType.E.value:
                        if len(check_path) == 0 or (current_square - 16 in check_path):
                            move_list.append((current_square, current_square - 16))
            else:
                # black pawn can only move forward one square
                if self.board[current_square - 8] == PieceType.E.value:
                    if len(check_path) == 0 or (current_square - 8 in check_path):
                        move_list.append((current_square, current_square - 8))

            # check if can take at diagonal
            if current_square % 8 < 7 and self.board[current_square - 7] != PieceType.E.value and not self.is_same_color(piece, self.board[current_square - 7]):
                if len(check_path) == 0 or (current_square - 7 in check_path):
                    move_list.append((current_square, current_square - 7))
            
            if current_square % 8 > 0 and self.board[current_square - 9] != PieceType.E.value and not self.is_same_color(piece, self.board[current_square - 9]):
                if len(check_path) == 0 or (current_square - 9 in check_path):
                    move_list.append((current_square, current_square - 9))

    def get_legal_moves(self, current_move=None, chess_syntax=False):

        if self.state_evaluation != StateEvaluation.PLAY.value:
            return []
        
        if current_move is None:
            current_move = self.move
        
        legal_moves, in_check, double_check, check_path, pinned_squares = self.get_king_moves()

        # if double check, only king moves
        if double_check:
            if chess_syntax:
                return [(self.board_index_to_square(x), self.board_index_to_square(y)) for x, y in legal_moves]
            return legal_moves
        
        # check the rest of the pieces
        for current_square, piece in enumerate(self.board):
            
            if current_square in pinned_squares:
                continue

            # White to Move
            if current_move == Turn.White.value:

                #* CURRENT PIECE: ROOK
                if piece == PieceType.WR.value:
                    self.check_axis_vertical_horizontal(legal_moves, current_square, piece, check_path)
                
                #* CURRENT PIECE: BISHOP
                if piece == PieceType.WB.value:
                    self.check_axis_diagonal(legal_moves, current_square, piece, check_path)
                
                #* CURRENT PIECE: QUEEN
                if piece == PieceType.WQ.value:
                    self.check_axis_vertical_horizontal(legal_moves, current_square, piece, check_path)
                    self.check_axis_diagonal(legal_moves, current_square, piece, check_path)
                
                #* CURRENT PIECE: KNIGHT
                if piece == PieceType.WN.value:
                    self.check_knight_moves(legal_moves, current_square, piece, check_path)
                
                #* CURRENT PIECE: PAWN
                if piece == PieceType.WP.value:
                    self.check_pawn_moves(legal_moves, current_square, piece, check_path)
            # Black to Move
            elif current_move == Turn.Black.value:
                #* CURRENT PIECE: ROOK
                if piece == PieceType.BR.value:
                    self.check_axis_vertical_horizontal(legal_moves, current_square, piece, check_path)
                
                #* CURRENT PIECE: BISHOP
                if piece == PieceType.BB.value:
                    self.check_axis_diagonal(legal_moves, current_square, piece, check_path)
                
                #* CURRENT PIECE: QUEEN
                if piece == PieceType.BQ.value:
                    self.check_axis_vertical_horizontal(legal_moves, current_square, piece, check_path)
                    self.check_axis_diagonal(legal_moves, current_square, piece, check_path)
                
                #* CURRENT PIECE: KNIGHT
                if piece == PieceType.BN.value:
                    self.check_knight_moves(legal_moves, current_square, piece, check_path)
                
                #* CURRENT PIECE: PAWN
                if piece == PieceType.BP.value:
                    self.check_pawn_moves(legal_moves, current_square, piece, check_path)

        if len(legal_moves) == 0:
            if in_check:
                self.state_evaluation = StateEvaluation.CHECKMATE.value
            else:
                self.state_evaluation = StateEvaluation.STALEMATE.value

        if chess_syntax:
            return [(self.board_index_to_square(x), self.board_index_to_square(y)) for x, y in legal_moves]

        return legal_moves
