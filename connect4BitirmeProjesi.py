import numpy
from tkinter import *
root = Tk()
myCanvas = Canvas(root, bg="blue", width=400, height=400)
myCanvas.pack()
def onObjectClick(event):                  
    print ("Clicked x,y:" + str(event.x) + "," + str(event.y))
    print(" Widget: " + str(event.widget) + "Closest:" + str(event.widget.find_closest(event.x, event.y))) 
    myCanvas.configure(bg="#f20")

def create_circle(x, y, r, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,outline="#fb0", fill="#fb0", tags=("clickable"))

dict = {}
for x in range(7):
    for y in range(6):
        myCircle = create_circle(30+50*x, 100+50*y, 20, myCanvas)
        myCanvas.tag_bind(myCircle, "<Button-1>", onObjectClick) 
        myCanvas.pack()
        key = (x,y)
        dict[key] = True
"""
print(dict)


item_type = myCanvas.type(myCircle)
if item_type == "rectangle":
    print("rectangle")
else:
    print("circle")
"""
root.mainloop()