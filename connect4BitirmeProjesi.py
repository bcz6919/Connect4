from tkinter import *


class Menu:
    def addMenu(self):
        self.menubar = Menu(window)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.donothing)
        self.filemenu.add_command(label="Open", command=self.donothing)
        self.filemenu.add_command(label="Save", command=self.donothing)
        self.filemenu.add_command(label="Save as...", command=self.donothing)
        self.filemenu.add_command(label="Close", command=self.donothing)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command=window.quit)
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
        filewin = Toplevel(window)
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

class Move:
    theButton = Button(width=5, height=5)
    theTurn = 0

    def __init__(self, myButton, myTurn): 
        self.theButton = myButton
        self.theTurn = myTurn



class App:

    def play(self, move):
        
        if move.theTurn == yellowCoin:
            move.theButton['command'] = lambda theButton=move.theButton: insertYellowDisc(theButton)
        elif move.theTurn == redCoin:
            move.theButton['command'] = lambda theButton=move.theButton: insertRedDisc(theButton)
        else:
            print("Error")
        move.theButton.pack()
    def __init__(self, myWindow, myTurn) -> None:

        for i in range(6):
            for j in range(7):
                frame = Frame(master=myWindow, relief=FLAT, borderwidth=5, bg="blue")
                frame.grid(row=i, column=j, padx=1, pady=1)

                myButton = Button(master=frame, width=5, height=5)
                move = Move(myButton, myTurn)
                self.play(move)
                
                myTurn = switchTurn(myTurn)


if __name__ == "__main__":
    window = Tk()

    # Setting the title of the window
    window.title("Button State App")

    # Setting the geometry i.e Dimensions
    window.geometry('1000x1000')

    window['bg'] = "blue"

    # Calling our App
    menu = Menu()

    yellowCoin = 0
    redCoin = 1
    turn = yellowCoin

    # Calling our App
    app = App(window, turn)

    # to run infinitely
    window.mainloop()