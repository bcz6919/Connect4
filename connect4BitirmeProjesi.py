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

    def score_position(self, board, piece):
        score = 0
        center_array = []
        ## Score center column
        for row in range(int(ROW_COUNT)):
            for col in range(int(COLUMN_COUNT / 2)):
                center_array.append(board[row][col])

        # center_array = [Button(i) for i in list(self.board[:][ COLUMN_COUNT//self.redCoin])]
        # center_count = center_array.count(piece)
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

    def is_valid_location_color(self, board, row, col):
        return board[row][col]["bg"] != "yellow" and board[row][col]["bg"] != "red"

    # def get_valid_locations(self, board):
    #     valid_locations = []

    #     row = 0
    #     column2 = 0
    #     while row < ROW_COUNT:
    #         while column2 < COLUMN_COUNT:
    #             isValid = self.is_valid_location(board, row, column2)
    #             prevValid = True
    #         #Bu aşağıdaki koşulda tümünü sağlamıyor. Bu seferde ilk başta 0'lar olduğu için içeri girmiyor. Hiç 0 kalmadıysa buna girme dememiz lazım
    #             if(any (0 in sublist for sublist in board)):
    #                 if (row != 0):
    #                     print(board)
    #                     prevValid = (valid_locations[row - 1][column2] != 0)
    #                 if isValid and prevValid:
    #                     key = (row, column2)
    #                     valid_locations.append(key)
    #                 else:
    #                     upperRow = row
    #                     while upperRow < ROW_COUNT:
    #                         isValid = self.is_valid_location(board, upperRow, column2)
    #                         prevValid = True
    #                         if (row != 0):
    #                             prevValid = valid_locations[row - 1][column2] != 0
    #                         if isValid and prevValid:
    #                             key = (upperRow, column2)
    #                             valid_locations.append(key)
    #                             break
    #                         else:
    #                             upperRow += 1
    #                 column2 += 1

    #         if isValid:
    #             break
    #         else:
    #             column2 = 0
    #             row += 1

    #     return valid_locations
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
        return self.isWinner(board, self.yellowCoin) or self.isWinner(board, self.redCoin)  or len(self.get_valid_locations(board)) == 0

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] != self.yellowCoin and board[r][col] != self.redCoin:
                return r

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.isWinner(board, self.redCoin):
                    return (-1, -1, -100000000000000)
                elif self.isWinner(board, self.yellowCoin):
                    return (-1, -1, 10000000000000)
                else:  # Game is over, no more valid moves
                    return (-1, -1, 0)
            else:  # Depth is zero
                return (-1, -1, self.score_position(board, self.redCoin))
        if maximizingPlayer:
            value = -math.inf
            column = 0
            # valid_locations = self.get_valid_locations(board)
            validRowCol = random.choice(valid_locations)
            row = validRowCol[0]
            column = validRowCol[1]
            for location in valid_locations:
                col=location[1]
                row = location[0]
                # row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.redCoin)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[2]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return row, column, value

        else:  # Minimizing player
            value = math.inf
            # valid_locations = self.get_valid_locations(board)
            # column = random.choice(valid_locations)
            validRowCol = random.choice(valid_locations)
            row = validRowCol[0]
            column = validRowCol[1]
            for location in valid_locations:
                col = location[1]
                row = location[0]
                # row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.yellowCoin)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[2]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return row, column, value

    def drop_piece(self, board, row, col, piece):
        if(self.is_valid_location(board, row, col)):
            if (piece == self.redCoin):
                (board[row][col]) = self.redCoin
                self.turn = self.yellowCoin
            else:
                (board[row][col]) = self.yellowCoin
                self.turn = self.redCoin

    def checkAcross(self, board, color):
        # check for 4 across
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                if (((board[row][col])) == color and
                        (board[row][col + 1]) == color and
                        (board[row][col + 2]) == color and
                        (board[row][col + 3]) == color):
                    print("across")
                    return True
                else:
                    return False

    def checkUpAndDown(self, board, color):
        # check for 4 up and down
        for row in range(ROW_COUNT - 3):
            for col in range(COLUMN_COUNT):
                if (((board[row][col])) == color and
                        (board[row + 1][col]) == color and
                        (board[row + 2][col]) == color and
                        (board[row + 3][col]) == color):
                    print("up and down")
                    return True
                else:
                    return False

    def checkUpwardDiagonal(self, board, color):
        # check upward diagonal
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                if (((board[row][col])) == color and
                        (board[row - 1][col + 1]) == color and
                        (board[row - 2][col + 2]) == color and
                        (board[row - 3][col + 3]) == color):
                    print("upward diagonal")
                    return True
                else:
                    return False

    def checkDownwardDiagonal(self, board, color):
        # check downward diagonal
        for row in range(ROW_COUNT - 3):
            for col in range(COLUMN_COUNT - 3):
                if (((board[row][col])) == color and
                        (board[row + 1][col + 1]) == color and
                        (board[row + 2][col + 2]) == color and
                        (board[row + 3][col + 3]) == color):
                    print("downward diagonal")
                    return True
                else:
                    return False

    def isWinner(self, board, piece):
        if (self.checkAcross(board, piece) or
                self.checkUpAndDown(board, piece) or
                self.checkUpwardDiagonal(board, piece) or
                self.checkDownwardDiagonal(board, piece)):
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
        boardCopy = self.boardPieces.copy()
        row, col, minimax_score = self.minimax(boardCopy, 5, -math.inf, math.inf, True)
        if (col == -1):
            return
        # if self.is_valid_location(self.boardPieces, row, col):
        # row = self.get_next_open_row(self.boardPieces, col)
        self.drop_piece(self.boardPieces, row, col, self.redCoin)
        self.boardButtons[row][col]["bg"] = "red"
        theWindow.update()
        self.turn = self.yellowCoin
        print("Yellows turn")

    def playGame(self, i, j):
        self.playYellow(i, j)
        if (self.isWinner(self.boardPieces, self.boardPieces[i][j])):
            return
        self.playRed()
        if (self.isWinner(self.boardPieces, self.boardPieces[i][j])):
            return

    def initialize_board(self):
        self.boardPieces = [[0 for x in range(ROW_COUNT)] for y in range(COLUMN_COUNT)]
        self.boardButtons = [[0 for x in range(ROW_COUNT)] for y in range(COLUMN_COUNT)]

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
    COLUMN_COUNT = 6
    theWindow = Tk()
    theWindow.title("Connect 4")
    theWindow.geometry('500x700')
    theWindow['bg'] = "blue"
    # Calling our App
    app = App(theWindow)
    # to run infinitely
    theWindow.mainloop()