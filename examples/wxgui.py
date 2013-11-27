""" this is a template for a wx python frame.
imported from 06wxpython.py example
"""

try:
    import wx
    import os
    import mirra.utilities

    class MyFrame(mirra.utilities.WxMirraFrame):#, wx.FileDropTarget):

##        def OnDropFiles(self, x, y, filenames):
##            self.window.SetInsertionPointEnd()
##            for file in filenames:
##                print x,y, file + '\n'
      
##        def doStatusBar(self): 
##            self.CreateStatusBar(1,0)
##            self.SetStatusText("ixi app")

        def doMenu(self):
            #-- menus IDs. constants
            ID_OPEN     = 101
            ID_IMPORT   = 102
            ID_SAVE     = 103
            ID_SAVEAS   = 104
            ID_EXIT     = 105
            ID_HELP     = 106
            ID_ABOUT    = 107

            #--vFile
            menu = wx.Menu()
            menu.Append(ID_OPEN, "&Open\tAlt-O", "open file")
            menu.Append(ID_IMPORT, "&Import\tAlt-I", "import file")
            menu.Append(ID_SAVE, "&Save\tAlt-S", "save file")
            menu.Append(ID_SAVEAS, "&Save as", "save as file")
            menu.AppendSeparator()
            menu.Append(ID_EXIT, "&Exit\tAlt-X", "Quit")
            #-- About
            menu2 = wx.Menu()
            menu2.Append(ID_HELP, "&Help\tAlt-H", "help!")
            menu2.Append(ID_ABOUT, "&About this app", "About this app text")
            #-- add all to manubar
            menuBar = wx.MenuBar()
            menuBar.Append(menu, "&File")
            menuBar.Append(menu2, "&Help")
            #-- set bar
            self.SetMenuBar(menuBar)
            #-- set IDs and functions
            wx.EVT_MENU(self, ID_OPEN, self.onOpen)
            wx.EVT_MENU(self, ID_IMPORT, self.onImport)
            wx.EVT_MENU(self, ID_SAVE, self.onSave)
            wx.EVT_MENU(self, ID_SAVEAS, self.onSaveAs)
            wx.EVT_MENU(self, ID_EXIT,  self.onQuit)
            #
            wx.EVT_MENU(self, ID_HELP,  self.onHelp)
            wx.EVT_MENU(self, ID_ABOUT, self.onAbout)

        #-------- menu ---------------------------------------------
        def onQuit(self, event):
            self.Close(True)

        def onHelp(self, event):
            dlg = wx.MessageDialog(self, "First Aid text\n"
                "in this message box\n",
                "First Aid", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        def onAbout(self, event):
            dlg = wx.MessageDialog(self, "This is the Mirra WxPython template\n"
                "implementing all that stuff like\n"
                "import/save as dialogues and this message.\n",
                "About this app", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        #-----
        def onOpen(self, event):
            wildcard = "files (*.xx)|*.xx|All files (*.*)|*.*"
            dlg = wx.FileDialog(self, "Open file", os.getcwd(),
                style = wx.OPEN, wildcard = wildcard)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                self.ReadFile()
                self.SetTitle(self.title + ' -- ' + self.filename)
            dlg.Destroy()

        def onImport(self, event):
            #wildcard = "files (*.xx)|*.xx|All files (*.*)|*.*"
            wildcard = "All files (*.*)|*.*"
            dlg = wx.FileDialog(self, "Import file", os.getcwd(),
                style = wx.OPEN, wildcard = wildcard)
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                #self.ReadFile()
                #self.SetTitle(self.title + ' -- ' + self.filename)
            dlg.Destroy()

        def onSave(self, event):
            if not self.filename:
                self.OnSaveAs(event)
            else:
                self.SaveFile()

        def onSaveAs(self, event):
            wildcard = "files (*.xx)|*.xx|All files (*.*)|*.*"
            dlg = wx.FileDialog(self, "Save as", os.getcwd(),
                style=wx.SAVE | wx.OVERWRITE_PROMPT,
                wildcard = wildcard)
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                if not os.path.splitext(filename)[1]:
                    filename = filename + '.ddl'
                self.filename = filename
                self.SaveFile()
                self.SetTitle(self.title + ' -- ' + self.filename)
            dlg.Destroy()

        def SaveFile(self):
            if self.filename:
                print "saving file"
    ##            data = self.getData()
    ##            f = open(self.filename, 'w')
    ##            f.close()



except ImportError:
    print 'Mirra > gui.py : ImportError, no wxpython found.'





