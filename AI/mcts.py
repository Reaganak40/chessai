
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

    def get_legal_moves(self):
        legal_moves = []

        for current_square, piece in enumerate(self.board):
            
            #* CURRENT PIECE: ROOK
            if piece == PieceType.WR.value or piece == PieceType.BR.value:
                self.check_axis_vertical_horizontal(legal_moves, current_square, piece)
            
            #* CURRENT PIECE: BISHOP
            if piece == PieceType.WB.value or piece == PieceType.BB.value:
                self.check_axis_diagonal(legal_moves, current_square, piece)
            
            #* CURRENT PIECE: QUEEN
            if piece == PieceType.WQ.value or piece == PieceType.BQ.value:
                self.check_axis_vertical_horizontal(legal_moves, current_square, piece)
                self.check_axis_diagonal(legal_moves, current_square, piece)
            
            #* CURRENT PIECE: KNIGHT
            if piece == PieceType.WN.value or piece == PieceType.BN.value:
                self.check_knight_moves(legal_moves, current_square, piece)

        return legal_moves

                

test_board = [PieceType.E.value] * 64
test_board[36] = PieceType.WK.value


node = ChessNode()
node.print_board()
print(node.get_legal_moves())