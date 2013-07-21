"""
 "  File: outlinergui.py
 "  Written By: Gregory Owen
 "
 "  Description: The GUI manager for outliner
""" 

from Tkinter import *
from outlinermenu import OutlinerMenu
import dndlist

class OutlinerGUI:

    def __init__(self, ol=None):

        self.outliner = ol
        self.root = self.outliner.root

        self.root.title("The Outliner, by Gregory Owen")
        self.defaultWidth = 700
        self.defaultHeight = 800

        geoString = str(self.defaultWidth) + "x" + str(self.defaultHeight)
        self.root.geometry(geoString)

        self.TOPICS_PER_ROW = 4

        self.menu = OutlinerMenu(self.outliner) 
        self.topicFrame = self.upperFrame = self.makeTopicFrame()
        self.noteFrame = self.lowerFrame = self.makeNoteFrame()
        self.packFrames()

        self.makeReturnFrame()

    """ ------------------------------------------------------------------------- """
    """                              General methods                              """
    """ ------------------------------------------------------------------------- """

    def packFrames(self):
        """ Pack self.upperFrame above self.lowerFrame. """

        self.upperFrame.pack(side=TOP, fill=BOTH, expand=True)
        self.lowerFrame.pack(side=TOP, anchor=S, fill=X, expand=True)

    def unpackFrames(self):
        """ Unpack the current self.upperFrame and self.lowerFrame. """

        self.upperFrame.pack_forget()
        self.lowerFrame.pack_forget()

    """ ------------------------------------------------------------------------- """
    """                            Topic Frame methods                            """
    """ ------------------------------------------------------------------------- """

    def makeTopicFrame(self):
        """ Make the topic frame, including buttons for new topics. """

        topicFrame = Frame(self.root)

        for col in range(self.TOPICS_PER_ROW):
            button = Button(topicFrame, text="New Topic")
            button.config(command=(lambda o=self.outliner, b=button: o.newTopic(b)))
            button.grid(row=0, column=col, sticky=NSEW, padx=10, pady=10)

        return topicFrame

    def newTopicButton(self, topic, button=None):
        """ If a Button object is passed, change its text to display the topic name.
             Otherwise, create and grid a new Button with the topic name. """

        if button is None:
            button = Button(self.topicFrame)
            index = topic["number"]
            button.grid(row=index/self.TOPICS_PER_ROW, column=(index %
                self.TOPICS_PER_ROW), sticky=NSEW, padx=10, pady=10)
        else:
            button.unbind("<Button-1>")

        endChar = '' if (len(topic["notes"]) == 1) else 's'
        buttonText = "%s\n%d note%s" % (topic["name"], len(topic["notes"]), endChar)
        button.config(text=buttonText)
        button.config(command=(lambda o=self.outliner, t=topic: o.addNoteToTopic(t)))

        return button

    def newTopicFrame(self, topic):
        """ Creates a new dndlist for the given topic and populates it with the
            topic's notes (if any). Returns a tuple containing the parent frame
            for the DNDList and the DNDList itself. """

        frame = Frame(self.root)
        list = dndlist.DNDList(frame, self.defaultWidth, self.defaultHeight,
                               items=topic["notes"])

        return (frame, list)

    def topicAlreadyExists(self):
        """ Report to the user that there is already a topic with the name that they
             entered. """
        errorprompt = "I'm sorry, but a topic by that name already exists in \
this outline.\nPlease select a different name."
        tkMessageBox.showerror("Error: Topic Already Exists", errorprompt)

    def viewTopic(self, topic):
        """ Display the notes that are part of the topic. """

        self.unpackFrames()
        self.upperFrame = topic["frame"]
        self.lowerFrame = self.returnFrame
        self.packFrames()

    def updateTopicGUI(self, topic):
        """ Update all GUI components relating to the given topic. """

        endChar = '' if (len(topic["notes"]) == 1) else 's'
        buttonText = "%s\n%d note%s" % (topic["name"], len(topic["notes"]), endChar)
        topic["button"].config(text=buttonText)

    def addNoteToGUI(self, topic, note):
        """ Add note to the DNDList of the given topic. """

        topic["dndlist"].addItem(note)

    """ ------------------------------------------------------------------------- """
    """                            Note Frame methods                             """
    """ ------------------------------------------------------------------------- """

    def makeNoteFrame(self):
        """ Make and deploy the note frame. """

        noteFrame = Frame(self.root, relief=RAISED, borderwidth=2)

        self.outliner.noteText = StringVar()
        self.noteLabel = Label(noteFrame, textvariable=self.outliner.noteText,
                height=5, width=80)

        noNotes = "No notes. Open an existing project or create a new one to import notes."
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

    """ ------------------------------------------------------------------------- """
    """                            Return Frame methods                           """
    """ ------------------------------------------------------------------------- """

    def makeReturnFrame(self):
        """ Make the return frame, but do not deploy it. """

        self.returnFrame = Frame(self.root, relief=RAISED, borderwidth=2)
        self.returnButton = Button(self.returnFrame, text="Return to essay view",
                                    command=self.returnToMain)
        self.returnButton.pack()

    def returnToMain(self):
        """ Return to the main (essay) view. """

        self.unpackFrames()
        self.upperFrame = self.topicFrame 
        self.lowerFrame = self.noteFrame
        self.packFrames()
