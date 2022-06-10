# Names: Paulina DeVito, Oliver Pennanen, Briana Jackson
# Course: CAP4630 001
# Date: 6/17/22
# Assignment: 1
"""
This code shows how to play a game of checkers. 
The rules for the game are displayed below. These rules come from the assignment instructions page. 



Objective: 
The objective of the game is to get as many pieces as you can from the opponent. 
 
Material:
An 8 x 8 board of checkers is used with two colors one for each opponent. 

How to Win:
The game can be won when the opponent is unable to make a move. This can be done in two ways: 
The entirety of a player's pieces was captured by the opponent (when the piece is a King)  
 
Additional Rules: 
1. Only one jump is possible per move. 
2. Forward move is only allowed for each opponent. 
3. When a player jumps over another opponent's piece, the piece is not removed by the 
opponent. 
4. There are two types of moves Step or Jump. 
5. The pieces always move diagonally only on dark colored squares. 
6. When a player's piece reaches the last row on the opponent's side of the board, they can use 
one of their captured pieces to crown the piece as a king. 
7. The first player who has a piece promoted to king wins immediately.  
"""



# [[file:checker.org::*questions][questions:1]]
# !/usr/bin/env python3
# Libraries
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
from easyAI import solve_with_iterative_deepening
import numpy as np



# Oliver note: The following creates a diagonal "line" where every other spot is skipped.
# black_square
even = [0,2,4,6]
odd = [1,3,5,7]

#init 
even_row = [(i,j) for i in even for j in odd] # Oliver note: This creates a list of tuples, the tuples have 2 numbers each.
odd_row = [(i,j) for i in odd for j in even] # Oliver note: This also creates list of tuples, but the numbers are flipped per tuple.

black_squares = even_row + odd_row # Oliver note: This appends the two lists together, without reordering the contents per individual list.



