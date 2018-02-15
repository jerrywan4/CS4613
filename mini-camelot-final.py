"""
    Final build of mini camelot game
    Programmer: Jerry Wan
    CS4613
    Fall 2017
    Professor: Edward Wong
"""

#IMPORT STATEMENT
import operator, calendar, time

#GLOBAL VARIABLES
max_depth = 0
num_nodes = 0
max_node_prunes = 0
min_node_prunes = 0
start_time = 0
depth_limit = 4
alphanumeric_int_dict = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
int_alphanumeric_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}

#Define Board class
class Board:
    def __init__(self, white=None, black=None, white_castle=None, black_castle=None):
        #Board is initialized as an array
        self.board = []
        for i in range (0,112):
            self.board.append("-")

        #List of unusable spaces
        self.emptys = ['A1','A2','A3','B1','B2','C1','F1','G1','G2','H1','H2','H3','A12','A13','A14','B13','B14','C14','F14','G13','G14','H12','H13','H14']
        if white == None:
            #Initial list of white piece spaces
            self.white = ['C5','D5','E5','F5','D6','E6']
        else:
            self.white = white
        if black == None:
            #Initial list of black piece spaces
            self.black = ['D9','E9','C10','D10','E10','F10']
        else:
            self.black = black
        if white_castle == None:
            self.white_castle = ['D14', 'E14']
        if black_castle == None:
            self.black_castle = ['D1', 'E1']

    def display_board(self):
        for i in range(0,len(self.board)-1):
            self.board[i] = 'O'
        
        #Place 'w' where white pieces are in initial list
        for coord in self.white:
            idx = alphanumeric_to_int(coord)
            self.board[idx] = 'White'

        #Place 'b' where black pieces are in initial list
        for coord in self.black:
            idx = alphanumeric_to_int(coord)
            self.board[idx] = 'Black'

        #Place empty char where empty pieces are in initial list
        for coord in self.emptys:
            idx = alphanumeric_to_int(coord)
            self.board[idx] = 'EMPTY'

        for coord in self.white_castle:
            idx = alphanumeric_to_int(coord)
            self.board[idx] = 'GOAL'

        for coord in self.black_castle:
            idx = alphanumeric_to_int(coord)
            self.board[idx] = 'GOAL'
        
        #Create grid
        print("\tA\tB\tC\tD\tE\tF\tG\tH")
        row = 1
        print_str = ""
        for i in range(0,len(self.board)):
            if i%8 == 0:
                if i != 0:
                    print_str += '\t' + str(row) + '\n\n'
                    row += 1
                print_str += str(row)
            print_str += '\t' + self.board[i]            
        print(print_str + '\t' + str(row))

#Decode alphanumeric coords to board index
def alphanumeric_to_int(coord):
    #dict to convert row letter to row #
    alphanumeric_int_dict = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}

    #check if coord exceeds 3 digits or coord row is not in A:H
    if len(coord) > 3 or coord[0] not in alphanumeric_int_dict.keys():
        raise ValueError("Coordinate is invalid.")
    else:
        idx = (int(coord[1:])*8) + alphanumeric_int_dict[coord[0]]
        return idx-8
    
#Encode board index to alphanumeric coords
def int_to_alphanumeric(idx):
    #dict to convert row # to row letter
    int_alphanumeric_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}

    if idx not in range(0,112):
        raise ValueError("Coordinate is invalid.")
    else:
        row = int(idx/8) + 1
        col = int_alphanumeric_dict[idx%8]

        return str(col) + str(row)


