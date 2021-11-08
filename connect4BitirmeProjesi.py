
from tkinter import *

def addMenu():   
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_command(label="Save as...", command=donothing)
    filemenu.add_command(label="Close", command=donothing)

    filemenu.add_separator()

    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)

    editmenu.add_separator()

    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)
    editmenu.add_command(label="Select All", command=donothing)

    menubar.add_cascade(label="Edit", menu=editmenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)


def key(event):
    print ("pressed", repr(event.char))

def insertDisc():
    print("You have clicked Me...")
    click_btn = PhotoImage(file='yellow.png')
 
def donothing():
   filewin = Toplevel(window)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def callback(myButton):
    myButton.configure(bg="blue")
    

window = Tk()
addMenu()

window.geometry('1000x1000')
dict = {}
for i in range(6):
    for j in range(7):
        key = (i, j)
        frame = Frame(master=window, relief=FLAT, borderwidth=1)
        frame.grid(row=i, column=j, padx=1, pady=1)
        click_btn = PhotoImage(file='red_transparent.png')
        myButton = Button(master=frame, height=5, width=5)
        dict[key] = myButton
        myButton.bind("<Button-1>", callback(myButton))
        myButton.grid()

window.mainloop() 