class Checker(TwoPlayerGame):

    def __init__(self, players):
        # Paulina note: This is a list of players. This list is passed to the function.
        self.players = players 
        # self.board = np.arange(8 * 8).reshape(8,8)
        self.blank_board = np.zeros((8,8), dtype=object)
        self.board = self.blank_board.copy() # Oliver note: Assigns all array elements "blank values".
        # Paulina note: Identifies the black chips on the board. 
        self.black_pieces = [ # Oliver note: (part A) Creates 2 rows of black pieces on the top area of the board(?), implementation creates a list of coordinate tuples.
            (0,1), (0,3), (0,5), (0,7),
            (1,0), (1,2), (1,4), (1,6)
        ]
        # Paulina note: Identifies the white chips on the board.
        self.white_pieces = [ # Oliver note: Creates 2 rows of white pieces on the bottom area of the board(?)
            (6,1), (6,3), (6,5), (6,7),
            (7,0), (7,2), (7,4), (7,6)
        ]
        # Paulina note: Writes the black and white chips to the board. 
        # Oliver note: "board" here may be a 2 dimensional array, and selected array elements are assigned a value of "B" or "W".
        for i,j in self.black_pieces:
            self.board[i,j] = "B" #Oliver note: The values of i and j that exist in the black_pieces list is used to identify what array elements to label in self.board.
        for i,j in self.white_pieces:
            self.board[i,j] = "W" #Oliver note: The values of i and j that exist in the black_pieces list is used to identify what array elements to label in self.board.

        # Paulina note: Identifies the very end rows on the board, which are labeled as white_territory and black_territory.
        # Paulina note: When a black chip gets to white chip territory, white loses.
        # Paulina note: Conversely, when a white chip gets to black chip territory, black loses.
        self.white_territory = [(7,0), (7,2), (7,4), (7,6)]
        self.black_territory = [(0,1), (0,3), (0,5), (0,7)]

        # Paulina note: Here, we are creating variables that represent the positions of each player's pieces. 
        # Paulina note: The positions of pieces are given in a list.
        # Paulina note: For example, self.players[0].pos is a list of tuples that give the current locations of all of the white pieces.
        self.players[0].pos = self.white_pieces 
        self.players[1].pos = self.black_pieces

        self.current_player = 1  # Paulina note: First player starts.
    #Oliver note: End of Constructor

 
 
    def possible_moves_on_white_turn(self): 

        table_pos = [] #Oliver note: List of all possible moves.
        old_new_piece_pos = [] 

        # board position before move
        board = self.blank_board.copy() # Oliver note: Board is blanked again(??)
        for (p,l) in zip(self.players, ["W", "B"]): # Oliver note: This explains zip: https://www.w3schools.com/python/ref_func_zip.asp
            for x,y in p.pos: # Oliver note: Goes through each game piece of a player.
                board[x,y] = l # Oliver note: The board's coordinates that match the coordinates of the player's pieces is assigned either "W" for player 1, or "B" for player 2.
        
        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos: # Oliver note: For every single enemy piece.
            old_piece_pos = v  # Oliver note: old_piece_pos has coordinate of one of the pieces of the opposing player. I think it's the opposing player because of the [self.current_player-1] part.

            step_pos = [(v[0]-1, v[1]-1), (v[0]-1, v[1]+1)] # Oliver note: This marks 2 coordinates, 1st is diagonally left-down of the current piece, 2nd is diagonally left-up of the current piece.
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares): # Oliver note: Check if coordinate in step_pos (One of 2 diagonal next possible moves) is in the bounds of the game board.
                    if board[n[0], n[1]] in ["B","W"]: # Oliver note: Check if the coordinates of a next possible move contains a black or white game piece.
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0] 
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1] 
                        j = (y,x) # Oliver note: Make a coordinate from the manipulated x and y coordinates from the 2 lines above.
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7) # Oliver note: Basic check of if coordinates of j are inside the game board (some moves could go out of bounds!).
                        if (j[0] <= 7) and (j[1] <=7): 
                            is_position_empty = (board[j[0], j[1]] == 0) 
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j)) 
                    else:
                        old_new_piece_pos.append((old_piece_pos,n)) 

        # board position after  move
        for i,j in old_new_piece_pos: 
            # Oliver note: Example: iteration 1: (4,3),(3,4). iteration 2: (3,4),(4,3).
            print(f"i = {i}") # Oliver note: https://www.geeksforgeeks.org/formatted-string-literals-f-strings-python/
            # Oliver note: Example: "i = (4,3)" (iteration 1)
            b = board.copy() # Oliver note: Temp copy of board.
            b[i[0], i[1]] = 0 # old position     # Oliver note: Example: (4, 3) = 0 (iteration 1). Marks the past location of a game piece as "null"
            b[j[0], j[1]] = "W" # new position     # Oliver note: Example: (3, 4) = "W" (iteration 1). Marks the new location with a white piece (the piece didn't really get destroyed, just "moved").
            # print(b)
            table_pos.append(b) #Oliver note: This was a blank list from the beginning of the function.
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_white_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        self.board = board
        return table_pos



    def possible_moves_on_black_turn(self):
        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            # Paulina note: Checks the potential moves for each old piece.
            step_pos = [(v[0]+1, v[1]-1), (v[0]+1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                # Paulina note: Checks if it's within bounds and is a black square.
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]: # Paulina note: If we need to jump, we go here.
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j)) # ((x,y),(a,b))
                    else: # Paulina note: If we need to step, we go here.
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move

        """
        Paulina note:
        old_new_piece_pos = [ ((a,b), (a,b)), ((a,b), (a,b)), ((a,b), (a,b)) ]

        for i,j is basically going to get the following: 

            i = (a,b) #old posiiton
            j = (a,b) #new position

        where a and b are some coordinates
        """
        for i,j in old_new_piece_pos: 
            b = board.copy()
            b[i[0], i[1]] = 0 #coord of i (old pos)
            b[j[0], j[1]] = "B" #coord of j (new pos)
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_black_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        self.board = board
        return table_pos



    def possible_moves(self):
        """
        """
        if self.current_player == 2:
            return self.possible_moves_on_black_turn()
        else:
            return self.possible_moves_on_white_turn()



    def get_piece_pos_from_table(self, table_pos):
        if self.current_player-1 == 0:
            x = np.where(table_pos == "W")
        elif self.current_player-1 == 1:
            x = np.where(table_pos == "B")
        else:
            raise ValueError("There can be at most 2 players.")

        # Paulina note: "assert" is a debugging tool. In this case, it's used to confirm that there are 16 pieces on the board. 
        assert len(np.where(table_pos != 0)[0]) == 16, f"In get_piece_pos_from_table(), there are {len(np.where(table_pos != 0)[0])} pieces on the board  \n {table_pos}"
        
        return [(i,j) for i,j in zip(x[0], x[1])]



    def make_move(self, pos): 
        """
        assign pieces index of pos array to current player position.
        parameters

        -------
        pos = position of all pieces on the (8 x 8) boards. type numpy array.
        example of pos
        [[0,B,0,B,0,B,0,B],
         [B,0,B,0,B,0,B,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,W,0,W,0,W,0,W],
         [W,0,W,0,W,0,W,0]]
        ------
        """
        # Paulina note: This sets the current player position to the result of calling get_piece_pos_from_table with the argument pos.
        # Paulina note: We assume that pos is the chosen move.
        self.players[self.current_player - 1].pos = self.get_piece_pos_from_table(pos)



    def lose(self):
        """
        black lose if white piece is in black territory 
        white lose if black piece is in black territory
        """
        # Paulina note: Below is just some psuedocode that I used to help write the program.
        """
        if piece is in self.black_territory
            return loss
        if piece is in self.white_territory
            return loss
        else no loss
        """
        for i,j in self.white_territory:
            if (self.board[i,j] == "B"):
                return True # Paulina note: If a black piece is in white territory, we have met a lose condition.
        for i,j in self.black_territory:
            if (self.board[i,j] == "W"):
                return True # Paulina note: If a white piece is in black territory, we have met a lose condition.
        return False # Paulina note: This is the case when we have not met a lose condition.



    def is_over(self):
        """
        game is over immediately when one player get one of its piece into opponent's territory.
        """
        # Paulina note: The game is over when there are no more possible moves to make or...
        # ...when the conditions of a loss are met.
        return (self.possible_moves() == []) or self.lose() 



    def show(self):
        """
        show 8*8 checker board.
        """
        # board position before move
        board = self.blank_board.copy()
        print(f"player 1 positions = {self.players[0].pos}")
        print(f"player 2 positions = {self.players[1].pos}")
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        print('\n')
        print(board)



    def scoring(self):
       """
       win = 0
       lose = -100
       """
       # Paulina note: This helps us teach the AI how to play the game.
       # Paulina note: If there is a loss, we return -100. If there is a win, we return 0.
       # Paulina note: We call the lose function to check if a loss condition has been met. 
       return -100 if self.lose() else 0





if __name__ == "__main__":
    ai = Negamax(1) # The AI will think 13 moves in advance
    game = Checker( [ AI_Player(ai), AI_Player(ai) ] )
    history = game.play()
# questions:1 ends here