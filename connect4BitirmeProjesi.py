from tkinter import *
import time
import math
import random




PLAYER = 0

EMPTY = 0

WINDOW_LENGTH = 4

class App:
    yellowCoin = 1
    redCoin = 2
    turn = yellowCoin
    boardPieces = []
    boardButtons = []

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.yellowCoin
        if piece == self.yellowCoin:
            opp_piece = self.redCoin

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == self.redCoin and window.count(0) == self.redCoin:
            score += self.redCoin

        return score


    def score_position(self, piece):
        score = 0
        center_array = []
        ## Score center column
        for row in range (int(ROW_COUNT/self.redCoin)):
            for col in range (int(COLUMN_COUNT/self.redCoin)):
                center_array.append(self.boardPieces[row][col])

        # center_array = [Button(i) for i in list(self.board[:][ COLUMN_COUNT//self.redCoin])]
        # center_count = center_array.count(piece)
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        row_array = []
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT):
                row_array.append(self.boardPieces[row][col])

            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            # col_array = [Button(i) for i in list(self.board[:][c])]
            col_array = []
            for i in range(0,ROW_COUNT):
                for j in range(0,int(COLUMN_COUNT/self.redCoin)):
                    col_array.append(self.boardPieces[i][j])
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [self.boardPieces[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [self.boardPieces[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)
        # score = random.random()
        return score

    def is_valid_location(self, col):
        return self.boardPieces[0][col] == 0

    def get_valid_locations(self, row):
        valid_locations = []
        for column in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.is_valid_location(column):
                    valid_locations.append(column)

        return valid_locations

    def is_terminal_node(self):
        return self.isWinner(self.yellowCoin) or self.isWinner(self.redCoin)

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.boardPieces[r][col] != self.yellowCoin and self.boardPieces[r][col] != self.redCoin:
                return r
            else:
                return -1
    def get_next_open_row_col(self):
            for r in range(ROW_COUNT):
                for c in range(COLUMN_COUNT):
                    if self.boardPieces[r][c] != self.yellowCoin or self.boardPieces[r][c] != self.redCoin:
                        return r, c

    def minimax(self, depth, alpha, beta, maximizingPlayer, row, col):
        valid_locations = self.get_valid_locations(row)
        if(len(valid_locations) == 0):
            row = self.get_next_open_row(col)
            valid_locations = self.get_valid_locations(row)
        is_terminal = self.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.isWinner(self.redCoin):
                    return (-1, -100000000000000)
                elif self.isWinner(self.yellowCoin):
                    return (-1, 10000000000000)
                else: # Game is over, no more valid moves
                    return (-1, 0)
            else: # Depth is zero
                return (-1, self.score_position(self.redCoin))
        if maximizingPlayer:
            value = -math.inf
            column = 0
            # if(len(valid_locations) == 0):
            #     row = self.get_next_open_row(col)
            # else:
            column = random.choice(valid_locations)

            # if(len(self.get_valid_locations()) == 0):
            for col in valid_locations:
                row = self.get_next_open_row(col)

        # for col in valid_locations:
        #     row = self.get_next_open_row(col)
                b_copy = self.boardPieces.copy()
                self.drop_piece(b_copy,row, col, self.redCoin)
                new_score = self.minimax(depth-2, alpha, beta, False, row, col)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(col)
                b_copy = self.boardPieces.copy()
                self.drop_piece(b_copy,row, col, self.yellowCoin)
                new_score = self.minimax(depth-1, alpha, beta, True, row, col)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def drop_piece(self, board, row, col, piece):
        if(piece == self.redCoin):
            if((board[row][col]) == self.redCoin or (board[row][col]) == self.yellowCoin):
                print("already clicked")
                # self.playRed( row, col)
            else:
                (board[row][col]) = self.redCoin
                self.turn = self.yellowCoin
        else:
            (board[row][col]) = self.yellowCoin
            self.turn = self.redCoin
            
        theWindow.update()

    def checkAcross(self, color): 
        #check for 4 across
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT-3):
                if (((self.boardPieces[row][col]) ) == color and 
                (self.boardPieces[row][col+1])  == color and 
                (self.boardPieces[row][col+2])  == color and
                (self.boardPieces[row][col+3]) == color):
                    print("across")
                    return True
                else:
                    return False

    def checkUpAndDown(self, color): 
        #check for 4 up and down
        for row in range (ROW_COUNT-3):
            for col in range (COLUMN_COUNT):
                if (((self.boardPieces[row][col])) == color   and 
                (self.boardPieces[row+1][col]) == color and
                (self.boardPieces[row+2][col]) == color and
                (self.boardPieces[row+3][col]) == color):
                    print("up and down")
                    return True
                else:
                    return False

    def checkUpwardDiagonal(self, color): 
        #check upward diagonal
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT-3):
                if (((self.boardPieces[row][col])) == color and 
                (self.boardPieces[row-1][col+1]) == color and
                (self.boardPieces[row-self.redCoin][col+2]) == color and
                (self.boardPieces[row-3][col+3]) == color):
                    print("upward diagonal")
                    return True
                else:
                    return False

    def checkDownwardDiagonal(self, color): 
        #check downward diagonal
        for row in range (ROW_COUNT-3):
            for col in range (COLUMN_COUNT-3):
                if (((self.boardPieces[row][col])) == color and 
                (self.boardPieces[row+1][col+1]) == color and
                (self.boardPieces[row+2][col+2]) == color and
                (self.boardPieces[row+3][col+3]) == color):
                    print("downward diagonal")
                    return True
                else:
                    return False


    def isWinner(self, piece):
        if(self.checkAcross(piece) or
            self.checkUpAndDown(piece) or
            self.checkUpwardDiagonal(piece) or    
            self.checkDownwardDiagonal(piece)):
            print(" wins")
            return True
        else:
            return False
                
    def playYellow(self, i, j):
        self.drop_piece(self.boardPieces, i, j, self.yellowCoin)
        self.boardButtons[i][j]["bg"] = "yellow"
        self.turn = self.redCoin
        print("Reds turn")

    def playRed(self):
        col, minimax_score = self.minimax(5, -math.inf, math.inf, True, 0, -1)
        if(col == -1):
            return
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(self.boardPieces, row, col, self.redCoin)
            self.boardButtons[row][col]["bg"] = "red"

        self.turn = self.yellowCoin
        print("Yellows turn")

    def playGame(self, i, j):
        self.playYellow(i,j)
        if(self.isWinner((self.boardPieces[i][j]))):
            return
        self.playRed()
        if(self.isWinner((self.boardPieces[i][j]))):
            return

    def initialize_board(self):
        self.boardPieces = [[0 for x in range(ROW_COUNT)] for y in range(COLUMN_COUNT)] 
        self.boardButtons = [[0 for x in range(ROW_COUNT)] for y in range(COLUMN_COUNT)] 

    def __init__(self, myWindow) -> None:
        # self.board = [[0]*COLUMN_COUNT]*ROW_COUNT
        self.initialize_board()
        for i in range(0,ROW_COUNT):
            for j in range(0,COLUMN_COUNT):

                theFrame = Frame(master=myWindow, relief=FLAT, borderwidth=5, bg="blue")
                theFrame.grid(row=i, column=j, padx=1, pady=1)
                myButton = Button(master=theFrame, width=5, height=5, text=str(i) + "," + str(j), padx=5, pady=5)
                myButton["command"] = lambda k=i, m=j , buttonParam = myButton: self.playGame(k, m)
                myButton.pack()
                self.boardButtons[i][j]= myButton

                theWindow.update()



               

if __name__ == "__main__":
    ROW_COUNT = 6
    COLUMN_COUNT = 6
    theWindow = Tk()
    theWindow.title("Connect 4")
    theWindow.geometry('500x700')
    theWindow['bg'] = "blue"
    # Calling our App
    app = App(theWindow)
    # to run infinitely
    theWindow.mainloop()