# -*- coding: utf-8 -*- 
__author__ = 'harm7'

import wx
import gui
import string
from smartcard.System import *
from smartcard.util import toHexString
from smartcard import Exceptions


def logchr(c):
    if chr(c) in string.printable:
        return chr(c)
    else:
        return '.'


class fMain(gui.frmMain):
    def __init__(self, parent):
        gui.frmMain.__init__(self, parent)
        self.card = None
        self.reader_list = None
        self.history = []
        self.history_index = 0
        self.lastpos = 0
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.txtLog.SetFont(font1)
        self.evtRdrRefresh(None)

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
        if wx.WXK_RETURN == code or wx.WXK_NUMPAD_ENTER == code:
            linenum = len(self.txtLog.GetRange(0, self.txtLog.GetInsertionPoint()).split("\n"))
            linetext = self.txtLog.GetLineText(linenum-1)
            self.history.append(linetext)
            self.history_index = len(self.history)
            cmd = map(ord, linetext.decode('hex'))
            self.txtLog.AppendText('\n')
            if self.card:
                try:
                    data, sw1, sw2 = self.card.transmit(cmd)
                except Exceptions.CardConnectionException as ex:
                    self.txtLog.SetDefaultStyle(wx.TextAttr('RED'))
                    self.txtLog.AppendText("{0}\n\n".format(ex.message))
                    self.txtLog.SetDefaultStyle(wx.TextAttr('BLACK'))
                if sw1 == 0x61:
                    data, sw1, sw2 = self.card.transmit([0x00, 0xC0, 0x00, 0x00, sw2])
                self.txtLog.SetDefaultStyle(wx.TextAttr('BROWN'))
                if data:
                    self.txtLog.AppendText("> Data:\n")
                    for octet in [data[i: i+8] for i in xrange(0, len(data), 8)]:
                        txtform = ''.join(map(logchr, octet))
                        txtform = "{0}{1}{2}\n".format(toHexString(octet), ' '*((8-len(octet))*3+5), txtform)
                        self.txtLog.AppendText(txtform)
                self.txtLog.SetDefaultStyle(wx.TextAttr('BLUE'))
                self.txtLog.AppendText("> SW: " + toHexString([sw1, sw2]) + "\n\n")
                self.txtLog.SetDefaultStyle(wx.TextAttr('BLACK'))
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

    def evtRdrRefresh(self, event):
        rlist = readers()
        if self.reader_list != rlist:
            self.reader_list = rlist
            self.treeReaders.DeleteAllItems()
            root = self.treeReaders.AddRoot("PCSC")
            for r in rlist:
                self.treeReaders.AppendItem(root, str(r))
            self.treeReaders.ExpandAll()

app = wx.App()
frame = fMain(None)
frame.Show()
app.MainLoop()
