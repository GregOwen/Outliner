"""
 "  File: outlinergui.py
 "  Written By: Gregory Owen
 "
 "  The GUI manager (view) for the Outliner
""" 

from Tkinter import *

from outlinermenu import OutlinerMenu
from outlinermodel import OutlinerModel
import dndlist

class TopicLine(Frame):
    """ A frame that contains a label, a reference to a topic, a button to add a
        note to that topic, and a button to view that topic. """

    def __init__(self, topic, outliner, **args):
        Frame.__init__(self, **args)

        self.topic = topic

        labelText = StringVar()
        label = Label(self, textvariable=labelText)
        labelText.set(self.getLabelText())
        topic['labelText'] = labelText
        label.pack(side=LEFT)

        viewButton = Button(self, text="View Topic")
        viewButton.config(command=(lambda o=outliner, t=topic: o.viewTopic(t)))
        viewButton.pack(side=RIGHT)

        addButton = Button(self, text="Add Note")
        addButton.config(command=(
                         lambda o=outliner, t=topic: o.addNoteToTopic(t)))
        addButton.pack(side=RIGHT)

    def getLabelText(self):
        """ Returns the text that should be displayed on this topic line. """

        endChar = '' if (len(self.topic['notes']) == 1) else 's'
        labelText = "%s:%d note%s" % (self.topic['name'],
                                      len(self.topic['notes']), 
                                      endChar)
        return labelText

    def updateLabel(self):
        """ Update the text displayed on this topic line's label. """
        
        self.topic['labelText'].set(self.getLabelText())


