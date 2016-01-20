__author__ = 'harm7'

import wx
import gui
from smartcard.System import *
from smartcard.util import toHexString


class fMain(gui.frmMain):
    def __init__(self, parent):
        gui.frmMain.__init__(self, parent)
        self.card = None
        self.history = []
        self.history_index = 0
        self.lastpos = 0
        root = self.treeReaders.AddRoot("PCSC")
        for r in readers():
            self.treeReaders.AppendItem(root, str(r))
        self.treeReaders.ExpandAll()

    def evtOpenReader(self, event):
        if self.card:
            self.card.disconnect()
        r_name = self.treeReaders.GetItemText(event.GetItem())
        for r in readers():
            if str(r) == r_name:
                self.card = r.createConnection()
                self.card.connect()
                self.txtLog.AppendText("ATR: " + toHexString(self.card.getATR()) + "\n")
                self.lastpos = self.txtLog.GetLastPosition()
                break

    def evtLogKeyDown(self, event):
        code = event.GetKeyCode()
        if wx.WXK_RETURN == code:
            linenum = len(self.txtLog.GetRange(0, self.txtLog.GetInsertionPoint()).split("\n"))
            linetext = self.txtLog.GetLineText(linenum-1)
            self.history.append(linetext)
            self.history_index = len(self.history)
            cmd = map(ord, linetext.decode('hex'))
            self.txtLog.AppendText('\n')
            if self.card:
                data, sw1, sw2 = self.card.transmit(cmd)
                if sw1 == 0x61:
                    data, sw1, sw2 = self.card.transmit([0x00, 0xC0, 0x00, 0x00, sw2])
                self.txtLog.SetForegroundColour('DARK GOLDENROD')
                self.txtLog.AppendText("\n> Data: " + toHexString(data) + "\n")
                self.txtLog.SetForegroundColour('BLUE')
                self.txtLog.AppendText("> SW: " + toHexString([sw1, sw2]) + "\n\n")
                self.txtLog.SetForegroundColour('BLACK')
            self.lastpos = self.txtLog.GetLastPosition()
        elif wx.WXK_UP == code:
            if not len(self.history):
                return
            if self.history_index:
                self.history_index -= 1
            self.txtLog.Remove(self.lastpos, self.txtLog.GetLastPosition())
            self.txtLog.SetInsertionPoint(self.lastpos)
            self.txtLog.WriteText(self.history[self.history_index])
        elif wx.WXK_DOWN == code:
            if not len(self.history):
                return
            if self.history_index + 1 < len(self.history):
                self.history_index += 1
            self.txtLog.Remove(self.lastpos, self.txtLog.GetLastPosition())
            self.txtLog.SetInsertionPoint(self.lastpos)
            self.txtLog.WriteText(self.history[self.history_index])
        elif wx.WXK_BACK == code:
            if self.lastpos < self.txtLog.GetInsertionPoint():
                event.Skip()
        else:
            event.Skip()
            return


app = wx.App()
frame = fMain(None)
frame.Show()
app.MainLoop()