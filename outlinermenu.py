"""
 "  File: outlinermenu.py
 "  Written By: Gregory Owen
 "
 "  Description: Handles the menu for outlinergui.py
""" 

from Tkinter import *

class OutlinerMenu():

    def __init__(self, outliner, root):
        """ Initialize the menu to contain File and Topic options. """

        self.outliner = outliner

        self.menubar = Frame(root, relief=RAISED, borderwidth=2)
        self.menubar.pack(side=TOP, fill=X)
        
        FileBtn = self.makeFileMenu()
        self.TopicBtn = self.makeTopicMenu()
        self.NoteBtn = self.makeNoteMenu()

        self.menubar.tk_menuBar(FileBtn, self.TopicBtn, self.NoteBtn)

    """ ------------------------ File menu methods ------------------------- """

    def makeFileMenu(self):
        """ Initialize the File options in the menu. """

        FileBtn = Menubutton(self.menubar, text="File", underline=0)
        FileBtn.pack(side=LEFT, padx="2m")
        FileBtn.menu = Menu(FileBtn)

        FileBtn.menu.add_command(label="New Project", underline=0, 
                                 command=self.outliner.newProject)
        FileBtn.menu.add_command(label="Open Project", underline=0,
                                 command=self.outliner.openProject)
        FileBtn.menu.add_command(label="Save Project", underline=0, 
                                 command=self.outliner.saveProject)
        FileBtn.menu.add_command(label="Save Project as", underline=0,
                                 command=self.outliner.saveProjectAs)
        FileBtn.menu.add_command(label="Export Outline", underline=0,
                                 command=self.outliner.exportOutline)
        FileBtn.menu.add_command(label="Quit", underline=0,
                                 command = self.outliner.quit)

        FileBtn['menu'] = FileBtn.menu
        return FileBtn

    """ ------------------------ Topic menu methods ------------------------ """

    def makeTopicMenu(self):
        """ Initialize the Topic options in the menu. """

        TopicBtn = Menubutton(self.menubar, text="Topic", underline=0)
        TopicBtn.pack(side=LEFT, padx="2m")
        TopicBtn.menu = Menu(TopicBtn)
        TopicBtn.menu.topicList = Menu(TopicBtn.menu)

        for topic in self.outliner.model.topics.keys():
            TopicBtn.menu.topicList.add_command(
                label=topic["name"],
                underline=0,
                command=(lambda o=self.outliner, t=topic: o.viewTopic(t)))

        TopicBtn.menu.add_command(label="New Topic", underline=0, 
                                  command=self.outliner.newTopic)
        TopicBtn.menu.add_cascade(label="View Topic",
                                  menu=TopicBtn.menu.topicList)

        TopicBtn['menu'] = TopicBtn.menu
        return TopicBtn

    def addToTopicLists(self, topic):
        """ Append topic to the list of topics in the View Topic option in the
            Topic menu and in the Add To Topic option in the Note Menu. """

        self.TopicBtn.menu.topicList.add_command(
            label=topic["name"],
            underline=0,
            command=(lambda o=self.outliner, t=topic: o.viewTopic(t)))
        self.NoteBtn.menu.topicList.add_command(
            label=topic["name"],
            underline=0,
            command=(lambda o=self.outliner, t=topic: o.addNoteToTopic(t)))


    """ ------------------------ Note menu methods ------------------------- """

    def makeNoteMenu(self):
        """ Initialize the Note options in the menu. """

        NoteBtn = Menubutton(self.menubar, text="Note", underline=0)
        NoteBtn.pack(side=LEFT, padx="2m")
        NoteBtn.menu = Menu(NoteBtn)
        NoteBtn.menu.topicList = Menu(NoteBtn.menu)
        
        for topic in self.outliner.model.topics.keys():
            NoteBtn.menu.topicList.add_command(
                label=topic["name"],
                underline=0,
                command=(lambda o=self.outliner, t=topic: o.addNoteToTopic(t)))

        NoteBtn.menu.add_cascade(label="Add To Topic",
                                 menu=NoteBtn.menu.topicList)
        NoteBtn.menu.add_command(label="Next Note", underline=0,
                                 command=self.outliner.nextNote)
        NoteBtn.menu.add_command(label="Prev Note", underline=0,
                                 command=self.outliner.prevNote)

        NoteBtn['menu'] = NoteBtn.menu
        return NoteBtn
