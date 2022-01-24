from tkinter import *
import time
import math
import random



PLAYER = 0
AI = 1

EMPTY = 0

WINDOW_LENGTH = 4

class App:
    yellowCoin = 0
    redCoin = 1
    turn = yellowCoin
    board = {}

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.yellowCoin
        if piece == self.yellowCoin:
            opp_piece = self.redCoin

        if self.pieceCounter(window, piece) == 4:
            score += 100
        elif self.pieceCounter(window, piece) == 3: #and window.count(EMPTY) == 1:
            score += 5
        elif self.pieceCounter(window, piece) == 2: #and window.count(EMPTY) == 2:
            score += 2

        if self.pieceCounter(window, opp_piece) == 3: #and window.count(EMPTY) == 1:
            score -= 4

        return score
    def pieceCounter(self, theArray, thePiece):
        count = 0
        color = "white"
        if (thePiece == self.redCoin):
            color = "red"
        else:
            color = "yellow"


        for element in theArray:
            if(element["bg"] == color):
                count = count + 1

        return count


    def score_position(self, piece):
        score = 0
        center_array = []
        ## Score center column
        for row in range (int(ROW_COUNT/2)):
            for col in range (int(COLUMN_COUNT/2)):
                center_array.append(self.board[row][col])

        # center_array = [Button(i) for i in list(self.board[:][ COLUMN_COUNT//2])]
        # center_count = center_array.count(piece)
        center_count = self.pieceCounter(center_array, piece)
        score += center_count * 3

        ## Score Horizontal
        row_array = []
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT):
                row_array.append(self.board[row][ col])

            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            # col_array = [Button(i) for i in list(self.board[:][c])]
            col_array = []
            for i in range(0,ROW_COUNT):
                for j in range(0,int(COLUMN_COUNT/2)):
                    col_array.append(self.board[i][j])
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [self.board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [self.board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)
        # score = random.random()
        return score

    def is_valid_location(self, col):
        # color = (self.board[ROW_COUNT-1][col])["bg"] 
        valid = False
        for i in range (COLUMN_COUNT):
            color = (self.board[i][col])["bg"] 
            if(color== "red"  or color == "yellow"):
                valid = False
                break
            else:
                valid = True
        return valid

    def get_valid_locations(self):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            nextOpenRow = self.get_next_open_row(col)
            if(nextOpenRow > -1 and nextOpenRow < ROW_COUNT):
                valid_locations.append(col)
        return valid_locations

    def is_terminal_node(self):
        return self.isWinner("yellow") or self.isWinner("red")

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col]["bg"] != "yellow" or self.board[r][col]["bg"] != "red":
                return r
    def get_next_open_row_col(self):
            for r in range(ROW_COUNT):
                for c in range(COLUMN_COUNT):
                    if self.board[r][c]["bg"] != "yellow" or self.board[r][c]["bg"] != "red":
                        return r, c

    def minimax(self, depth, alpha, beta, maximizingPlayer, yellowI, yellowJ):
        valid_locations = self.get_valid_locations()
        if(len(valid_locations) == 0):
            row, col = self.get_next_open_row_col()

        is_terminal = self.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.isWinner("red"):
                    return (-1, -100000000000000)
                elif self.isWinner("yellow"):
                    return (-1, 10000000000000)
                else: # Game is over, no more valid moves
                    return (-1, 0)
            else: # Depth is zero
                return (-1, self.score_position(self.redCoin))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)

            # if(len(self.get_valid_locations()) == 0):
            for col in valid_locations:
                row = self.get_next_open_row(col)

        # for col in valid_locations:
        #     row = self.get_next_open_row(col)
                self.drop_piece(yellowI, yellowJ, self.redCoin)
                new_score = self.minimax(depth-1, alpha, beta, False, yellowI, yellowJ)[1]
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
                self.drop_piece(row, col, self.yellowCoin)
                new_score = self.minimax(depth-1, alpha, beta, True, yellowI, yellowJ)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def drop_piece(self, row, col, piece):
        if(piece == self.redCoin):
            if((self.board[row][col])["bg"] == "red" or (self.board[row][col])["bg"] == "yellow"):
                print("already clicked")
                self.playRed( row, col)
            else:
                (self.board[row][col])["bg"] = "red"
        else:
            (self.board[row][col])["bg"] = "yellow"
        (self.board[row][col]).pack()
        theWindow.update()

    def checkAcross(self, color): 
        #check for 4 across
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT-3):
                if (((self.board[row][col]) )["bg"] == color and 
                (self.board[row][col+1])["bg"]  == color and 
                (self.board[row][col+2])["bg"]  == color and
                (self.board[row][col+3])["bg"] == color):
                    print("across")
                    return True
                else:
                    return False

    def checkUpAndDown(self, color): 
        #check for 4 up and down
        for row in range (ROW_COUNT-3):
            for col in range (COLUMN_COUNT):
                if (((self.board[row][col]))["bg"] == color   and 
                (self.board[row+1][col])["bg"] == color and
                (self.board[row+2][col])["bg"] == color and
                (self.board[row+3][col])["bg"] == color):
                    print("up and down")
                    return True
                else:
                    return False

    def checkUpwardDiagonal(self, color): 
        #check upward diagonal
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT-3):
                if (((self.board[row][col]))["bg"] == color and 
                (self.board[row-1][col+1])["bg"] == color and
                (self.board[row-2][col+2])["bg"] == color and
                (self.board[row-3][col+3])["bg"] == color):
                    print("upward diagonal")
                    return True
                else:
                    return False

    def checkDownwardDiagonal(self, color): 
        #check downward diagonal
        for row in range (ROW_COUNT-3):
            for col in range (COLUMN_COUNT-3):
                if (((self.board[row][col]))["bg"] == color and 
                (self.board[row+1][col+1])["bg"] == color and
                (self.board[row+2][col+2])["bg"] == color and
                (self.board[row+3][col+3])["bg"] == color):
                    print("downward diagonal")
                    return True
                else:
                    return False


    def isWinner(self, color):
        if(self.checkAcross(color) or
            self.checkUpAndDown(color) or
            self.checkUpwardDiagonal(color) or    
            self.checkDownwardDiagonal(color)):
            print(color + " wins")
            return True
        else:
            return False
                
    def playYellow(self, i, j):
        self.drop_piece(i, j, self.yellowCoin)
        self.turn = self.redCoin
        print("Reds turn")

    def playRed(self, yellowI, yellowJ):
        col, minimax_score = self.minimax(5, -math.inf, math.inf, True, yellowI, yellowJ)
        if(col == -1):
            return
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, self.redCoin)

        self.turn = self.yellowCoin
        print("Yellows turn")

    def playGame(self, i, j):
        # self.playYellow(i,j)
        # if(self.isWinner((self.board[i][j])["bg"])):
        #     return
        self.playRed(i, j)
        if(self.isWinner((self.board[i][j])["bg"])):
            return

    def initialize_board(self):
        self.board = [[0 for x in range(ROW_COUNT)] for y in range(COLUMN_COUNT)] 

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
                self.board[i][j]= myButton
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