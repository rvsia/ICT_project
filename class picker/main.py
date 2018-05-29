import sys

import os
import sys
import wx
from collections import defaultdict
import random

print (sys.path)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(535,655))
        self.CreateStatusBar() # A StatusBar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuReset = filemenu.Append(wx.ID_RESET, "&Reset", " Reset the program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        self.clearButton = wx.Button(self, wx.ID_CLEAR, label='Open a file',pos=(415, 5), size=(100, 25))
        self.filename = wx.TextCtrl(self,pos=(5, 5), size=(400, 25))
        self.filename.SetEditable(False)
        self.filename.AppendText("Please select a txt file")
        self.filename.SetCanFocus(False)
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.clearButton)

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnReset, menuReset)
        self.SetBackgroundColour(wx.Colour(red=255,green=255,blue=255))
        self.Show(True)

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A program that has a text file with a single document\
        on each line on the input. At the beginning, there is a\
        class label (e.g., an integer number), e.g.,\
        1 Very good price/quality.\
        2 Breakfast room is a bit small.\
        The program will be able to randomly select desired\
        numbers of documents from given classes (e.g., 1000\
        documents from class 1 and 2000 documents form\
        class 5). Class labels might be eventually changed\
        according to the given criteria (e.g., all labels 2 will be\
        changed to label 1).\
        Test your programs on a sample data with just a few\
        instances.", "A document picker", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnReset(self,e):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def OnClear(self,e):
        with wx.FileDialog(self, "Open txt file", wildcard="txt files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding="utf8") as file:
                    self.filename.Clear()
                    self.filename.write(pathname)
                    self.getData(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def getData(self, file):
        c = file.readlines()
        self.classes = []
        self.documents = defaultdict()

        for line in c:
            l = line[2:]
            l = l.replace("\n","")
            classa = line.split(' ')[0]
            if not classa in self.classes:
                self.classes.append(classa)
                self.documents[classa] = [l]
            else:
                self.documents[classa].append(l)
        #print(self.documents)
        self.dataLoaded()

    def dataLoaded(self):
        self.picks = defaultdict()
        box1label = wx.StaticText(self, label="Classes:", pos=(5, 35), style=0)
        self.boxl = wx.ListBox(self, -1, (5, 50), (100, 300), self.classes, wx.LB_SINGLE)
        self.renameButton = wx.Button(self, label='Change to different class', pos=(315, 50), size=(200, 25))
        self.chooseButton = wx.Button(self, label='Choose', pos=(315, 80), size=(200, 25))
        self.export = wx.Button(self, label='Export output', pos=(315, 540), size=(200, 25))
        self.Bind(wx.EVT_BUTTON, self.picked, self.chooseButton)
        self.Bind(wx.EVT_BUTTON, self.OnSaveAs, self.export)
        self.Bind(wx.EVT_BUTTON, self.renameClass, self.renameButton)

        picksLabel = wx.StaticText(self, label="Picks:", pos=(115, 85), style=0)
        self.classCountArea = wx.TextCtrl(self, value="1",  pos=(155, 80), size=(100, 25))
        self.classCount = wx.SpinButton(self, pos=(255, 80), size=(25, 25))
        self.classCount.SetRange(1, 10000)
        self.classCount.SetValue(1)
        self.Bind(wx.EVT_SPIN, self.OnSpin, self.classCount)

        self.renameTextName = wx.TextCtrl(self, pos=(115, 50), size=(195, 25))
        self.renameTextName.write("Rename to...")


        self.className = wx.TextCtrl(self, pos=(115, 110), size=(400, 25))
        self.className.SetEditable(False)
        self.className.write("You must to choose a class")

        self.Bind(wx.EVT_LISTBOX, self.selectClass, self.boxl)
        box1labe2 = wx.StaticText(self, label="Documents:", pos=(115, 140), style=0)
        self.box1labe3 = wx.StaticText(self, label="Unselected", pos=(185, 140), style=0)
        self.box2 = wx.ListBox(self, -1, (115, 160), (400, 190), [] , wx.LB_SINGLE)
        #self.box3 = wx.ListCtrl(self, -1, (5, 355), (510, 100), [] , wx.LB_SINGLE)
        self.box3 = wx.ListCtrl(self, size=(510,180), style=wx.LC_REPORT)
        self.box3.SetPosition((5, 355))
        self.box3.InsertColumn(0, 'Class')
        self.box3.InsertColumn(1, 'Random picks',width=125)
        self.index = 0

    def selectClass(self, event):
        self.className.Clear()
        self.className.AppendText(event.GetEventObject().GetStringSelection())
        self.set = self.box2.Set(self.documents[event.GetEventObject().GetStringSelection()])
        self.box1labe3.SetLabelText(str(len(self.documents[event.GetEventObject().GetStringSelection()])))

    def picked(self, event):
        try:
            if int(self.classCountArea.GetValue())>int(self.box1labe3.GetLabel()):
                raise Exception
            if int(self.classCountArea.GetValue())<0:
                raise Exception
            self.picks[self.className.GetValue()] = int(self.classCountArea.GetValue())
            self.box3.InsertItem(self.index, self.className.GetValue())
            self.box3.SetItem(self.index, 1, self.classCountArea.GetValue())
            self.index += 1
            self.changeDisable()
        except ValueError:
            dlg = wx.MessageDialog(self, "You must choose a number", "OK", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        except:
            dlg = wx.MessageDialog(self, "You must choose a number which is => 0 and <= documents count", "OK", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        print(self.picks)

    def randomSentences(self, key, numberOfRandom):
        selectedSentenc = []
        sentencesOfClass = list(self.documents[key])
        if numberOfRandom == len(selectedSentenc):
            selectedSentenc = sentencesOfClass
        else:
            for i in range (0,numberOfRandom):
                randomNum = random.randint(0, len(sentencesOfClass)-1)
                selectedSentenc.append(key+" "+sentencesOfClass[randomNum])
                sentencesOfClass.remove(sentencesOfClass[randomNum])
        return selectedSentenc

    def pickedSentences(self):
        allSelectedSentences = []
        for key, value in self.picks.items():
           allSelectedSentences.extend(self.randomSentences(key,value))
        return allSelectedSentences

    def OnSaveAs(self, event):
        with wx.FileDialog(self, "Save txt file", wildcard="txt files (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w', encoding="utf8") as outFile:
                    self.doSaveData(outFile)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def doSaveData(self, outFile):
        sentencesToSave = self.pickedSentences()
        for sentenc in sentencesToSave:
            outFile.write("%s\n" % sentenc)

    def changeDisable(self):
        self.renameButton.Disable()

    def OnSpin(self, event):
        self.classCountArea.SetValue(str(event.GetPosition()))

    def renameClass(self, event):
        try:
            splitClass=0
            newName = self.renameTextName.GetValue()
            oldName = self.className.GetValue()
            if newName == "":
                raise Exception
            for c in self.documents:
                if c == newName:
                    splitClass = 1
            if splitClass == 0:
                self.documents[newName] = []
            self.documents[newName].extend(self.documents[oldName])
            del self.documents[oldName]
            print(self.documents)
            self.updateBox1();
        except:
            dlg = wx.MessageDialog(self, "You must write some name of new class and choose class which you want to change", "OK", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def updateBox1(self):
        self.classes = list(self.documents.keys())
        self.set = self.boxl.SetItems(self.classes)


app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()