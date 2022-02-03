from tkinter import *
import time
import math
import random
import copy

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
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += self.redCoin

        return score

    def score_position(self, board, piece):
        score = 0
        center_array = []
        ## Score center column
        for row in range(int(ROW_COUNT)):
            for col in range(int(COLUMN_COUNT / 2)):
                center_array.append(board[row][col])

        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        row_array = []
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                row_array.append(board[row][col])

            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            # col_array = [Button(i) for i in list(self.board[:][c])]
            col_array = []
            for i in range(0, ROW_COUNT):
                for j in range(0, int(COLUMN_COUNT / self.redCoin)):
                    col_array.append(board[i][j])
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)
        # score = random.random()
        return score

    def is_valid_location(self, board, row, col):
        return board[row][col] == 0

    def get_valid_locations(self, board):
        valid_locations = []
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                empty = board[r][c] == 0 
                key = (r, c)
                if(r != 0):
                    if(empty and (board[r-1][c]) != 0):
                        valid_locations.append(key)
                else:
                    if(empty and (board[0][c]) == 0):
                        valid_locations.append(key)

        return valid_locations
        
    def is_terminal_node(self, board):
        return self.winning_move(board, self.yellowCoin) or self.winning_move(board, self.redCoin)  or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        # print("depth: " + str(depth), end =" ")
        # print("is_terminal: " + str(is_terminal))
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.redCoin):
                    # print("******************")
                    # print("redCoin isWinner About to return: ")
                    # print(str(-1) +" "+ str(-1)+" "+ str(-100000000000000))
                    # print("******************")
                    return (-1, -1, -100000000000000)
                elif self.winning_move(board, self.yellowCoin):
                    # print("******************")
                    # print("yellowCoin isWinner About to return: ") 
                    # print(str(-1) +" "+ str(-1)+" "+ str(100000000000000))
                    # print("******************")
                    return (-1, -1, 10000000000000)
                else:  # Game is over, no more valid moves
                    # print("******************")
                    # print("Game is over About to return: " +  str(-1) +" "+ str(-1)+" "+ str(0))
                    # print("******************")
                    return (-1, -1, 0)
            else:  # Depth is zero
                # print("******************")
                # print("Depth is zero About to return score_position: ")
                # print(str(-1) +" "+ str(-1)+" "+ str(self.score_position(board, self.redCoin)))
                # print("******************")
                return (-1, -1, self.score_position(board, self.redCoin))
        if maximizingPlayer:
            # print("------------------")
            # print("maximizingPlayer: ")
            value = -math.inf
            # valid_locations = self.get_valid_locations(board)
            validRowCol = random.choice(valid_locations)
            row = validRowCol[0]
            column = validRowCol[1]
            for location in valid_locations:
                # print("location: " + str(location), end =" ")
                col=location[1]
                r = location[0]
                b_copy = copy.deepcopy(board)
                self.drop_piece(b_copy, r, col, self.redCoin)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[2]
                if new_score > value:
                    value = new_score
                    row = r
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            # print("------------------")
            # print("MAX About to return: " +  str(row) +" "+ str(column)+" "+ str(value))
            # print("------------------")
            return row, column, value

        else:  # Minimizing player
            # print("------------------")
            # print("minimizingPlayer: ")
            value = math.inf
            # valid_locations = self.get_valid_locations(board)
            # column = random.choice(valid_locations)
            validRowCol = random.choice(valid_locations)
            row = validRowCol[0]
            column = validRowCol[1]
            for location in valid_locations:
                # print("location: " + str(location), end =" ")
                col = location[1]
                r = location[0]
                b_copy = copy.deepcopy(board)
                self.drop_piece(b_copy, r, col, self.yellowCoin)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[2]
                if new_score < value:
                    value = new_score
                    row = r
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            # print("------------------")
            # print("MIN About to return: " +  str(row) +" "+ str(column)+" "+ str(value))
            # print("------------------")
            return row, column, value

    def drop_piece(self, myBoard, row, col, piece):
        if(self.is_valid_location(myBoard, row, col)):
            if (piece == self.redCoin):
                (myBoard[row][col]) = self.redCoin
                # print("drop redCoin")
                self.turn = self.yellowCoin
            else:
                (myBoard[row][col]) = self.yellowCoin
                # print("drop yellowCoin")
                self.turn = self.redCoin

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def playYellow(self, i, j):
        self.drop_piece(self.boardPieces, i, j, self.yellowCoin)
        print("YELLOW PLAYED")
        self.boardButtons[i][j]["bg"] = "yellow"
        theWindow.update()
        self.turn = self.redCoin
        print("Reds turn")

    def locationInLocation(self, row, col):
        valid_locations = self.get_valid_locations(self.boardPieces)
        exist = False
        for location in valid_locations:
            # print("location: " + str(location), end =" ")
            if(col != location[1] and row != location[0]):
                exist = False
            else:
                exist = True
                break

        return exist

    def playRed(self):
        # boardCopy = self.boardPieces[:]
        boardCopy = copy.deepcopy(self.boardPieces)
 
        depth = 7
        row, col, minimax_score = self.minimax(boardCopy, depth, -math.inf, math.inf, True)

        if (col == -1):
            return
            
        exist = self.locationInLocation(row, col)
        if(not exist):
            # self.playRed()
            pass
        else:
            self.drop_piece(self.boardPieces, row, col, self.redCoin)
            print("RED PLAYED " + str(row) + "," + str(col))
            self.boardButtons[row][col]["bg"] = "red"
            theWindow.update()
            self.turn = self.yellowCoin
            print("Yellows turn")

    def playGame(self, i, j):
        self.playYellow(i, j)
        if (self.winning_move(self.boardPieces, self.boardPieces[i][j])):
            print ("yellow wins")
            return
        self.playRed()
        if (self.winning_move(self.boardPieces, self.boardPieces[i][j])):
            print ("red wins")
            return

    def initialize_board(self):
        self.boardPieces = [[0 for y in range(COLUMN_COUNT)] for x in range(ROW_COUNT)]
        # self.boardPieces = self.boardPieces [::-1]
        self.boardButtons = [[0 for y in range(COLUMN_COUNT)] for x in range(ROW_COUNT)]


    def __init__(self, myWindow) -> None:
        # self.board = [[0]*COLUMN_COUNT]*ROW_COUNT
        self.initialize_board()
        for i in range(0, ROW_COUNT):
            for j in range(0, COLUMN_COUNT):
                theFrame = Frame(master=myWindow, relief=FLAT, borderwidth=5, bg="blue")
                theFrame.grid(row=i, column=j, padx=1, pady=1)
                myButton = Button(master=theFrame, width=5, height=5, text=str(i) + "," + str(j), padx=5, pady=5)
                myButton["command"] = lambda k=i, m=j, buttonParam=myButton: self.playGame(k, m)
                myButton.pack()
                self.boardButtons[i][j] = myButton

                theWindow.update()


if __name__ == "__main__":
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    theWindow = Tk()
    theWindow.title("Connect 4")
    theWindow.geometry('460x700')
    theWindow['bg'] = "blue"
    # Calling our App
    app = App(theWindow)
    # to run infinitely
    theWindow.mainloop()