class OutlinerGUI:

    def __init__(self, master, outliner, model):

        self.root = master
        self.outliner = outliner
        self.model = model

        self.root.title("The Outliner, by Gregory Owen")
        self.defaultWidth = 700
        self.defaultHeight = 800

        geoString = str(self.defaultWidth) + "x" + str(self.defaultHeight)
        self.root.geometry(geoString)

        self.menu = OutlinerMenu(self.outliner, self.root) 
        self.essayFrame = self.upperFrame = self.makeEssayFrame()
        self.noteFrame = self.lowerFrame = self.makeNoteFrame()
        self.packFrames()

        self.makeReturnFrame()
        self.currTopic = None
        self.dragNote = None

    """ -------------------------------------------------------------------- """
    """                            General methods                           """
    """ -------------------------------------------------------------------- """

    def openGUI(self):
        """ Initialize the GUI from a previous project. """

        # Sort the topics by number
        sortedTopicNames = sorted(self.model.topics,
                                  key=(lambda name:
                                           self.model.topics[name]['number']))
        
        for name in sortedTopicNames:
            topic = self.model.topics[name]
            self.initializeTopicGUI(topic)

    def packFrames(self):
        """ Pack self.upperFrame above self.lowerFrame. """

        self.upperFrame.pack(side=TOP, fill=BOTH, expand=True)
        self.lowerFrame.pack(side=TOP, anchor=S, fill=X, expand=True)

    def unpackFrames(self):
        """ Unpack the current self.upperFrame and self.lowerFrame. """

        self.upperFrame.pack_forget()
        self.lowerFrame.pack_forget()

    """ -------------------------------------------------------------------- """
    """                          Essay Frame methods                         """
    """ -------------------------------------------------------------------- """

    def makeEssayFrame(self):
        """ Make the essay frame, including a DNDList to hold topic lines. """

        essayFrame = Frame(self.root)
        self.topicList = dndlist.DNDList(essayFrame, self.defaultWidth,
                                         self.defaultHeight - 200)

        return essayFrame

    """ -------------------------------------------------------------------- """
    """                          Topic Frame methods                         """
    """ -------------------------------------------------------------------- """

    def addNoteToGUI(self, topic, note):
        """ Add note to the DNDList of the given topic. """

        node = topic['dndlist'].addItem(self.createNoteLabel(note))
        node.widget.bind("<Button-1>", self.onClick, add='+')
        node.widget.bind("<B1-Motion>", self.onMotion, add='+')
        node.widget.bind("<ButtonRelease-1>", self.onRelease, add='+')

    def createNoteLabel(self, text):
        """ Create a label with the given text to be added to a DNDList. """

        args = {"wraplength": self.defaultWidth - 200, "relief": RAISED,
                "borderwidth": 2}
        label = Label(text=text, **args)

        return label

    def initializeTopicGUI(self, topic):
        """ Initialize the GUI components related to the given topic. """

        topic['line'] = self.newTopicLine(topic)
        self.newTopicFrame(topic)
        self.menu.addToTopicLists(topic)

    def newTopicFrame(self, topic):
        """ Create a new dndlist for the given topic and populate it with the
            topic's notes (if any). """

        frame = Frame(self.root)
        
        removeFrame = Frame(frame, width=self.defaultWidth, height=30,
                            relief=SOLID, borderwidth=2)
        removeLabel = Label(removeFrame,
                            text="Drag note here to remove from topic")

        removeLabel.pack()
        removeFrame.pack(side=TOP, fill=X)
        
        dndl = dndlist.DNDList(frame, self.defaultWidth, 
                               self.defaultHeight - 120)

        topic['frame'] = frame
        topic['rframe'] = removeFrame
        topic['dndlist'] = dndl
        
        for note in topic['notes']:
            self.addNoteToGUI(topic, note)

    def newTopicLine(self, topic):
        """ Create a new line for the given topic, add it to the dndlist of 
            topics, and return it. """

        line = TopicLine(topic, self.outliner, width=(self.defaultWidth - 100),
                         height=30, relief=RAISED, borderwidth=2)
        self.topicList.addItem(line)
        return line

    def onClick(self, event):
        """ When an item on the canvas is clicked, store that item's id. """

        x, y = self.currTopic['dndlist'].getClickCoords()
        self.dragNote = self.currTopic['dndlist'].canvas.find_closest(x, y)[0]

    def onMotion(self, event):
        """ Change the color of the text in the current topic's remove frame
            when an object is dragged into that frame. Assumes that the remove
            frame is located immediately above the canvas. """

        if self.dragNote is not None:
            x, y = self.currTopic['dndlist'].getClickCoords()
            label = self.currTopic['rframe'].winfo_children()[0]
            
            if y < 0 and label.cget('fg') != "red":                
                label.config(fg="red")
            if y > 0 and label.cget('fg') == "red":
                label.config(fg="black")

    def onRelease(self, event):
        """ When an item on the canvas is released, check if the mouse is over
            the remove from topic frame. If it is, remove the selected note from
            the topic. Assumes that the remove frame is located immediately
            above the canvas. """

        x, y = self.currTopic['dndlist'].getClickCoords()

        # if the mouse is currently in the remove frame
        if y < 0:
            self.removeNoteFromTopic(self.currTopic, self.dragNote)
            self.currTopic['rframe'].winfo_children()[0].config(fg="black")

        self.dragNote = None

    def removeNoteFromTopic(self, topic, noteid):
        """ Remove the note with the given id from the given topic. Push the
            text of the note onto the left of the note deque. """

        text = topic['dndlist'].getItem(noteid).widget.cget('text')

        topic['dndlist'].removeItem(noteid)
        topic['notes'].remove(text)

        self.model.notes.appendleft(text)
        self.updateTopicGUI(topic)
        self.displayNextNote()

    def updateTopicGUI(self, topic):
        """ Update all GUI components relating to the given topic. """

        topic['line'].updateLabel()

    def viewTopic(self, topic):
        """ Display the notes that are part of the topic. """

        self.currTopic = topic
        self.unpackFrames()
        self.upperFrame = topic['frame']
        self.lowerFrame = self.returnFrame
        self.packFrames()

    """ -------------------------------------------------------------------- """
    """                          Note Frame methods                          """
    """ -------------------------------------------------------------------- """

    def makeNoteFrame(self):
        """ Make and deploy the note frame. """

        noteFrame = Frame(self.root, height=60, relief=RAISED, borderwidth=2)

        self.noteText = StringVar()

        noteLabelArgs = {'textvariable': self.noteText,
                         'height': 6, 'width': 80, 'justify': LEFT,
                         'wraplength': self.defaultWidth - 100}
        self.noteLabel = Label(noteFrame, **noteLabelArgs)

        noNotes = "No notes. Open an existing project or create a new one to" +\
            " import notes."
        self.noteText.set(noNotes)

        self.noteLabel.pack(side=LEFT, expand=YES)

        nextButton = Button(noteFrame, text="Next") 
        nextButton.config(command=(lambda: self.outliner.nextNote()))
        nextButton.pack(side=TOP)

        prevButton = Button(noteFrame, text="Prev") 
        prevButton.config(command=(lambda: self.outliner.prevNote()))
        prevButton.pack(side=BOTTOM)

        return noteFrame

    def displayNextNote(self):
        """ Display the first note in the list. """

        if len(self.outliner.model.notes) > 0:
            self.noteText.set(self.outliner.model.notes[0])
        else:
            self.noteText.set("No more notes.")

    """ -------------------------------------------------------------------- """
    """                         Return Frame methods                         """
    """ -------------------------------------------------------------------- """

    def makeReturnFrame(self):
        """ Make the return frame, but do not deploy it. """

        self.returnFrame = Frame(self.root, height=30, relief=RAISED,
                                 borderwidth=2)
        self.returnButton = Button(self.returnFrame,
                                   text="Return to essay view",
                                   command=self.returnToMain)
        self.returnButton.pack()

    def returnToMain(self):
        """ Return to the main (essay) view. """

        self.currTopic = None
        self.unpackFrames()
        self.upperFrame = self.essayFrame 
        self.lowerFrame = self.noteFrame
        self.packFrames()
