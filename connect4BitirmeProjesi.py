from tkinter import *
import math
import random

PLAYER_PIECE = 0
AI_PIECE = 1

EMPTY = 0

WINDOW_LENGTH = 4


class Position:
    def __init__(self, i, j):
        value = EMPTY
        theFrame = Frame(relief=FLAT, borderwidth=5, bg="blue")
        theFrame.grid(row=i, column=j, padx=1, pady=1)
        myButton = Button(master=theFrame, width=5, height=5, padx=5, pady=5, text=str(i) + "," + str(j) + "\nvalue: " + str(value))
        myButton["command"] = lambda k=i, m=j, buttonParam=myButton: App.playGameNew(k, m)
        myButton.pack()


class App:
    yellowCoin = 0
    redCoin = 1
    turn = yellowCoin
    board = []
    def playGameNew(self, i, j):
        # self.playYellow(i,j)
        # if(self.isWinner((self.board[i][j])["bg"])):
        #     return
        App.playRed(i, j)
        if (App.isWinner((App.board[i][j])["bg"])):
            return

    def playRed(self, i, j):
        print("Reds turn")
        col, minimax_score = self.minimax(5, -math.inf, math.inf, True)
        if(col == -1):
            return
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, self.redCoin)
        if(self.isWinner((self.board[i][j])["bg"])):
            return
        self.turn = self.yellowCoin
    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(board, col):
        return board[ROW_COUNT-1][col] == 0

    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    # def print_board(board):
    #     print(np.flip(board, 0))

    def winning_move(board, piece):
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

    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score

    def is_terminal_node(board):
        return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, AI_PIECE):
                    return (None, 100000000000000)
                elif winning_move(board, PLAYER_PIECE):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, score_position(board, AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_PIECE)
                new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
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
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def playGame(self, i, j):
        # self.playYellow(i,j)
        # if(self.isWinner((self.board[i][j])["bg"])):
        #     return
        self.playRed(i, j)
        if (self.isWinner(self.redCoin)):
            return

    def initialize_board(self):
        pos = Position(ROW_COUNT, COLUMN_COUNT)
        self.board = [[pos]*COLUMN_COUNT]*ROW_COUNT
        # self.board = []
        # for i in range(ROW_COUNT):
        #     for j in range(COLUMN_COUNT):
        #         self.board.append(pos)

        # self.board = [[Position for x in range(ROW_COUNT)] for y in range(COLUMN_COUNT)]

    def __init__(self, myWindow) -> None:
        # self.board = [[0]*COLUMN_COUNT]*ROW_COUNT
        self.initialize_board()
        for i in range(0, ROW_COUNT):
            for j in range(0, COLUMN_COUNT):
                position = Position(i, j)
                self.board[i][j] = position
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