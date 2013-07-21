"""
 "  File: outliner.py
 "  Written By: Gregory Owen
 "  Date: 24-12-2012 
 "  Last Modified: Sun Apr  7 02:10:09 2013
 "
 "  Execution: python outliner.py
 "
 "  Description: A graphical user interface for an outline generator.
""" 

from Tkinter import *
from tkFileDialog import *
from collections import deque
import tkSimpleDialog
import tkMessageBox
import json

from outlinergui import OutlinerGUI

"""
Fields in a topic:
  name:    Subject of the topic, used to index into Outliner.topics (string)
  notes:   Notes in the topic (list of strings)
  number:  Number of topics created before this one (int)
  button:  Button used to select topic (Tkinter.Button)
  frame:   Frame containing this topic's dndlist (Tkinter.Frame)
  dndlist: DNDList containing this topic's notes (DNDList.dndlist)
"""

class Outliner():

    def __init__(self, master=None):
        self.root = master
        self.filename = None
        self.topics = {}
        self.notes = deque()
        self.noMoreNotes = True

        self.gui = OutlinerGUI(self)

    def newProject(self):
        """ Create a new project. """
        
        notepath = askopenfilename()

        if notepath is not None:
            notefile = open(notepath, 'r')
            self.notes = deque(notefile.read().strip().split("\n"))

            if len(self.notes) > 0:
                self.noMoreNotes = False
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

        self.filename = projectPath
        projectFile = open(projectPath, 'r')

        noMoreNotes = projectFile.readline()
        self.noMoreNotes = json.loads(noMoreNotes)

        currNote = projectFile.readline()
        self.noteText.set(json.loads(currNote))
        
        noteList = projectFile.readline()
        self.notes = deque(json.loads(noteList))

        topicDict = projectFile.readline()
        self.topics = json.loads(topicDict)

        # Sort the topics by number
        sortedTopicNames = sorted(self.topics,
                                  key=(lambda name: self.topics[name]["number"]))
        
        for name in sortedTopicNames:
            topic = self.topics[name]
            topic["button"] = self.gui.newTopicButton(topic)
            topic["frame"], topic["dndlist"] = self.gui.newTopicFrame(topic)
            self.gui.menu.addToTopicLists(topic)

        projectFile.close()

    def saveProject(self):
        """ Save the current state of the project. """
        
        if self.filename is None:
            self.saveProjectAs()
        else:
            # Sort notes in each topic
            for topic in self.topics.values():
                topic["notes"] = [node.widget.cget('text')
                                  for node in topic["dndlist"].getOrdered()]

            outfile = open(self.filename, 'w')
            outfile.write(json.dumps(self.noMoreNotes))
            outfile.write("\n")
            outfile.write(json.dumps(self.noteText.get()))
            outfile.write("\n")
            outfile.write(json.dumps(list(self.notes)))
            outfile.write("\n")
            outfile.write(json.dumps(self.topics, default=self.handleJSON))
            outfile.close()

    def saveProjectAs(self):
        """ Save the project under a new name. """
        
        options = {}
        options['defaultextension'] = '.otln'
        options['filetypes'] = [('all files', '.*'), ('Outliner files', '.otln')]
        options['title'] = 'Save your outline'

        self.filename = asksaveasfilename(**options)

        if self.filename is not None:
            self.saveProject()

    def handleJSON(self, obj):
        """ Handles the JSON encoding of obj when obj would cause a TypeError. """

        return None

    def exportOutline(self):
        """ Create a new project. """
        
        print "exportOutline() called."

    def quit(self):
        """ Quit the outliner. """

        self.root.quit()

    def newTopic(self, button=None):
        """ Create a new topic. If a Button object is passed, associate that Button
             with the new topic. Otherwise, create a new Button for the topic. """

        topicPrompt = "What would you like to call your new topic?"
        topicName = tkSimpleDialog.askstring("New Topic", topicPrompt)

        if topicName in self.topics:
            self.gui.topicAlreadyExists()
            topicName = None
            self.newTopic(button)

        if topicName is None:
            print "Error: no topic name"
            return

        newTopic = {}
        newTopic["name"] = topicName
        newTopic["notes"] = []
        newTopic["number"] = len(self.topics.keys())
        newTopic["button"] = self.gui.newTopicButton(newTopic, button)
        newTopic["frame"], newTopic["dndlist"] = self.gui.newTopicFrame(newTopic)

        self.topics[topicName] = newTopic
        self.gui.menu.addToTopicLists(newTopic)

    def addNoteToTopic(self, topic):
        """ Add the currently-displayed note to the topic. """

        if not self.noMoreNotes:
            note = self.noteText.get()
            topic["notes"].append(note)
            self.gui.addNoteToGUI(topic, note)
            self.gui.updateTopicGUI(topic)
            self.gui.displayNextNote()

    def viewTopic(self, topic):
        """ Display the notes that are part of the topic. """

        self.gui.viewTopic(topic)

    def nextNote(self):
        """ Display the next note in the list. """

        print "nextNote() called."

    def prevNote(self):
        """ Display the previous note in the list. """

        print "prevNote() called."


""" --------------------------------- main method ------------------------------- """

if __name__ == "__main__":
    root = Tk()
    outliner = Outliner(root)
    root.mainloop()
