from tkinter import *

class App:
    yellowCoin = 0
    redCoin = 1
    turn = yellowCoin
    board = {}

    def checkAcross(self, color): 
        #check for 4 across
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT-3):
                if ((self.board[row,col] )["bg"] == color and 
                (self.board[row,col+1])["bg"]  == color and 
                (self.board[row,col+2])["bg"]  == color and
                (self.board[row,col+3])["bg"] == color):
                    print("across")
                    return True

    def checkUpAndDown(self, color): 
        #check for 4 up and down
        for row in range (ROW_COUNT-3):
            for col in range (COLUMN_COUNT):
                if ((self.board[row,col])["bg"] == color   and 
                (self.board[row+1,col])["bg"] == color and
                (self.board[row+2,col])["bg"] == color and
                (self.board[row+3,col])["bg"] == color):
                    print("up and down")
                    return True

    def checkUpwardDiagonal(self, color): 
        #check upward diagonal
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT-3):
                if ((self.board[row,col])["bg"] == color and 
                (self.board[row-1,col+1])["bg"] == color and
                (self.board[row-2,col+2])["bg"] == color and
                (self.board[row-3,col+3])["bg"] == color):
                    print("upward diagonal")
                    return True

    def checkDownwardDiagonal(self, color): 
        #check downward diagonal
        for row in range (ROW_COUNT-3):
            for col in range (COLUMN_COUNT-3):
                if ((self.board[row,col])["bg"] == color and 
                (self.board[row+1,col+1])["bg"] == color and
                (self.board[row+2,col+2])["bg"] == color and
                (self.board[row+3,col+3])["bg"] == color):
                    print("downward diagonal")
                    return True


    def isWinner(self, color):
        if(self.checkAcross(color) or
            self.checkUpAndDown(color) or
            self.checkUpwardDiagonal(color) or
            self.checkDownwardDiagonal(color)):
         return True
        else:
            return False

                
    

    def playGame(self, i, j):
        if(self.turn == self.yellowCoin):
            (self.board[i,j])["bg"] = "yellow"
            self.turn = self.redCoin
        else:
            (self.board[i,j])["bg"] = "red"
            self.turn = self.yellowCoin

        win = self.isWinner((self.board[i,j])["bg"])
        if(win):
            print((self.board[i,j])["bg"] + " wins")
            return

    def __init__(self, myWindow) -> None:

        for i in range(0,ROW_COUNT):
            for j in range(0,COLUMN_COUNT):

                theFrame = Frame(master=myWindow, relief=FLAT, borderwidth=5, bg="blue")
                theFrame.grid(row=i, column=j, padx=1, pady=1)

                myButton = Button(master=theFrame, width=5, height=5, text=str(i) + "," + str(j), padx=5, pady=5)
                myButton["command"] = lambda k=i, m=j , buttonParam = myButton: self.playGame(k, m)
                myButton.pack()

                key = (i, j)
                self.board[key]= myButton
                theWindow.update()
               

if __name__ == "__main__":
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    theWindow = Tk()
    theWindow.title("Connect 4")
    theWindow.geometry('500x700')
    theWindow['bg'] = "blue"
    # Calling our App
    app = App(theWindow)
    # to run infinitely
    theWindow.mainloop()
