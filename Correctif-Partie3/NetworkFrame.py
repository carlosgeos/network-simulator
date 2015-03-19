# -*- coding: utf-8 -*-

import tkinter as Tk
from tkinter import colorchooser as tkColorChooser
from tkinter import simpledialog as tkSimpleDialog
from tkinter import messagebox as tKMessageBox

import random
from math import pi,sin,cos

from Person import *
from Link import *

class NetworkFrame(Tk.Canvas):
	def __init__(self,master):
		""" Construct a new drawing canvas for the network """
		Tk.Canvas.__init__(self,master,width=200,height=200,background='#DDD')
		self.layout='circular'
		self.nodes = []
		self.edges = []
		self.bind("<Configure>",self.redraw)
		self.first		= None
		self.second		= None
	def setLayout(self,layout):
		""" update the layout (how to draw) method of the network """
		self.layout = layout
	def redraw(self,event=None):
		""" refresh the drawing """
		if(self.nodes):
			eval('self.'+self.layout+'_layout()')
	def random_layout(self):
		""" Place randomly person of the network """
		border = Person.WIDTH
		width	= self.winfo_width()-(border<<1)
		height= self.winfo_height()-(border<<1)
		for node in self.nodes:
			node.draw(int(random.random()*width)+border,int(random.random()*height)+border)
		self.drawEdges()
	def drawEdges(self):
		""" Draw all links meaning who is a friend of whom """
		for edge in self.edges:
			edge.draw()
	def shell_layout(self):
		""" Place person of the network as a seashell """
		border = Person.WIDTH
		width	= self.winfo_width()-(border<<1)
		height= self.winfo_height()-(border<<1)
		step = 2.0*pi/len(self.nodes)
		positions	= [ (i*step*cos(i) , i*step*sin(i)) for i in range(len(self.nodes))]
		maxX,maxY	= positions[0]
		maxX,maxY	= abs(maxX),abs(maxY)
		for x,y in positions:
			maxX = max(maxX,abs(x))
			maxY = max(maxY,abs(y))
		maxX	*= 2.0
		maxY	*= 2.0
		positions	= [ (x/maxX +0.5, y/maxY+0.5) for (x,y) in positions]
		for (i,node) in enumerate(self.nodes):
			x,y	= positions[i]
			node.draw(int(x*width)+border,int(y*height)+border)
		self.drawEdges()
	def circular_layout(self):
		""" Place person of the network as a circle """
		border = Person.WIDTH
		width	= self.winfo_width()-(border<<1)
		height= self.winfo_height()-(border<<1)
		step = 2.0*pi/len(self.nodes)
		for (i,node) in enumerate(self.nodes):
			i *= step
			x = (cos(i)+1.0)/2.0
			y = (sin(i)+1.0)/2.0
			node.draw(int(x*width)+border,int(y*height)+border)
		self.drawEdges()
	def nodeOver(self,node):
		"""
		Update the information panel located in the main frame
		with the name of the current person
		"""
		self.master.master.updateInfoPanel(node)
	def edgeDelete(self,edge,redraw=True):
		""" Delete a specific link (a friendship) """
		for (i,n) in enumerate(self.edges):
			if(edge is n):
				edge.delete()
				del self.edges[i]
				if(redraw): self.redraw(None)
				return
	def nodeDelete(self,node):
		""" Delete a specific person """
		for (i,n) in enumerate(self.nodes):
			if(node is n):
				edges = list(filter(lambda x:x.firstSide is n or x.secondSide is n,self.edges))
				for edge in edges:
					self.edgeDelete(edge,False)
				node.delete()
				del self.nodes[i]
				self.redraw(None)
				return
	def addPerson(self):
		""" Add a new person in the network and canvas """
		node = Person('',self)
		self.itemconfig('node_',dash=(3,5),fill='#000',outline='#F00',width=3)
		self.nodes.append(node)
		self.redraw()
		res = tkSimpleDialog.askstring("New node", "Enter the name of the new node")
		self.nodes[-1].delete()
		del self.nodes[-1]
		if(res):
			res = res.strip()
		if(res):
			if(len(list(filter(lambda x:res is x.identifier,self.nodes))) > 0):
				tKMessageBox.showerror("Existing name","This name is already given")
			else:
				self.nodes.append(Person(res,self))
		self.redraw()
	def startEdgeFrom(self,node):
		""" Start to establish friendshipfrom a person """
		self.first = node
		x,y = self.first.center
		self.create_line(x,y,x,y, fill='#00F',activefill='#00F',tag='show',width=Link.WEIGHT)
	def drawEdgeTo(self,x,y):
		""" Draw an temporary edge (new friendship) """
		if(self.first is None): return
		ax,ay	= self.first.center
		self.coords('show', ax,ay,x,y)
	def endEdgeTo(self,node):
		""" End to establish friendshipfrom to person """
		node = list(filter(lambda x:x.identifier == node,self.nodes))
		node = node[0] if(node)else None
		if(node not in [None , self.first]):
			nodes		= [self.first , node]
			similar = list(filter(lambda edge: edge.getSource() in nodes and edge.getDestination() in nodes ,self.edges))
			if(len(similar) > 0):
				tKMessageBox.showinfo("Adding Link","Link already exist")
			else:
				self.second = node
				self.edges.append(Link(self,self.first,self.second))
		elif(node is self.first):
			tKMessageBox.showinfo("Adding Link","A person cannot be linked to himself")
		self.first = self.second = None
		self.delete('show')
	def nodeColorize(self,node):
		""" Open a Dialog box to update the rumor of a person """
		rgb,html = tkColorChooser.askcolor(node.toRGB(), title='Choose the politic color of the node '+node.identifier)
		if(html):
			node.setColor(html)