def generate_player_move_list(board):
    move_list = []
    capture_flag = False

    player_pieces = board.white

    for alpha_coord in player_pieces:
        if alpha_coord[0] == 'A':
            int_moves_list = [-8,-7,1,8,9]
        elif alpha_coord[0] == 'H':
            int_moves_list = [-9,-8,-1,7,8]
        else:
            int_moves_list = [-9,-8,-1,1,7,8,9]
        idx = alphanumeric_to_int(alpha_coord)
        for intmove in int_moves_list:
            int_dest = idx+intmove
            int_dest_alpha = int_to_alphanumeric(idx+intmove)
            #player capturing move
            if int_dest_alpha in board.black:
                if (not(int_dest_alpha[0] == 'A' and alpha_coord[0] == 'B')) and (not(int_dest_alpha[0] == 'H' and alpha_coord[0] == 'G')):
                    capture_dest = idx+intmove+intmove
                    capture_dest_alpha = int_to_alphanumeric(capture_dest)
                    if capture_dest in range(0,112) and capture_dest_alpha not in board.black and capture_dest_alpha not in board.white and capture_dest_alpha not in board.emptys:
                        move_list.append([alpha_coord, capture_dest_alpha, int_dest_alpha])
                        capture_flag = True
            #player cantering move
            if int_dest_alpha in board.white:
                if (not(int_dest_alpha[0] == 'A' and alpha_coord[0] == 'B')) and (not(int_dest_alpha[0] == 'H' and alpha_coord[0] == 'G')):
                    canter_dest = idx+intmove+intmove
                    canter_dest_alpha = int_to_alphanumeric(canter_dest)
                    if canter_dest in range(0,112) and canter_dest_alpha not in board.black and canter_dest_alpha not in board.white and canter_dest_alpha not in board.emptys:
                        move_list.append([alpha_coord, canter_dest_alpha])
            #player non-capturing, non-cantering move
            if int_dest in range(0,112) and int_dest_alpha not in board.black and int_dest_alpha not in board.white and int_dest_alpha not in board.emptys:
                move_list.append([alpha_coord, int_dest_alpha])
    
    if capture_flag:
        temp_move_list = []
        for move in move_list:
            if len(move) == 3:
                temp_move_list.append(move)
        move_list = list(temp_move_list)

    return move_list

def generate_AI_move_list(board):
    move_list = []
    capture_flag = False
    
    AI_pieces = board.black

    for alpha_coord in AI_pieces:
        if alpha_coord[0] == 'A':
            int_moves_list = [-8,-7,1,8,9]
        elif alpha_coord[0] == 'H':
            int_moves_list = [-9,-8,-1,7,8]
        else:
            int_moves_list = [-9,-8,-1,1,7,8,9]
        idx = alphanumeric_to_int(alpha_coord)
        for intmove in int_moves_list:
            int_dest = idx+intmove
            int_dest_alpha = int_to_alphanumeric(idx+intmove)
            #AI capturing move
            if int_dest_alpha in board.white:
                if (not(int_dest_alpha[0] == 'A' and alpha_coord[0] == 'B')) and (not(int_dest_alpha[0] == 'H' and alpha_coord[0] == 'G')):
                    capture_dest = idx+intmove+intmove
                    capture_dest_alpha = int_to_alphanumeric(capture_dest)
                    if capture_dest in range(0,112) and capture_dest_alpha not in board.black and capture_dest_alpha not in board.white and capture_dest_alpha not in board.emptys:
                        move_list.append([alpha_coord, capture_dest_alpha, int_dest_alpha])
                        capture_flag = True
            #AI cantering move
            if int_dest_alpha in board.black:
                if (not(int_dest_alpha[0] == 'A' and alpha_coord[0] == 'B')) and (not(int_dest_alpha[0] == 'H' and alpha_coord[0] == 'G')):
                    canter_dest = idx+intmove+intmove
                    canter_dest_alpha = int_to_alphanumeric(canter_dest)
                    if canter_dest in range(0,112) and canter_dest_alpha not in board.black and canter_dest_alpha not in board.white and canter_dest_alpha not in board.emptys:
                        move_list.append([alpha_coord, canter_dest_alpha])
            #AI non-capturing, non-cantering move
            if int_dest in range(0,112) and int_dest_alpha not in board.black and int_dest_alpha not in board.white and int_dest_alpha not in board.emptys:
                move_list.append([alpha_coord, int_dest_alpha])
    
    if capture_flag:
        temp_move_list = []
        for move in move_list:
            if len(move) == 3:
                temp_move_list.append(move)
        move_list = list(temp_move_list)

    return move_list

#Define function for AI move
def AI_move(board, move):
    if move in generate_AI_move_list(board):
        for i in range(0,len(board.black)):
            if board.black[i] == move[0]:
                board.black[i] = move[1]
        if len(move) == 3:           
            board.white.remove(move[2])
    else:
        raise ValueError("AI Move Error")

