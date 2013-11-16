"""
 "  File: outlinermodel.py
 "  Written By: Gregory Owen
 "
 "  Model for the Outliner
""" 

from collections import deque
from operator import itemgetter
import json

"""
Fields in a topic:
  dndlist: DNDList containing this topic's notes (DNDList.dndlist)
  frame:   Frame containing this topic's dndlist (Tkinter.Frame)
  line:    Information line about the topic on the main screen (Tkinter.Frame)
  name:    Subject of the topic, used to index into Outliner.topics (string)
  notes:   Notes in the topic (list of strings)
  number:  Number of topics created before this one (int)
  rframe:  Frame into which notes are dragged to be removed (Tkinter.Frame)
"""

class OutlinerModel():

    def __init__(self, outliner):
        self.outliner = outliner
        self.filename = None
        self.topics = {}
        self.notes = deque()

    def newModel(self, notepath):
        """ Create a new project from the note file at notepath. """

        try:
            notefile = open(notepath, 'r')            
            for note in notefile.read().strip().split("\n\n"):
                if note != "":
                    self.notes.append(" ".join(note.split("\n")))
        except IOError:
            print "Error: no such file"

    def openModel(self, projectpath):
        """ Open a previous project from its .otln file. """
        
        self.filename = projectpath
        projectFile = open(projectpath, 'r')

        noteList = projectFile.readline()
        self.notes = deque(json.loads(noteList))

        topicDict = projectFile.readline()
        self.topics = json.loads(topicDict)

        projectFile.close()

    def saveModel(self):
        """ Save the current state of the project. """
        
        self.sortTopics()
        self.sortNotes()

        outfile = open(self.filename, 'w')
        outfile.write(json.dumps(list(self.notes)))
        outfile.write("\n")
        outfile.write(json.dumps(self.topics, default=self.handleJSON))
        outfile.close()

    def handleJSON(self, obj):
        """ Handles the JSON encoding of obj when obj would cause a TypeError. """

        return None

    def exportModel(self, exportpath):
        """ Create a .txt outline based off of the notes in the model. """

        try:
            self.sortNotes()
            self.sortTopics()

            outfile = open(exportpath, 'w')
            # Write topics in the order given by their numbers
            for topic in sorted(self.topics.values(), key=itemgetter('number')):
                outfile.write(topic['name'] + ":\n")
                for note in topic['notes']:
                    outfile.write("\t" + note + "\n\n")
                outfile.write("\n")
            outfile.close()
        except IOError:
            print "Error: no such file"

    def newTopic(self, topicName):
        """ Create a new topic with the given name. """

        newTopic = {}
        newTopic['name'] = topicName
        newTopic['notes'] = []
        newTopic['number'] = len(self.topics.keys())
        self.topics[topicName] = newTopic

    def addNoteToTopic(self, topic):
        """ Add the currently-displayed note to the topic, return that note. """

        try:
            note = self.notes.popleft()
            topic['notes'].append(note)
            return note
        except IndexError:
            print "Error: tried to pop empty notes deque"
            return None

    def sortNotes(self):
        """ Sort the notes in each topic according to the order in which they 
            are currently arranged. """

        self.outliner.sortNotes()

    def sortTopics(self):
        """ Assign numbers to topics according to the order in which they are
            currently assigned. """

        self.outliner.sortTopics()
