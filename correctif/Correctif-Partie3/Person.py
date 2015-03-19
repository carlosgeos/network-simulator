# -*- coding: utf-8 -*-

import tkinter as Tk
import time
from PlatformUtils import *

import rumorFunctions as Core


class Person:
	WIDTH				= 20
	CLICK_TIME			= 300
	def __init__(self,identifier,canvas):
		""" Construc a new GUI person with its unique identifier (name) and its drawing canvas """
		self.identifier= str(identifier)
		self.canvas		= canvas
		self.politics	= Core.NO_RUMOR
		self.center		= 0,0
		LEFT,RIGHT = str(PlatformUtils.getLeftButton()),str(PlatformUtils.getRightButton())
		self.canvas.create_oval(0,0,0,0, fill=self.toRGB(),activeoutline='#FF0000',tag='node_'+self.identifier)
		self.canvas.tag_bind('node_'+self.identifier, "<Any-Enter>", self.onMouseOver)
		self.canvas.tag_bind('node_'+self.identifier, "<Button-"+LEFT+">", self.onMouseDown)
		self.canvas.tag_bind('node_'+self.identifier, "<Motion>", self.onMouseMove)
		self.canvas.tag_bind('node_'+self.identifier, "<ButtonRelease-"+LEFT+">", self.onMouseUp)
		self.canvas.tag_bind('node_'+self.identifier,"<Double-Button-"+LEFT+">", self.mouseDubbleClicked)
		self.canvas.tag_bind('node_'+self.identifier, "<Button-"+RIGHT+">", self.mouseClicked)
		self.down = self.timestamp()
	#
	def timestamp(self):
		return int(round(time.time() * 1000))
	def onMouseMove(self,mouseEvent):
		""" Event management when the mouse moves """
		self.canvas.drawEdgeTo(mouseEvent.x,mouseEvent.y)
	def onMouseOver(self,mouseEvent):
		""" Event management when the mouse is over a GUI object """
		self.canvas.nodeOver(self)
	def onMouseDown(self,mouseEvent):
		self.down = self.timestamp()
		""" Event management when a mouse button is pressed """
		self.canvas.startEdgeFrom(self)
	def mouseDubbleClicked(self,mouseEvent):
		""" Event management when a mouse button is clicked twice """
		self.canvas.nodeDelete(self)
	def mouseClicked(self,mouseEvent):
		""" Event management when a mouse button is clicked (pressed and released) """
		self.canvas.nodeColorize(self)
	def onMouseUp(self,mouseEvent):
		up = self.timestamp()
		if((up - self.down) < Person.CLICK_TIME):
			self.canvas.endEdgeTo(None)
			return False
		""" Event management when a mouse button is released """
		under = self.canvas.find_overlapping(mouseEvent.x, mouseEvent.y, mouseEvent.x, mouseEvent.y)
		under = list(under)
		if(under):
			matched = []
			for x in under:
				matched += self.canvas.gettags(x)
			matched = list(filter(lambda x:x.startswith('node_'), matched))
			if(matched):
				under = matched[0][len('node_'):]
			else:
				under = None
		else:
			under = None
		self.canvas.endEdgeTo(under)
	#
	def setColor(self,value):
		""" Set the color (rumor) for the current person """
		self.politics = value if(type(value) is int)else int(value[1:],16)
		self.canvas.itemconfig('node_'+self.identifier,fill=self.toRGB())
	def delete(self):
		""" Notify to GUI system that the person will be deleted """
		self.canvas.delete('node_'+self.identifier)
		self.canvas.tag_unbind('node_'+self.identifier,"<Any>")
	def toRGB(self):
		""" Get the value (RBG format) of the known rumor """
		return '#'+ (hex(self.politics)[2:].upper().rjust(6,'0'))
	def draw(self,x=0,y=0):
		""" draw this person on its associated canvas """
		self.center = x,y
		r		= max(Person.WIDTH>>1,1)
		self.canvas.coords('node_'+self.identifier, x-r,y-r,x+r,y+r)
	#
	def __hash__(self):
		return hash(self.identifier)
	def __eq__(self,other):
		if(other is None): return False
		return self.identifier == other.identifier
	def __str__(self):
		return 'Person: '+str(self.identifier)
	def __repr__(self):
		return 'Person: '+str(self.identifier)
