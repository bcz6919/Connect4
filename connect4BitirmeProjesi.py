
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


table = {}
movesDict = {}


def switchTurn(myTurn, i, j):
    if myTurn == yellowCoin:
        switchedTurn = redCoin
    else:
        (table[i,j])["bg"] = "red"
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

def whichButton(i, j, buttonParam):
    movesDict[0,0] = buttonParam
    if(turn == yellowCoin):
        (table[i,j])["bg"] = "yellow"
    else:
        (table[i,j])["bg"] = "red"
    switchTurn(turn, i, j)

class App:

    def __init__(self, myWindow, myTurn) -> None:
        for i in range(0,6):
            for j in range(0,6):
                key = (i, j)
                theFrame = Frame(master=myWindow, relief=FLAT, borderwidth=5, bg="blue")
                theFrame.grid(row=i, column=j, padx=1, pady=1)

                if(i == 0):
                    myButton = Button(master=theFrame, width=1, height=1, text=str(j)) 
                    myButton["command"] = lambda k=i, m=j , buttonParam = myButton: whichButton(k, m, buttonParam)
                    # myButton.bind("<Button-1>", playGame)
                    myButton.pack()
                else:
                    myButton = Button(master=theFrame, width=5, height=5, text=str(i-1) + "," + str(j), padx=5, pady=5)
                    myButton.pack()

                table[key]= myButton
                theWindow.update()
                

if __name__ == "__main__":
    theWindow = Tk()

    # Setting the title of the window
    theWindow.title("Connect 4")

    # Setting the geometry i.e Dimensions
    theWindow.geometry('800x800')

    theWindow['bg'] = "blue"

    # Calling our App
    menu = Menu()

    yellowCoin = 0
    redCoin = 1
    turn = yellowCoin

    action = Button(theWindow, text="clicked")

    # Calling our App
    app = App(theWindow, turn)


    # to run infinitely
    theWindow.mainloop()
