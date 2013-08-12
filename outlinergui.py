"""
 "  File: outlinergui.py
 "  Written By: Gregory Owen
 "
 "  Description: The GUI manager for outliner
""" 

from Tkinter import *
from outlinermenu import OutlinerMenu

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

    def __init__(self, ol=None):

        self.outliner = ol
        self.root = self.outliner.root

        self.root.title("The Outliner, by Gregory Owen")
        self.defaultWidth = 700
        self.defaultHeight = 800

        geoString = str(self.defaultWidth) + "x" + str(self.defaultHeight)
        self.root.geometry(geoString)

        self.menu = OutlinerMenu(self.outliner) 
        self.topicFrame = self.upperFrame = self.makeTopicFrame()
        self.noteFrame = self.lowerFrame = self.makeNoteFrame()
        self.packFrames()

        self.makeReturnFrame()

    """ -------------------------------------------------------------------- """
    """                            General methods                           """
    """ -------------------------------------------------------------------- """

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

    def makeTopicFrame(self):
        """ Make the topic frame, including a DNDList to hold topic lines. """

        topicFrame = Frame(self.root)
        self.topicList = dndlist.DNDList(topicFrame, self.defaultWidth,
                                         self.defaultHeight - 100)

        return topicFrame

    def newTopicFrame(self, topic):
        """ Creates a new dndlist for the given topic and populates it with the
            topic's notes (if any). Returns a tuple containing the parent frame
            for the DNDList and the DNDList itself. """

        frame = Frame(self.root)
        labels = [self.createNoteLabel(n) for n in topic['notes']]
        dndl = dndlist.DNDList(frame, self.defaultWidth,
                               self.defaultHeight - 100, items=labels)

        return (frame, dndl)

    def newTopicLine(self, topic):
        """ Creates a new line for the given topic, adds it to the dndlist of 
            topics, and returns it. """

        line = TopicLine(topic, self.outliner, width=(self.defaultWidth - 100),
                         relief=RAISED, borderwidth=2)
        self.topicList.addItem(line)
        return line

    def topicAlreadyExists(self):
        """ Report to the user that there is already a topic with the name that
            they entered. """

        errorprompt = "I'm sorry, but a topic by that name already exists in" +\
" this outline.\nPlease select a different name."
        tkMessageBox.showerror("Error: Topic Already Exists", errorprompt)

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

        noteFrame = Frame(self.root, relief=RAISED, borderwidth=2)

        self.outliner.noteText = StringVar()
        self.noteLabel = Label(noteFrame, textvariable=self.outliner.noteText,
                height=5, width=80)

        noNotes = "No notes. Open an existing project or create a new one to" +\
            " import notes."
        self.outliner.noteText.set(noNotes)

        self.noteLabel.pack(side=BOTTOM, expand=YES)

        return noteFrame

    def displayNextNote(self):
        """ Display the next note in the list. """

        note = ""

        while (len(self.outliner.notes) > 0 and note.strip() == ""):
            note = self.outliner.notes.popleft()

        if (note.strip() == ""):
            self.outliner.noMoreNotes = True
            self.outliner.noteText.set("No more notes")
        else:
            self.outliner.noteText.set(note)

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
