"""
 "  File: outliner.py
 "  Written By: Gregory Owen
 "
 "  An easy way to synthesize notes into an essay outline.
""" 

from Tkinter import *
from tkFileDialog import *
from collections import deque
import tkSimpleDialog
import tkMessageBox

from outlinermodel import OutlinerModel
from outlinergui import OutlinerGUI

class Outliner():

    def __init__(self, master=None):
        self.model = OutlinerModel(self)
        self.gui = OutlinerGUI(master, self, self.model)

    def newProject(self):
        """ Create a new project. """
        
        notepath = askopenfilename()

        if notepath is not None:
            self.model.newModel(notepath)
            self.gui.displayNextNote()

    def openProject(self):
        """ Open a previous project from its .otln file. """
        
        projectPath = askopenfilename(filetypes=[("Outliner files", "*.otln")])

        if projectPath is None:
            return
        if projectPath[-5:] != ".otln":
            errorPrompt = "I'm sorry, but that file is not a valid input type.\n\
Please choose a valid Outliner file (.otln)"
            tkMessageBox.showerror("Error: Invalid File Type", errorPrompt)
            return

        self.model.openModel(projectPath)
        self.gui.openGUI()

    def saveProject(self):
        """ Save the current state of the project. """

        if self.model.filename is None:
            self.saveProjectAs()
        else:
            self.model.saveModel()

    def saveProjectAs(self):
        """ Save the project under a new name. """
        
        options = {}
        options['defaultextension'] = '.otln'
        options['filetypes'] = [('all files', '.*'), ('Outliner files', '.otln')]
        options['title'] = 'Save your outline'

        self.model.filename = asksaveasfilename(**options)

        if self.model.filename is not None:
            self.saveProject()

    def exportOutline(self):
        """ Create a .txt outline based off of the notes in the Outliner. """
        
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('Text files', '.txt')]
        options['title'] = 'Export your outline to a text file'
        
        exportpath = asksaveasfilename(**options)

        if exportpath is not None:
            self.model.exportModel(exportpath)

    def quit(self):
        """ Quit the outliner. """

        self.gui.root.quit()

    def newTopic(self):
        """ Create a new topic. """

        topicPrompt = "What would you like to call your new topic?"
        topicName = tkSimpleDialog.askstring("New Topic", topicPrompt)

        if topicName in self.model.topics:
            self.topicAlreadyExists()
            topicName = None

        if topicName is None:
            return

        self.model.newTopic(topicName)
        self.gui.initializeTopicGUI(self.model.topics[topicName])

    def topicAlreadyExists(self):
        """ Report to the user that there is already a topic with the name that
            they entered. """

        errorprompt = "I'm sorry, but a topic by that name already exists in" +\
            " this outline.\nPlease select a different name."
        tkMessageBox.showerror("Error: Topic Already Exists", errorprompt)

    def addNoteToTopic(self, topic):
        """ Add the currently-displayed note to the topic. """

        if len(self.model.notes) > 0:
            note = self.model.addNoteToTopic(topic)
            self.gui.addNoteToGUI(topic, note)
            self.gui.displayNextNote()

    def viewTopic(self, topic):
        """ Display the notes that are part of the topic. """

        self.gui.viewTopic(topic)

    def nextNote(self):
        """ Display the next note in the list. """

        if len(self.model.notes) > 0:
            self.model.notes.append(self.model.notes.popleft())
            self.gui.displayNextNote()

    def prevNote(self):
        """ Display the last note in the list. """

        if len(self.model.notes) > 0:
            self.model.notes.appendleft(self.model.notes.pop())
            self.gui.displayNextNote()

    def sortNotes(self):
        """ Sort the notes in each topic according to the order in which they 
            are currently arranged. """
        
        for topic in self.model.topics.values():
            topic['notes'] = [node.widget.cget('text')
                              for node in topic['dndlist'].getOrdered()]

    def sortTopics(self):
        """ Assign numbers to topics according to the order in which they are
            currently arranged. """

        ordered = self.gui.topicList.getOrdered()
        for i in range(len(ordered)):
            topic = ordered[i].widget.topic
            topic['number'] = i

""" --------------------------------- main method ------------------------------- """

if __name__ == "__main__":
    root = Tk()
    outliner = Outliner(root)
    root.mainloop()
