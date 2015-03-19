# -*- coding: utf-8 -*-

import tkinter as Tk

class Link:
	WEIGHT	= 2
	def __init__(self,canvas,firstSide,secondSide):
		""" Construct a new friendship between two persons, which has to be drawn on a specific canvas """
		self.canvas		= canvas
		self.firstSide	= firstSide
		self.secondSide= secondSide
		tag	= 'link_'+self.getIdentifier()
		ax,ay	= self.firstSide.center
		bx,by	= self.secondSide.center
		res = self.canvas.create_line(ax,ay,bx,by, fill='#000',activefill='#FF0000',tag=tag,width=Link.WEIGHT)
		self.canvas.tag_bind(tag,"<Double-Button-1>", self.mouseDubbleClicked)
	def getSource(self):
		return self.firstSide
	def getDestination(self):
		return self.secondSide
	def delete(self):
		""" Notify to GUI system that the friendship will be deleted """
		tag	= 'link_'+self.getIdentifier()
		self.canvas.delete(tag)
		self.canvas.tag_unbind(tag,"<Any>")
	def getIdentifier(self):
		""" Get the unique identifier of this link (composed of identifiers of the two persons) """
		minimum = self.firstSide.identifier
		maximum = self.secondSide.identifier
		if(minimum > maximum):
			minimum,maximum = maximum,minimum
		return minimum+','+maximum
	def mouseDubbleClicked(self,mouseEvent):
		""" Event management when a mouse button is clicked twice """
		self.canvas.edgeDelete(self)
	def draw(self):
		""" draw this person on its associated canvas """
		ax,ay	= self.firstSide.center
		bx,by	= self.secondSide.center
		self.canvas.coords('link_'+self.getIdentifier(), ax,ay,bx,by)
	def __hash__(self):
		return hash(self.getIdentifier())
	def __eq__(self,other):
		if(other is None): return False
		return self.getIdentifier() == other.getIdentifier()