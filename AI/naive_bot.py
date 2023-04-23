from chess_node import *

class NaiveBot:

    def __init__(self):
        pass

    def suggest_move(state : ChessNode):
        moves = state.get_legal_moves()

        piece_value_states = [] # the value state based the opponents un-captured pieces
        move_value_states = []  # the value state based on potential new moves 

        for move in moves:
            new_state : ChessNode = state.create_child(move, make_orphan=True) # don't add to node tree

            new_state_moves = new_state.get_legal_moves()
            
            if len(new_state_moves) == 0:
                return move # checkmate or stalemate
            
            piece_value_states.append(new_state.board_piece_value(new_state.move)) # add the total value of pieces for the opponent to a list of value states
            
            new_state.move = Turn.Black.value if new_state.move == Turn.White.value else Turn.White.value
            
            try:
                move_potential = len(new_state.get_legal_moves())
            except:
                return move # puts king in check, just do it.
            
            move_value_states.append(move_potential)
        
        # make move that takes best piece
        min_state = min(piece_value_states)
        state_count = 0
        state_index = 0

        for index, pvs in enumerate(piece_value_states):
            if pvs == min_state:
                state_count += 1
                state_index = index
                if state_count > 1:
                    break
        
        if state_count == 1:
            return moves[state_index]
        
        # if tie, make move that gives move new moves
        max_state = max(move_value_states)
        state_count = 0
        state_index = 0

        for index, mvs in enumerate(move_value_states):
            if mvs == max_state:
                return moves[state_index]