# Function to convert player input to player move
# First iteration needs testing
def convert_player_input(board):
    player_moves = generate_player_move_list(board)
    move = []
    if len(player_moves[0]) == 3:
        input("Capture move identified, press enter to continue.")
        board.black.remove(player_moves[0][2])
        ctr = 0
        for piece in board.white:
            if piece == player_moves[0][0]:
                board.white[ctr] = player_moves[0][1]
            ctr+=1
    else:
        while True:
            move_piece = input("Please enter the coordinate of the piece you would like to move.")
            while len(move_piece) > 3 or move_piece[0] not in alphanumeric_int_dict.keys():
                move_piece = input("Please enter the coordinate of the piece you would like to move.")
            if move_piece not in board.white:
                print("Please enter a valid piece coordinate.")
                continue
            else:
                move.append(move_piece)
                break

        while True:
            move_dest = input("Please enter the coordinate of where you would like to move your piece.")
            while len(move_dest) > 3 or move_dest[0] not in alphanumeric_int_dict.keys():
                move_dest = input("Please enter the coordinate of where you would like to move your piece.")

            move.append(move_dest)
            # if all(move_piece == move[0] and move_dest != move[1] for move in player_moves):
            ctr = 0
            for move in player_moves:
                if move[0] == move_piece:
                    if move[1] == move_dest:
                        ctr = 1
                        break
            if ctr == 0:
                print("Please enter a valid destination coordinate.")
                continue
            else:
                break
        move.append(move_piece)
        move.append(move_dest)

        ctr = 0
        for piece in board.white:
            if piece == move[0]:
                board.white[ctr] = move[1]
            ctr+=1

#ABOVE CODE IS TENTATIVELY DONE



#Function to implement alpha beta search algorithm for AI agent
def a_b_search(state, depth):
    global max_depth
    global num_nodes
    global max_node_prunes
    global min_node_prunes
    global start_time
    global depth_limit

    start_time = float(time.time())

    num_nodes += 1

    #NEED TO DETERMINE INITIAL ALPHA AND BETA VALUES
    alpha = -1000
    beta =  1000
    capture_flag = None

    move_list = generate_AI_move_list(state)
    moves_and_val = {}
    for j in range(0,len(move_list)):
        move = move_list[j]
        updated_board = Board(list(state.white), list(state.black))
        AI_pieces = updated_board.black
        player_pieces = updated_board.white
        # for i in range(0,len(updated_board.black)):
        #     if updated_board.black[i] == move[0]:
        #         updated_board.black[i] = move[1]
        #     if len(move_list[0]) == 3:
        #         capture_flag = move
        #         updated_board.white.remove(move[2])
        #     val = max_value(updated_board, alpha, beta, depth+1)
        #     moves_and_val[j] = val
        for piece_coord in AI_pieces:
            if piece_coord == move[0]:
                piece_coord = move[1]
        if len(move) == 3:
            capture_flag = move
            updated_board.white.remove(move[2])
        val = max_value(updated_board, alpha, beta, depth+1)
        moves_and_val[j] = val

    best = max(moves_and_val, key = moves_and_val.get)

    finish_time = float(time.time())
    search_time = finish_time-start_time
    if search_time < 5.0 and max_depth == depth_limit:
        depth_limit += 1
        print("Depth level of search increased.")
        return a_b_search(state, depth)
    else:
        print("The search took", search_time, "seconds.")
        if capture_flag == None:
            return move_list[best]
        else:
            return capture_flag

#Function to determine minimax max value
def max_value(state, alpha, beta, depth):
    global max_depth
    global num_nodes
    global max_node_prunes
    global min_node_prunes    

    num_nodes += 1
    max_depth = max(max_depth, depth)

    if terminal_check(state, depth):
        return eval(state)
    max_val = -1000
    move_list = generate_player_move_list(state)
    for move in move_list:
        updated_board = Board(list(state.white), list(state.black))
        # AI_pieces = updated_board.black
        # player_pieces = updated_board.white
        for i in range(0,len(updated_board.white)):
            if updated_board.white[i] == move[0]:
                updated_board.white[i] = move[1]
        if len(move) == 3:
            updated_board.black.remove(move[2])
        max_val = max(max_val, min_value(updated_board, alpha, beta, depth+1))
        if max_val >= beta:
            max_node_prunes += 1
            return max_val
        alpha = max(alpha, max_val)
    return max_val

