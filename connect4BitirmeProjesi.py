from ctypes import sizeof
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


def insertYellowDisc(buttonParam):
    buttonParam['bg'] = "yellow"


def insertRedDisc(buttonParam):
    buttonParam['bg'] = "red"


def switchTurn(myTurn):
    if myTurn == yellowCoin:
        switchedTurn = redCoin
    else:
        switchedTurn = yellowCoin
    return switchedTurn


def getClickedPosition(event, frame):
    print(frame["bg"])
    # Here retrieving the size of the parent
    # widget relative to master widget
    x = abs(event.x_root - frame.winfo_rootx())
    y = abs(event.y_root - frame.winfo_rooty())
    
    # Here grid_location() method is used to
    # retrieve the relative position on the
    # parent widget
    z = frame.grid_location(x, y)

    # printing position
    print(z)
    return z

class App:
    table = {}

    def __init__(self, myWindow, myTurn) -> None:
        
        for i in range(6):
            for j in range(7):
                key = (i, j)
                theFrame = Frame(master=myWindow, relief=FLAT, borderwidth=5, bg="blue")
                theFrame.grid(row=i, column=j, padx=1, pady=1)
                theWindow.update()
                myButton = Button(master=theFrame, width=5, height=5, text=str(i) + "," + str(j)) 

                myButton.bind("<Button-1>", lambda event:getClickedPosition(event, theFrame))
                # print(str(theFrame.winfo_rootx()) + "," + str(theFrame.winfo_rootx()))
                myButton.pack()
                self.table[key]= myButton
                


     
    def playGame(self, whoseTurn, myButton):
        
        if whoseTurn == yellowCoin:
            myButton['command'] = lambda theButton=myButton: insertYellowDisc(theButton)
        elif whoseTurn == redCoin:
            myButton['command'] = lambda theButton=myButton: insertRedDisc(theButton)
        else:
            print("Error")
        whoseTurn = switchTurn(whoseTurn)


if __name__ == "__main__":
    theWindow = Tk()

    # Setting the title of the window
    theWindow.title("Connect 4")

    # Setting the geometry i.e Dimensions
    theWindow.geometry('1000x1000')

    theWindow['bg'] = "blue"

    # Calling our App
    menu = Menu()

    yellowCoin = 0
    redCoin = 1
    turn = yellowCoin

    # Calling our App
    app = App(theWindow, turn)
    for i in range(42):
        key = (1, 2)
        app.playGame(turn, app.table[key])

    # to run infinitely
    theWindow.mainloop()
