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
        self.topicFrame = self.upperFrame = self.makeTopicFrame()
        self.noteFrame = self.lowerFrame = self.makeNoteFrame()
        self.packFrames()

        self.makeReturnFrame()

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
    """                          Topic Frame methods                         """
    """ -------------------------------------------------------------------- """

    def createNoteLabel(self, text):
        """ Creates a label with the given text to be added to a DNDList. """

        args = {"wraplength": self.defaultWidth - 200, "relief": RAISED,
                "borderwidth": 2}
        label = Label(text=text, **args)

        return label

    def initializeTopicGUI(self, topic):
        """ Initialize the GUI components related to the given topic. """

        topic['line'] = self.newTopicLine(topic)
        topic['frame'], topic['dndlist'] = self.newTopicFrame(topic)
        self.menu.addToTopicLists(topic)

    def makeTopicFrame(self):
        """ Make the topic frame, including a DNDList to hold topic lines. """

        topicFrame = Frame(self.root)
        self.topicList = dndlist.DNDList(topicFrame, self.defaultWidth,
                                         self.defaultHeight - 200)

        return topicFrame

    def newTopicFrame(self, topic):
        """ Creates a new dndlist for the given topic and populates it with the
            topic's notes (if any). Returns a tuple containing the parent frame
            for the DNDList and the DNDList itself. """

        frame = Frame(self.root)
        labels = [self.createNoteLabel(n) for n in topic['notes']]
        dndl = dndlist.DNDList(frame, self.defaultWidth,
                               self.defaultHeight - 200, items=labels)

        return (frame, dndl)

    def newTopicLine(self, topic):
        """ Creates a new line for the given topic, adds it to the dndlist of 
            topics, and returns it. """

        line = TopicLine(topic, self.outliner, width=(self.defaultWidth - 100),
                         height=30, relief=RAISED, borderwidth=2)
        self.topicList.addItem(line)
        return line

    def viewTopic(self, topic):
        """ Display the notes that are part of the topic. """

        self.unpackFrames()
        self.upperFrame = topic['frame']
        self.lowerFrame = self.returnFrame
        self.packFrames()

    def updateTopicGUI(self, topic):
        """ Update all GUI components relating to the given topic. """

        topic['line'].updateLabel()

    def addNoteToGUI(self, topic, note):
        """ Add note to the DNDList of the given topic. """

        topic['dndlist'].addItem(self.createNoteLabel(note))
        self.updateTopicGUI(topic)

    """ -------------------------------------------------------------------- """
    """                          Note Frame methods                          """
    """ -------------------------------------------------------------------- """

    def makeNoteFrame(self):
        """ Make and deploy the note frame. """

        noteFrame = Frame(self.root, height=60, relief=RAISED, borderwidth=2)

        self.noteText = StringVar()

        noteLabelArgs = {'textvariable': self.noteText,
                         'height': 5, 'width': 80, 'justify': LEFT,
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

        self.returnFrame = Frame(self.root, relief=RAISED, borderwidth=2)
        self.returnButton = Button(self.returnFrame,
                                   text="Return to essay view",
                                   command=self.returnToMain)
        self.returnButton.pack()

    def returnToMain(self):
        """ Return to the main (essay) view. """

        self.unpackFrames()
        self.upperFrame = self.topicFrame 
        self.lowerFrame = self.noteFrame
        self.packFrames()
