"""
 "  File: dndlist.py
 "  Written By: Gregory Owen
 "  Date: 03-02-2013 
 "  Last Modified: July 13, 2013
 "
 "  A drag-and-drop list widget. Currently only supports text-based label
 "  objects, but could be easily extended to support anything else that can be
 "  put onto a canvas by changing the type of widget in DNDNode.
""" 

from Tkinter import *

class DNDNode():

    def __init__(self, string, dndlist):
        """ Create a new DNDNode object containing a label with the given string
            that belongs to the given DNDList. """

        self.list = dndlist

        self.widget = Label(self.list.canvas, wraplength=500, text=string, 
                            relief=RAISED, borderwidth=2)

        self.window = self.list.canvas.create_window(self.list.center,
                                                     self.list.depth, 
                                                     window=self.widget,
                                                     anchor=N)

    def getY(self):
        """ Returns the y-coordinate of the top of the node's widget in the 
            coordinate system of the DNDList's canvas. """

        bbox = self.list.canvas.bbox(self.window)
        return bbox[1]

    def __lt__(self, other):
        """ Compares DNDNode objects based on their y-coordinate (as defined by
            getY(). Necessary for sorting the elements of a DNDList. """

        return self.getY() < other.getY()


class DNDList():

    def __init__(self, frame, width, height, items=None):
        """ Create a new DNDList object that fits into the given frame and has the
            specified width and height. If a list is passed as items, set the
            dndlist to contain the elements in items. """

        # The size of the offset, in pixels, between two adjacent items in the list
        self.OFFSET = 10

        self.width = width
        self.center = self.width/2
        self.height = height
        self.frame = Frame(frame, width=self.width, height=self.height)
        self.canvas = self.makeCanvas()
        self.depth = 0
        self.dragData = {"x":0, "y":0, "item":None}
        self.elements = {}

        self.frame.pack()

        self.getOrdered()

        if items is not None:
            for item in items:
                self.addItem(item)

    def addItem(self, item):
        """ Add a new entry to the list containing item. """

        node = DNDNode(string=item, dndlist=self)

        self.elements[node.window] = node

        # Bounding box for the node's window (used to get height)
        bbox = self.canvas.bbox(node.window)

        self.depth += self.OFFSET
        self.depth += (bbox[3] - bbox[1])

        # Bind drag and drop capabilities to the widget
        node.widget.bind("<Button-1>", self.onClick)
        node.widget.bind("<ButtonRelease-1>", self.onRelease)
        node.widget.bind("<B1-Motion>", self.onMotion)
        

    def makeCanvas(self):
        """ Initialize the canvas, including scrollbar. """

        canvas = Canvas(self.frame, width=self.width, height=self.height,
                        scrollregion=(0, 0, self.width, self.height))
        scroll = Scrollbar(self.frame, command=canvas.yview)
        canvas.config(yscrollcommand=scroll.set)
        canvas.pack(side=LEFT, fill="both", expand=True)
        scroll.pack(side=RIGHT, fill=Y)

        return canvas

    """ ------------------------------------------------------------------------- """
    """                         Pointer Coordinate method                         """
    """   Courtesy of Bryan Oakley, http://stackoverflow.com/questions/16640747   """
    """ ------------------------------------------------------------------------- """

    def getClickCoords(self):
        """ Translate the position of the mouse to canvas coordinates. Returns
            a tuple (x,y) of the resulting coordinates. """

        wx, wy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        x, y = self.frame.winfo_pointerxy()
        cx = self.canvas.canvasx(x-wx)
        cy = self.canvas.canvasy(y-wy)

        return (cx, cy)

    """ ------------------------------------------------------------------------- """
    """                           Click and Drag methods                          """
    """    Courtesy of Bryan Oakley, http://stackoverflow.com/questions/6740855   """
    """ ------------------------------------------------------------------------- """

    def onClick(self, event):
        """ Begin dragging an item. """
        
        x, y = self.getClickCoords()

        self.dragData["item"] = self.canvas.find_closest(x, y)[0]
        self.dragData["x"] = x
        self.dragData["y"] = y
        
    def onRelease(self, event):
        """ Finish dragging an item. """

        self.dragData["item"] = None
        self.dragData["x"] = 0
        self.dragData["y"] = 0

    def onMotion(self, event):
        """ Handle dragging an item. """

        x, y = self.getClickCoords()

        deltaX = x - self.dragData["x"]
        deltaY = y - self.dragData["y"]
        self.canvas.move(self.dragData["item"], deltaX, deltaY)
        self.dragData["x"] = x
        self.dragData["y"] = y

    def getOrdered(self):
        """ Returns the elements of the DNDList sorted by y-coordinate, with the
            top element first. This is an order nlogn operation, since the list
            does not maintain any state about the order of its elements. """

        nodes = [self.elements[id] for id in sorted(self.elements, 
                                                    key=self.elements.get)]
        return nodes

if __name__ == "__main__":
    """ Test the methods. """

    root = Tk()
    #frame = Frame(root)
    #frame.pack()
    list = DNDList(root, 700, 800)
    list.addItem("First")
    list.addItem("Second")
    list.addItem("Third")
    list.addItem("Really really really really really really really really really really really really really really really really really really really really really really really really long text.")

    list.getOrdered()

    """
    root2 = Tk()
    frame2 = Frame(root2)
    frame2.pack()
    list2 = DNDList(frame2, 700, 800, items=["Primero", "Segundo", "Tercero"])
    """

    root.mainloop()
    #root2.mainloop()
