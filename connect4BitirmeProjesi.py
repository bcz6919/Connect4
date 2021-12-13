
from tkinter import *
class Menu:
    def addMenu(self):
        self.menubar = Menu(theWindow)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.donothing)
        self.filemenu.add_command(label="Open", command=self.donothing)
        self.filemenu.add_command(label="Save", command=self.donothing)
        self.filemenu.add_command(label="Save as...", command=self.donothing)
        self.filemenu.add_command(label="Close", command=self.donothing)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command=theWindow.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo", command=self.donothing)

        self.editmenu.add_separator()

        self.editmenu.add_command(label="Cut", command=self.donothing)
        self.editmenu.add_command(label="Copy", command=self.donothing)
        self.editmenu.add_command(label="Paste", command=self.donothing)
        self.editmenu.add_command(label="Delete", command=self.donothing)
        self.editmenu.add_command(label="Select All", command=self.donothing)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.donothing)
        self.helpmenu.add_command(label="About...", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.window.config(menu=self.menubar)

    def donothing(self):
        filewin = Toplevel(theWindow)
        button = Button(filewin, text="Do nothing button")
        button.pack()






# def getClickedPosition(event, frame):
#     # Here retrieving the size of the parent
#     # widget relative to master widget
#     x = abs(event.x_root - frame.winfo_rootx())
#     y = abs(event.y_root - frame.winfo_rooty())
    
#     # Here grid_location() method is used to
#     # retrieve the relative position on the
#     # parent widget
#     z = frame.grid_location(x, y)

#     # printing position
#     print(z)
#     return z



class App:
    yellowCoin = 0
    redCoin = 1
    turn = yellowCoin
    board = {}
    movesDict = {}
    moveCount = -1
    
    def isWinner(self, color):
        #check for 4 across
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT-3):
                if ((self.board[row,col] )["bg"] == color and 
                (self.board[row,col+1])["bg"]  == color and 
                (self.board[row,col+2])["bg"]  == color and
                (self.board[row,col+3])["bg"] == color):
                    print("across")
                    return True

        #check for 4 up and down
        for row in range (ROW_COUNT-3):
            for col in range (COLUMN_COUNT):
                if ((self.board[row,col])["bg"] == color   and 
                (self.board[row+1,col])["bg"] == color and
                (self.board[row+2,col])["bg"] == color and
                (self.board[row+3,col])["bg"] == color):
                    print("up and down")
                    return True

        #check upward diagonal
        for row in range (ROW_COUNT):
            for col in range (COLUMN_COUNT-3):
                if ((self.board[row,col])["bg"] == color and 
                (self.board[row-1,col+1])["bg"] == color and
                (self.board[row-2,col+2])["bg"] == color and
                (self.board[row-3,col+3])["bg"] == color):
                    print("upward diagonal")
                    return True

        #check downward diagonal
        for row in range (ROW_COUNT-3):
            for col in range (COLUMN_COUNT-3):
                if ((self.board[row,col])["bg"] == color and 
                (self.board[row+1,col+1])["bg"] == color and
                (self.board[row+2,col+2])["bg"] == color and
                (self.board[row+3,col+3])["bg"] == color):
                    print("downward diagonal")
                    return True
                
    

    def playGame(self, i, j, buttonParam):
        self.movesDict[i,j] = (buttonParam, self.turn)
        if(self.turn == self.yellowCoin):
            (self.board[i,j])["bg"] = "yellow"
            self.turn = self.redCoin
        else:
            (self.board[i,j])["bg"] = "red"
            self.turn = self.yellowCoin
        win = self.isWinner((self.board[i,j])["bg"])
        self.moveCount = self.moveCount + 1

    def __init__(self, myWindow) -> None:

        for i in range(0,ROW_COUNT):
            for j in range(0,COLUMN_COUNT):
                key = (i, j)
                theFrame = Frame(master=myWindow, relief=FLAT, borderwidth=5, bg="blue")
                theFrame.grid(row=i, column=j, padx=1, pady=1)

                myButton = Button(master=theFrame, width=5, height=5, text=str(i) + "," + str(j), padx=5, pady=5)
                myButton["command"] = lambda k=i, m=j , buttonParam = myButton: self.playGame(k, m, buttonParam)
   
                myButton.pack()
                self.board[key]= myButton
                theWindow.update()
                

if __name__ == "__main__":
    COLUMN_COUNT = 7
    ROW_COUNT = 6
    tablo = {}
    theWindow = Tk()
    # Setting the title of the window
    theWindow.title("Connect 4")
    # Setting the geometry i.e Dimensions
    theWindow.geometry('800x800')
    theWindow['bg'] = "blue"

    # Calling our App
    menu = Menu()
    # Calling our App
    app = App(theWindow)


    # to run infinitely
    theWindow.mainloop()