#Function to determine minimax min value
def min_value(state, alpha, beta, depth):
    global max_depth
    global num_nodes
    global max_node_prunes
    global min_node_prunes

    num_nodes += 1
    max_depth = max(max_depth, depth)

    if terminal_check(state, depth):
        return eval(state)
    min_val = 1000
    move_list = generate_AI_move_list(state)
    for move in move_list:
        updated_board = Board(list(state.white), list(state.black))
        # AI_pieces = updated_board.black
        # player_pieces = updated_board.white
        for i in range(0,len(updated_board.black)):
            if updated_board.black[i] == move[0]:
                updated_board.black[i] = move[1]
        if len(move) == 3:
            updated_board.white.remove(move[2])
        min_val = min(min_val, max_value(updated_board, alpha, beta, depth+1))
        if min_val <= alpha:
            min_node_prunes += 1
            return min_val
        beta = min(beta, min_val)
    return min_val

#Function to check for terminal state or cutoff
def terminal_check(board, depth):    
    global start_time
    global depth_limit

    player_pieces = board.white
    AI_pieces = board.black
    check_time = float(time.time())
    total_time = check_time - start_time

    if depth != 0 and total_time > 10.0:
        return True

    if depth >= depth_limit:
        return True

    white_goals = ['D14', 'E14']
    black_goals = ['D1', 'E1']

    if len(board.white) == 0 or len(board.black) == 0:
        return True

    if len(board.white) == 1 and len(board.black) == 1:
        return True

    for piece_coord in player_pieces:
        if piece_coord in white_goals:
            return True
    for piece_coord in AI_pieces:
        if piece_coord in black_goals:
            return True

    return False

#Function to determine values for various states
def eval(board):
    white_goals = ['D14','E14']
    black_goals = ['D1','E1']
    player_pieces = board.white
    AI_pieces = board.black

    white_dist = 13
    black_dist = 13

    if len(board.white) == 1 and len(board.black) == 1:
        return 0

    for piece_coord in player_pieces:
        piece_coord_int = alphanumeric_to_int(piece_coord)
        if piece_coord in white_goals:
            return 1000
        white_dist = min(white_dist,13-int(piece_coord_int/8))
    for piece_coord in AI_pieces:
        if piece_coord in black_goals:
            return -1000
        black_dist = min(black_dist,int(piece_coord_int/8))

    eval_num = 1000 * ((0.2 * ((len(player_pieces) - len(AI_pieces))/5)) + (0.4 * (-1/black_dist)) + (0.4 * (1/white_dist)))
    
    return eval_num

#Print out results of search
def print_search_stats():
    print("The search reached a depth of",max_depth,"levels.")
    print("The search generated",num_nodes,"nodes.")
    print("The search max player made",max_node_prunes,"prunes.")
    print("The search min player made",min_node_prunes,"prunes.")

def check_goal_state(board):
    white_goals = ['D14','E14']
    black_goals = ['D1','E1']
    player_pieces = board.white
    AI_pieces = board.black

    if len(player_pieces) == 0:
        return -1

    if len(AI_pieces) == 0:
        return 1

    for piece_coord in player_pieces:
        if piece_coord in white_goals:
            return 1
    for piece_coord in AI_pieces:
        if piece_coord in black_goals:
            return -1

    if len(board.white) == 1 and len(board.black) == 1:
        return 0

    return 2    

s = Board()
s.display_board()

while True:
    char = input("Would you like to move first(1) or second(2)? Enter 1 for first, 2 for second.")
    if char == '1':
        human_num = 1
        break
    elif char == '2':
        human_num = -1
        break
    print("Invalid character. Choose '1' or '2'.")

while True:
    difficulty = input("Enter the level of difficulty (1, 2, or 3): ")
    if difficulty == '1':
        diff = 1
        break
    elif difficulty == '2':
        diff = 2
        break
    elif difficulty == '3':
        diff = 3
        break
    print("Invalid character. Choose '1', '2' or '3'.")

while True:
    if human_num == 1:
        convert_player_input(s)
        s.display_board()
        if check_goal_state(s) != 2 : break
        AI_move(s,a_b_search(s,diff))
        print_search_stats()
        s.display_board()
        if check_goal_state(s) != 2 : break
    else:
        AI_move(s,a_b_search(s,diff))
        print_search_stats()
        s.display_board()
        if check_goal_state(s) != 2 : break
        convert_player_input(s)
        s.display_board()
        if check_goal_state(s) != 2 : break
        
if check_goal_state(s) == 1:
    print("GAME OVER. White has won the game!")
elif check_goal_state(s) == -1:
    print("GAME OVER. Black has won the game!")
elif check_goal_state(s) == 0:
    print("GAME ENDED IN A DRAW.")