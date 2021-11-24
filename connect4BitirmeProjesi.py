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


class App:

    def insertDisc(self, myButton, myDict, i, j, turn) -> None:
        myKey = (i, j)
        selected = myDict[myKey]

        if myButton['image'] is None:
            photo = PhotoImage(file=r".\yellow.png", width=5, height=5)

        else:
            photo = PhotoImage(file=r".\red.png", width=5, height=5)

        # myButton.__setattr__('image', photo)
        if turn == 0:
            myButton['bg'] = "yellow"
            turn = 1
        else:
            myButton['bg'] = "red"
            turn = 0
        myButton.pack()

    def __init__(self, window) -> None:
        window.geometry('1000x1000')
        turn = 0
        myDict = {}
        for i in range(6):
            for j in range(7):
                myKey = (i, j)
                frame = Frame(master=window, relief=FLAT, borderwidth=1)
                frame.grid(row=i, column=j, padx=1, pady=1)

                myButton = Button(master=frame, width=5, height=5)
                myButton['command'] = lambda theButton=myButton: self.insertDisc(theButton, myDict, i, j, turn)
                myDict[myKey] = myButton

                myButton.pack()


if __name__ == "__main__":
    window = Tk()

    # Setting the title of the window
    window.title("Button State App")

    # Setting the geometry i.e Dimensions
    window.geometry("400x250")

    # Calling our App
    menu = Menu()

    # Calling our App
    app = App(window)

    # to run infinitely
    window.mainloop()

