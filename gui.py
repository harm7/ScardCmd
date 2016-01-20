# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frmMain
###########################################################################

class frmMain ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ScardCmd", pos = wx.DefaultPosition, size = wx.Size( 813,666 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.treeReaders = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		self.treeReaders.SetMinSize( wx.Size( -1,200 ) )
		
		bSizer2.Add( self.treeReaders, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.txtLog = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.ALWAYS_SHOW_SB|wx.VSCROLL )
		bSizer2.Add( self.txtLog, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.SetMenuBar( self.m_menubar1 )
		
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.m_toolBar1.Realize() 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.treeReaders.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.evtOpenReader )
		self.txtLog.Bind( wx.EVT_KEY_DOWN, self.evtLogKeyDown )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def evtOpenReader( self, event ):
		event.Skip()
	
	def evtLogKeyDown( self, event ):
		event.Skip()
	

