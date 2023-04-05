
from enum import Enum
from typing import List
 
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

    def __init__(self, import_board : List[int] = None):
        self.move = Turn.White.value
        self.white_can_castle = True
        self.black_can_castle = True
        
        if import_board is None:
            self.board = [PieceType.E.value] * 64

            # Setup the chess pieces according to a new game
            self.board[0] = PieceType.BR.value
            self.board[7] = PieceType.BR.value
            self.board[1] = PieceType.BN.value
            self.board[6] = PieceType.BN.value
            self.board[2] = PieceType.BB.value
            self.board[5] = PieceType.BB.value
            self.board[3] = PieceType.BQ.value
            self.board[4] = PieceType.BK.value

            for index in range(8, 16):
                self.board[index] = PieceType.BP.value
            for index in range(48, 56):
                self.board[index] = PieceType.WP.value
            
            self.board[56] = PieceType.WR.value
            self.board[63] = PieceType.WR.value
            self.board[57] = PieceType.WN.value
            self.board[62] = PieceType.WN.value
            self.board[58] = PieceType.WB.value
            self.board[61] = PieceType.WB.value
            self.board[59] = PieceType.WQ.value
            self.board[60] = PieceType.WK.value
        else:
            self.board = import_board[:]

    
    def print_board(self):
        for row in range(8):
            for col in range(8):
                print(f"{self.board[row * 8 + col]}".ljust(2), end = ' ')
            print("")

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

        # check left
        other_square = king_square - 1
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square >= 0 and (other_square % 8) < 7:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(king_square, self.board[other_square]):
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
                            valid_king_directions[3] = valid_king_directions[4] = False   # take away the horizontal plane from available chess moves
                        break

            other_square -= 1 # continue down path
        
        # check right
        other_square = king_square + 1
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square < 64 and (other_square % 8) > 0:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(king_square, self.board[other_square]):
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
                            valid_king_directions[3] = valid_king_directions[4] = False   # take away the horizontal plane from available chess moves
                        break
            
            other_square += 1 # continue down path
        
        # check up
        other_square = king_square - 8
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square >= 0:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(king_square, self.board[other_square]):
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
                            valid_king_directions[1] = valid_king_directions[6] = False   # take away the horizontal plane from available chess moves
                        break
            
            other_square -= 8 # continue down path
        
        # check down
        other_square = king_square + 8
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square < 64:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(king_square, self.board[other_square]):
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
                            valid_king_directions[1] = valid_king_directions[6] = False   # take away the horizontal plane from available chess moves
                        break
            
            other_square += 8 # continue down path
        
        # check upper-left
        other_square = king_square - 9
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square >= 0 and (other_square % 8) < 7:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(king_square, self.board[other_square]):
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
                            valid_king_directions[0] = valid_king_directions[8] = False   # take away the horizontal plane from available chess moves
                        break
            
            other_square -= 9 # continue down path
        
        # check upper-right
        other_square = king_square - 7
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square >= 0 and (other_square % 8) > 0:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(king_square, self.board[other_square]):
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
                            valid_king_directions[2] = valid_king_directions[5] = False   # take away the horizontal plane from available chess moves
                        break
            
            other_square -= 7 # continue down path
        
        # check lower-left
        other_square = king_square + 7
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square < 64 and (other_square % 8) < 7:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(king_square, self.board[other_square]):
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
                            valid_king_directions[2] = valid_king_directions[5] = False   # take away the horizontal plane from available chess moves
                        break
            
            other_square += 7 # continue down path
        
        # check lower-right
        other_square = king_square + 9
        ally_piece = [] # keep track of friendly pieces in this path
        piece_path = [] # keep track of the square indexes in this path
        while other_square < 64 and (other_square % 8) > 0:
            piece_path.append(other_square)

            # if piece encountered in path is friendly => Add to ally piece list
            if self.is_same_color(king_square, self.board[other_square]):
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
                            valid_king_directions[0] = valid_king_directions[8] = False   # take away the horizontal plane from available chess moves
                        break
            
            other_square += 9 # continue down path

        return in_check, check_path, pinned_squares, valid_king_directions
        

    def check_king_moves(self):
        king_moves = []

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

        in_check, check_path, pinned_squares, valid_king_directions = self.get_checks_and_pins(king_square)
        double_check = False

        # check double check
        # check from diagonal and vertical/horizontal
        if ((not valid_king_directions[0] or not valid_king_directions[2]) 
            and  (not valid_king_directions[1] or not valid_king_directions[3])):
            double_check = True
        
        # check from double diagonal 
        elif (not valid_king_directions[0] and not valid_king_directions[2]) or (not valid_king_directions[1] and not valid_king_directions[3]):
            double_check = True
        
        
        for index, safe in enumerate(valid_king_directions):
            
            # if moving to that square does not run into checks, add it to the king move options
            if(safe):
                
                # upper-left
                other_square = king_square - 9
                if index == 0 and (other_square >= 0 and (other_square % 8) < 7) and not self.is_same_color(king_square, other_square):
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                        continue
                
                # up
                other_square = king_square - 8
                if index == 1 and (other_square >= 0) and not self.is_same_color(king_square, other_square):
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                        continue
                
                # upper-right
                other_square = king_square - 7
                if index == 2 and (other_square >= 0 and (other_square % 8) > 0) and not self.is_same_color(king_square, other_square):
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                        continue
                
                # left
                other_square = king_square - 1
                if index == 3 and (other_square >= 0 and (other_square % 8) < 7) and not self.is_same_color(king_square, other_square):
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                        continue
                
                # right
                other_square = king_square + 1
                if index == 4 and (other_square < 64 and (other_square % 8) > 0) and not self.is_same_color(king_square, other_square):
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                        continue
                
                # lower-left
                other_square = king_square + 7
                if index == 5 and (other_square < 64 and (other_square % 8) < 7) and not self.is_same_color(king_square, other_square):
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                        continue
                
                # bottom
                other_square = king_square + 8
                if index == 6 and (other_square < 64) and not self.is_same_color(king_square, other_square):
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                        continue

                # lower-right
                other_square = king_square + 9
                if index == 6 and (other_square < 64 and (other_square % 8) > 0) and not self.is_same_color(king_square, other_square):
                    if not self.get_checks_and_pins(other_square, return_check_bool=True):
                        king_moves.append((king_square, other_square))
                        continue
            
            return king_moves, in_check, check_path, pinned_squares


    def check_axis_vertical_horizontal(self, move_list : List, current_square : int, piece : int):
        # check left
        other_square = current_square - 1
        while other_square >= 0 and (other_square % 8) < 7:
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
            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square += 8
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break

    def check_axis_diagonal(self,  move_list : List, current_square : int, piece : int):
        # check upper-left
        other_square = current_square - 9
        while other_square >= 0 and (other_square % 8) < 7:
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
            if self.board[other_square] == PieceType.E.value:
                move_list.append((current_square, other_square))
                other_square += 9
            elif not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
                break
            else:
                break

    def check_knight_moves(self,  move_list : List, current_square : int, piece : int):
        # 2-up, 1-left
        other_square = current_square - 17
        if other_square >= 0 and (other_square % 8) < 7:
            if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))

        # 1-up, 2-left
        other_square = current_square - 10
        if other_square >= 0 and (other_square % 8) < 6:
            if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
        
        # 1-down, 2-left
        other_square = current_square + 6
        if other_square < 64 and (other_square % 8) < 6:
            if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
        
        # 2-down, 1-left
        other_square = current_square + 15
        if other_square < 64 and (other_square % 8) < 7:
            if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
        
        # 2-up, 1-right
        other_square = current_square - 15
        if other_square >= 0 and (other_square % 8) > 0:
            if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
        
        # 1-up, 2-right
        other_square = current_square - 6
        if other_square >= 0 and (other_square % 8) > 1:
            if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))

        # 1-down, 2-right
        other_square = current_square + 10
        if other_square < 64 and (other_square % 8) > 1:
            if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
        
        # 2-down, 1-right
        other_square = current_square + 17
        if other_square < 64 and (other_square % 8) > 0:
            if self.board[other_square] == PieceType.E.value or not self.is_same_color(piece, self.board[other_square]):
                move_list.append((current_square, other_square))
    
    def check_pawn_moves(self,  move_list : List, current_square : int, piece : int):
        
        # check if black pawn
        if piece == PieceType.BP.value:
            if int(current_square / 8) == 1:
                # black pawn can make two forward moves (first move)
                if self.board[current_square + 8] == PieceType.E.value:
                    move_list.append((current_square, current_square + 8))
                    if self.board[current_square + 16] == PieceType.E.value:
                        move_list.append((current_square, current_square + 16))
            else:
                # black pawn can only move forward one square
                if self.board[current_square + 8] == PieceType.E.value:
                    move_list.append((current_square, current_square + 8))

            # check if can take at diagonal
            if self.board[current_square + 7] != PieceType.E.value and not self.is_same_color(piece, self.board[current_square + 7]):
                 move_list.append((current_square, current_square + 7))
            
            if self.board[current_square + 9] != PieceType.E.value and not self.is_same_color(piece, self.board[current_square + 9]):
                 move_list.append((current_square, current_square + 9))

        # check if white pawn
        elif piece == PieceType.WP.value:
            if int(current_square / 8) == 6:
                # black pawn can make two forward moves (first move)
                if self.board[current_square - 8] == PieceType.E.value:
                    move_list.append((current_square, current_square - 8))
                    if self.board[current_square - 16] == PieceType.E.value:
                        move_list.append((current_square, current_square - 16))
            else:
                # black pawn can only move forward one square
                if self.board[current_square - 8] == PieceType.E.value:
                    move_list.append((current_square, current_square - 8))

            # check if can take at diagonal
            if self.board[current_square - 7] != PieceType.E.value and not self.is_same_color(piece, self.board[current_square - 7]):
                 move_list.append((current_square, current_square - 7))
            
            if self.board[current_square - 9] != PieceType.E.value and not self.is_same_color(piece, self.board[current_square - 9]):
                 move_list.append((current_square, current_square - 9))


    def get_legal_moves(self, current_move=None):

        if current_move is None:
            current_move = self.move
        
        legal_moves, in_check, check_path, pinned_squares = self.check_king_moves()



        for current_square, piece in enumerate(self.board):
            
            # White to Move
            if current_move == Turn.White.value:

                #* CURRENT PIECE: ROOK
                if piece == PieceType.WR.value:
                    self.check_axis_vertical_horizontal(legal_moves, current_square, piece)
                
                #* CURRENT PIECE: BISHOP
                if piece == PieceType.WB.value:
                    self.check_axis_diagonal(legal_moves, current_square, piece)
                
                #* CURRENT PIECE: QUEEN
                if piece == PieceType.WQ.value:
                    self.check_axis_vertical_horizontal(legal_moves, current_square, piece)
                    self.check_axis_diagonal(legal_moves, current_square, piece)
                
                #* CURRENT PIECE: KNIGHT
                if piece == PieceType.WN.value:
                    self.check_knight_moves(legal_moves, current_square, piece)
                
                #* CURRENT PIECE: PAWN
                if piece == PieceType.WP.value:
                    self.check_pawn_moves(legal_moves, current_square, piece)
            # Black to Move
            elif current_move == Turn.Black.value:
                #* CURRENT PIECE: ROOK
                if piece == PieceType.BR.value:
                    self.check_axis_vertical_horizontal(legal_moves, current_square, piece)
                
                #* CURRENT PIECE: BISHOP
                if piece == PieceType.BB.value:
                    self.check_axis_diagonal(legal_moves, current_square, piece)
                
                #* CURRENT PIECE: QUEEN
                if piece == PieceType.BQ.value:
                    self.check_axis_vertical_horizontal(legal_moves, current_square, piece)
                    self.check_axis_diagonal(legal_moves, current_square, piece)
                
                #* CURRENT PIECE: KNIGHT
                if piece == PieceType.BN.value:
                    self.check_knight_moves(legal_moves, current_square, piece)
                
                #* CURRENT PIECE: PAWN
                if piece == PieceType.BP.value:
                    self.check_pawn_moves(legal_moves, current_square, piece)

        return legal_moves

                

test_board = [PieceType.E.value] * 64
test_board[36] = PieceType.WP.value
test_board[28] = PieceType.BP.value
test_board[27] = PieceType.BK.value



node = ChessNode()
node.print_board()
moves = node.get_legal_moves()
print("\nPossible Moves:",len(moves))
print("\n{}".format(moves))