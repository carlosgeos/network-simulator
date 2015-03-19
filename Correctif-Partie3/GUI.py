#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as Tk

try:
	import tkinter.ttk as TTk
except:
	import tkinter as Tk

from tkinter import font as tkFont

from tkinter import filedialog as tkFileDialog
from tkinter import simpledialog as tkSimpleDialog
from tkinter import messagebox as tkMessageBox

import random,time

import rumorFunctions as Core

from Person import *
from Link import *
from NetworkFrame import *

class GUI(TTk.Frame):
	DEFAULT_DELAY		= 0.5
	DEFAULT_MUTATION	= 0.5
	DEFAULT_THEME		= 'aqua'
	def __init__(self, master=None):
		""" Construct the window of the Rumor application """
		style = TTk.Style()
		if(GUI.DEFAULT_THEME in style.theme_names()):
			style.theme_use(GUI.DEFAULT_THEME)
		TTk.Frame.__init__(self,master)
		Core.RUMOR_LENGTH					= 24
		Core.RUMOR_MAX						= (1<<Core.RUMOR_LENGTH)-1
		Core.MODIFICATION_PROBABILITY	= GUI.DEFAULT_MUTATION
		Core.NO_RUMOR						= 0
		self.delay		= GUI.DEFAULT_DELAY
		self.canvas		= None
		self.infoName	= Tk.StringVar(value=' ')
		self.steps		= Tk.StringVar(value='0')
		self.labelFont	= tkFont.Font(underline=1)
		self.ties = self.strategy	= 'random'
		self.error		= 'none'
		self.master.title("Network")
		self.menu		= self.createMenuBar()
		self.info		= self.createInfoPanel()
		self.content	= self.createContentPanel()
		self.menu		= self.createMenuPanel()
		self.pack(fill=Tk.BOTH,expand=True)
		#self.example()
		self.canvas.redraw()
	def clean(self):
		""" Clean the network by removing all friendships and all persons """
		for edge in self.canvas.edges:
			edge.delete()
		for node in self.canvas.nodes:
			node.delete()
		self.canvas.redraw()
	def example(self):
		""" Create a sample network with a rumor """
		nodes		= []
		edges		= []
		for node in range(1,21):
			nodes.append(Person(node,self.canvas))
		for i in range(0,len(nodes)-1):
			edges.append(Link(self.canvas,nodes[i],nodes[i+1]))
		nodes[5].setColor('#099099')
		self.canvas.nodes = nodes
		self.canvas.edges = edges
	def random_strategy(self):
		""" Select randomly a neighbor to propage a rumor """
		return Core.getRandomFriendId
	def updateInfoPanel(self,node):
		""" Update the name displayed onto the information panel """
		self.infoName.set(node.identifier)
	def resetStep(self):
		""" Reset (to 0) the steps counter """
		self.updateStep(0)
	def updateStep(self,value):
		""" Update the current number of steps """
		self.steps.set(str(value))
	def countSteps(self):
		""" Count the number of steps """
		return int(self.steps.get().strip())
	def updateTie(self,event):
		""" Change the replication function according to a specific event """
		selected = list(map(int, event.widget.curselection()))
		if(selected):
			self.ties = event.widget.get(selected[0]).lower()
	def updateStrategy(self,event):
		""" Change the selection function according to a specific event """
		selected = list(map(int, event.widget.curselection()))
		if(selected):
			self.strategy = event.widget.get(selected[0]).lower()
	def updateError(self,event):
		""" Change the modification (error) function according to a specific event """
		selected = list(map(int, event.widget.curselection()))
		if(selected):
			self.error = event.widget.get(selected[0]).lower()
	def createInfoPanel(self):
		""" Create the information panel which will dislay the number of steps and the name of the node """
		panel = TTk.LabelFrame(self,width=100, text='Person information')
		panel.pack(side=Tk.RIGHT, fill=Tk.Y)
		TTk.Label(panel,text='Name :',font=self.labelFont).pack()
		infoName = TTk.Label(panel,textvariable=self.infoName)
		infoName.pack()
		TTk.Separator(panel,orient=Tk.HORIZONTAL).pack()
		TTk.Label(panel,text='Number of steps :',font=self.labelFont).pack()
		steps = TTk.Label(panel,textvariable=self.steps)
		steps.pack()
		return panel
	def createContentPanel(self):
		""" Create the panel which will contains the drawing canvas """
		scroll = TTk.Scrollbar(self)
		self.canvas = NetworkFrame(scroll)
		self.canvas.pack(fill=Tk.BOTH,expand=True)
		scroll.pack(fill=Tk.BOTH,expand=True)
		return self.canvas
	def updateLayout(self,event):
		""" Change the layout used to place person on the drawing canvas """
		selected = list(map(int, event.widget.curselection()))
		if(selected):
			self.canvas.setLayout(event.widget.get(selected[0]).lower())
			self.canvas.redraw()
	def updatePersonWidth(self,event):
		""" Change the width of drawn person """
		Person.WIDTH = int(event)
		self.canvas.redraw()
	def updateDelay(self,event):
		""" Change the delay between two consecutive propagations during the automatic mode """
		self.delay = float(event)
	def updateMutation(self,event):
		""" Change the probablity of modification (error function) """
		Core.MODIFICATION_PROBABILITY = float(event)
	def updateEdgeWidth(self,event):
		""" Change the width of drawn edges """
		Link.WEIGHT = int(event)
		self.canvas.redraw()
	def random_policy(self):
		""" random policy as rumors selection """
		return Core.randomRumor
	def mixture_policy(self):
		""" mixture policy as rumors selection """
		return Core.mixRumors
	def stable_policy(self):
		""" stable policy as rumors selection """
		return Core.stableRumor
	def rewrite_policy(self):
		""" rewrite policy as rumors selection """
		return Core.rewriteRumor
	def propagate(self):
		""" Propage rumors in the network """
		if(len(self.canvas.nodes) < 1):
			tkMessageBox.showwarning("Propagation","No nodes in the network.")
			return
		if(self.countColors() < 1):
			tkMessageBox.showinfo("Propagation","No enough color to continue")
			return
		nodes,links	= self.getData()
		rumors		= list(map(lambda node: int(node.toRGB()[1:],16),self.canvas.nodes))
		decision		= eval('self.'+self.ties+'_policy()')
		neighbor		= eval('self.'+self.strategy+'_strategy()')
		error			= eval('self.'+self.error+'_error()')
		Core.propagateRumor(links, rumors, error, Core.MODIFICATION_PROBABILITY, decision, True,neighbor)
		for (i,node) in enumerate(self.canvas.nodes):
			node.setColor(rumors[i])
		self.updateStep(self.countSteps() + 1)
	def none_error(self):
		""" no modification function """
		return Core.noModification
	def incremental_error(self):
		""" incremental modification function """
		return Core.incrementalModify
	def bitflip_error(self):
		""" bitflip modification function """
		return Core.bitflipModify
	def countColors(self):
		""" the the number of colors (rumors) """
		return len(set(filter(lambda node:node.politics != Core.NO_RUMOR,self.canvas.nodes)))
	def autoPropagate(self,grab=None,k=-1):
		""" Open a Dialog box and perfom k times a propagation of rumors in the network """
		if(len(self.canvas.nodes) < 1):
			tkMessageBox.showwarning("Propagation","No nodes in the network.")
			return
		if(self.countColors() > 0):
			if(k > 0):
				time.sleep(self.delay)
				self.propagate()
				self.after(int(self.delay * 1000), self.autoPropagate,grab,k-1)
				return
			elif(k < 0):
				result = tkSimpleDialog.askinteger("Running k steps", "Enter the number of steps to perform",initialvalue=1,minvalue=1)
				if(result):
					grab = TTk.Frame()
					grab.grab_set()
					self.after(1, self.autoPropagate,grab,int(result))
					return
		else:
			tkMessageBox.showinfo("Propagation","No enough color to continue")
		if(grab):
			grab.grab_release()
	def createMenuPanel(self):
		"""  The menu panel which contain all button, scaler, ... """
		panel = TTk.Frame(height = 50)
		#
		named = TTk.LabelFrame(panel,text='Network Layout')
		layouts = Tk.Listbox(named,exportselection=0,height=3,width=12,selectmode=Tk.SINGLE)
		layouts.insert(Tk.END,"Circular")
		layouts.insert(Tk.END,"Shell")
		layouts.insert(Tk.END,"Random")
		layouts.select_set(0)
		layouts.bind('<<ListboxSelect>>', self.updateLayout)
		layouts.pack()
		named.pack(side=Tk.LEFT,fill=Tk.Y, expand=True)
		#
		named = TTk.LabelFrame(panel,text='Person width')
		nodeWidth = Tk.Scale(named,command=self.updatePersonWidth,orient=Tk.VERTICAL,relief=Tk.SOLID,variable=Tk.IntVar,
							  from_=1,to=50,showvalue=False)
		nodeWidth.set(Person.WIDTH)
		nodeWidth.pack()
		named.pack(side=Tk.LEFT,fill=Tk.Y, expand=True)
		#
		named = TTk.LabelFrame(panel,text='Edge width')
		edgeWidth = Tk.Scale(named,command=self.updateEdgeWidth,orient=Tk.VERTICAL,relief=Tk.SOLID,variable=Tk.IntVar,
							  from_=1,to=10,showvalue=False)
		edgeWidth.set(Link.WEIGHT)
		edgeWidth.pack()
		named.pack(side=Tk.LEFT,fill=Tk.Y, expand=True)
		#
		named = TTk.LabelFrame(panel,text='Delay')
		delay = Tk.Scale(named,command=self.updateDelay,orient=Tk.VERTICAL,relief=Tk.SOLID,variable=Tk.DoubleVar,
							  from_=0.0,to=5.0,resolution=0.1,showvalue=False)
		delay.set(GUI.DEFAULT_DELAY)
		delay.pack()
		named.pack(side=Tk.LEFT,fill=Tk.Y, expand=True)
		#
		named = TTk.LabelFrame(panel,text='Selection Policy')
		strategy = Tk.Listbox(named,exportselection=0,height=3,width=12,selectmode=Tk.SINGLE)
		strategy.insert(Tk.END,"Random")
		strategy.select_set(0)
		strategy.bind('<<ListboxSelect>>', self.updateStrategy)
		strategy.pack()
		named.pack(side=Tk.LEFT,fill=Tk.Y, expand=True)
		#
		named = TTk.LabelFrame(panel,text='Error Function')
		error = Tk.Listbox(named,exportselection=0,height=3,width=12,selectmode=Tk.SINGLE)
		error.insert(Tk.END,"None")
		error.insert(Tk.END,"Incremental")
		error.insert(Tk.END,"BitFlip")
		error.select_set(0)
		error.bind('<<ListboxSelect>>', self.updateError)
		error.pack()
		prob = Tk.Scale(named,command=self.updateMutation,orient=Tk.HORIZONTAL,relief=Tk.SOLID,variable=Tk.DoubleVar,
							  from_=0.0,to=1.0,resolution=0.1,showvalue=True)
		prob.set(GUI.DEFAULT_MUTATION)
		prob.pack()
		named.pack(side=Tk.LEFT,fill=Tk.Y, expand=True)
		#
		named = TTk.LabelFrame(panel,text='Update Policy')
		tie = Tk.Listbox(named,exportselection=0,height=4,width=12,selectmode=Tk.SINGLE)
		tie.insert(Tk.END,"Random")
		tie.insert(Tk.END,"Stable")
		tie.insert(Tk.END,"Rewrite")
		tie.insert(Tk.END,"Mixture")
		tie.select_set(0)
		tie.bind('<<ListboxSelect>>', self.updateTie)
		tie.pack()
		named.pack(side=Tk.LEFT,fill=Tk.Y, expand=True)
		#
		named = TTk.Frame(panel)
		TTk.Button(named, text="New node", command=self.canvas.addPerson).pack()
		TTk.Button(named, text="Propagate", command=self.propagate).pack()
		TTk.Button(named, text="Run", command=self.autoPropagate).pack()
		TTk.Button(named, text="Reset steps", command=self.resetStep).pack()
		named.pack(side=Tk.LEFT,fill=Tk.Y, expand=True)
		#
		panel.pack(side=Tk.BOTTOM, fill=Tk.X)
		return panel
	def loadNetwork(self):
		""" GUI action to load a network from a file through a Dialog box """
		result = tkFileDialog.askopenfilename(defaultextension='.rn',\
				title="Choose a source file",\
				filetypes=[('Rumor Network File','*.rn')])
		if(result):
			nodes,links = Core.loadNetwork(result)
			self.clean()
			self.canvas.nodes = list(map(lambda node:Person(node,self.canvas),nodes))
			self.canvas.edges = []
			for i in range(len(links)-1):
				for j in range(i+1,len(links)):
					if(i!=j and Core.areFriends(links,i,j)):
						self.canvas.edges.append(Link(self.canvas,self.canvas.nodes[i],self.canvas.nodes[j]))
			self.canvas.redraw()
	def getData(self):
		""" Get the network data as a tuple of the list of person  """
		nodes = list(map(lambda node: str(node.identifier) ,self.canvas.nodes))
		links = [ [False] * i for i in range(len(nodes)) ]
		for edge in self.canvas.edges:
			a,b = edge.getIdentifier().split(',')
			a = Core.idOf(a,nodes)
			b = Core.idOf(b,nodes)
			Core.setAsFriends(links,a,b)
		return nodes,links
	def saveNetwork(self):
		""" GUI action to save a network to a file through a Dialog box """
		result = tkFileDialog.asksaveasfilename(defaultextension='.rn',\
				title="Choose a destination",\
				filetypes=[('Rumor Network File','*.rn')])
		if(result):
			nodes,links = self.getData()
			Core.saveNetwork(result,nodes,links)
	def createMenuBar(self):
		""" Create the GUI menu bar """
		bar = Tk.Menu(self)
		menu = Tk.Menu(bar, tearoff=0)
		bar.add_cascade(label="File", menu=menu,accelerator="^F")
		menu.add_command(label="Load",accelerator="^O",command=self.loadNetwork)
		menu.add_command(label="Save",accelerator="^S",command=self.saveNetwork)
		menu.add_separator()
		menu.add_command(label="Quit",accelerator="^Q",command=self.quit)

		menu = Tk.Menu(bar, tearoff=0)
		bar.add_cascade(label="Help", menu=menu)
		menu.add_command(label="Manual")
		menu.add_command(label="About")
		
		self.master.config(menu=bar)

		return bar

if(__name__ == '__main__'):
	app	= GUI()
	app.mainloop()
