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


def insertYellowDisc(buttonParam, image):
    buttonParam['bg'] = "yellow"


def insertDisc(buttonParam, image):
    #buttonParam['bg'] = "red"
    buttonParam['image'] = image
    buttonParam['width'] = 70
    buttonParam['height'] = 70
    buttonParam.pack()


def switchTurn(myTurn):
    if myTurn == 0:
        switchedTurn = 1
    else:
        switchedTurn = 0
    return switchedTurn


class App:

    def __init__(self, myWindow, myTurn) -> None:
        global img
        for i in range(6):
            for j in range(7):
                frame = Frame(master=myWindow, relief=FLAT, borderwidth=3, width=10, height=10)
                frame.grid(row=i, column=j, padx=1, pady=1)
                myButton = Button(master=frame, width=7, height=7, bg='blue')

                if myTurn == 0:
                    img = PhotoImage(file=r"C:\Connect4\yellow.png")
                    myButton['command'] = lambda theButton=myButton: insertDisc(theButton, img)
                    myTurn = 1
                elif myTurn == 1:
                    img = PhotoImage(file=r"C:\Connect4\red.png")
                    myButton['command'] = lambda theButton=myButton: insertDisc(theButton, img)
                    myTurn = 0
                else:
                    print("Error")

                myButton.pack()



if __name__ == "__main__":
    window = Tk()

    # Setting the title of the window
    window.title("Button State App")

    # Setting the geometry i.e Dimensions
    window.geometry('1000x1000')

    window["bg"] = "blue"

    # Calling our App
    menu = Menu()

    yellowCoin = 0
    redCoin = 1
    turn = yellowCoin

    # Calling our App
    app = App(window, turn)

    # to run infinitely
    window.mainloop()
