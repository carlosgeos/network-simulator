#!/usr/bin/python
# -*- coding: utf8 -*-

#import libraries
from random import randint # integer in a range
from random import random # float in range [0.0; 1.0]
from random import choice # random element from a list

# ----------------- Initialization ---------------------------------------------
# CONSTANTS
RUMOR_LENGTH = 8 # values on RUMOR_LENGTH bits
RUMOR_MAX = (1<<RUMOR_LENGTH)-1  # max value on RUMOR_LENGTH bits

NO_RUMOR = -1 # default value when the person does not know the rumor yet
NO_FRIENDS = -1
SIMULATE_FULL_PROPAGATION = -1

MODIFICATION_PROBABILITY = 0.1 # default modification probability
MIX_KEEP_OWN_PROBABILITY = 0.9 # probability to keep own bit value for MIXTURE

# init Functions
def initRumors(size):
	return [NO_RUMOR for i in range(size)]

def initSystem(filename):
	names, network = loadNetwork(filename)
	rumors = initRumors(len(names))
	return rumors, names, network

# --------------- network functions --------------------------------------------

def saveNetwork(filename,person,network):
	"""This function save a social network to a file (filename given as parameter)"""
	pfile = open(filename,'w')
	for current in person:
		currentID	= idOf(current,person)
		neighbors	= []
		for other in person:
			otherID	= idOf(other,person)
			if(areFriends(network,currentID,otherID)):
				neighbors.append(other)
		print(current + ' : ' + (', '.join(neighbors)),file=pfile)
	pfile.close()

def loadNetwork(filename):
	"""This function loads a social network from a file (filename given as parameter)
	Return value: a coule of elements: list of names, matrix of connections"""
	#init
	nFile = open(filename)
	namesDict = {}
	friends = []
	curId = 0
	
	#extract info from file
	for line in nFile:
		#extract person's name
		index = line.find(":")
		name = line[0:index].strip()
		namesDict[name] = curId
		#extract persons friends
		friends.append(line[index+1:].strip().split(","))
		curId+=1
	
	# constructed as a bottom left corner triangle matrix
	network = [[False for j in range(i)] for i in range(curId)] 
	names = ["" for j in range(curId)]
	
	for key in namesDict:
		index = namesDict[key]
		names[index] = key
		#go through friends
		for friend in friends[index]:
			setAsFriends(network, index, namesDict[friend.strip()])
			
	return (names, network)

def areFriends(network, idx0, idx1):
	"""Returns True iff a person with index idx0 is a friend
	of a person with index idx1. A person is not a friend with himself (herself)."""
	res = False
	if idx0>idx1:
		res = network[idx0][idx1]
	elif idx0<idx1:
		res = network[idx1][idx0]
	return res

def setAsFriends(network, idx0, idx1):
	""" This funciton sets persons with ids id0 and id1 as friends in the social network.
	It is impossible to set a person as a friend with himself/herself.
	"""
	if idx0>idx1:
		network[idx0][idx1] = True
	elif idx0<idx1:
		network[idx1][idx0] = True

def idOf(person, names):
	"""
	returns the index of a person in list of names.
	"""
	id = 0
	GO = True
	while id < len(names) and GO:
		if names[id] == person:
			GO=False
		id+=1
	if GO: # person is not in the list
		id = 0
	return id-1

# ----------------- printing functions -----------------------------------------

def printRumorState(names, rumors):
	"""This function prints list of people and the rumor that they know"""
	print("{0:16}{1:10}{2:5}".format("NAME","BIN","DEC"))
	for i in range(len(names)):
		print("{0:<16}".format(names[i]), end="")
		if(rumors[i] == NO_RUMOR):
			print("-- Does not know --")
		else:
			print("{0:0>8b}{1:5}".format(rumors[i], rumors[i]))
	

def printNames(names, separator="\n"):
	"""This function prints a list of all people in the network
	If optional parameter is specified it is used as a separator
	between people's names."""
	for name in names:
		print(name, end=separator)
	
def printFriends(network, names):
	"""
	Function prints the social network in form of lists of friends of each person
	"""
	for i in range(len(names)):
		print(names[i],end=': ')
		firstFriendDone = False
		for j in range(len(names)):
			if (areFriends(network,i,j)):
				if (firstFriendDone):
					print(end=", ")
				print(names[j], end="")
				firstFriendDone = True
		
		print() #end line
		
def printRawNetwork(network):
	"""This function prints the raw matrix of friends in the network.
	This is very useful debugging tool."""
	print(end="  ")
	for i in range(len(network)): print(chr((ord('A')+i)%26), end=" ")
	print()
	
	for i in range(len(network)):
		print(chr((ord('A')+i)%26), end=" ")
		for j in range(len(network)):
			if areFriends(network, i, j):
				print("T", end=" ")
			else:
				print("F", end=" ")
		print()
	
# ------------------------------- Rumor propagation --------------------------------------

def getNewRumor(modifFunc, probability, replFunc, rumorNew, rumorOld):
	"""
	This funciton returns a new rumor for a person.
	The new rumor might be modified and mixed with previously known rumor.
	"""
	result = modifyRumor(rumorNew, modifFunc, probability)
	if rumorOld != NO_RUMOR:
		result = replFunc(rumorOld, result)
	return result

def getRandomFriendId(id, network, rumors, includeAlreadyKnows = False):
	"""
	This function return a random index of a person's (id) friend
	"""
	friends = []
	for i in range(len(network)):
		if areFriends(network, id, i):
			# does not know OR tell everybody:
			if rumors[i] == NO_RUMOR or includeAlreadyKnows:
				friends.append(i)
	
	if len(friends) > 0:
		friendId = choice(friends)
	else:
		friendId = NO_FRIENDS
	return friendId

def propagateRumor(network, rumors, modifFunc, probability, replFunc, tellAgain,selection=getRandomFriendId):
	"""This function propagates the rumor 1 time from each person that already knows it."""
	newRumors = list(rumors)
	newlyInformedPeopleNbr = 0
	for i in range(len(rumors)):
		if rumors[i] != NO_RUMOR:
			id = selection(i, network, rumors, tellAgain)
			if id != NO_FRIENDS:
				if newRumors[id] == NO_RUMOR: # before the person did not know about the rumor
					newlyInformedPeopleNbr+=1
				newRumors[id]=getNewRumor(modifFunc, probability, replFunc, rumors[i], rumors[id])
	rumors[:] = newRumors
	return newlyInformedPeopleNbr


# ------------ rumor modification functions ------------------------------------
def noModification(rumorValue):
	"""
	returns rumor without modification
	"""
	return rumorValue # this implementation of modifications allows adding new strategies

def incrementalModify(rumorValue):
	"""
	This function returns the rumorValue incremented or decremented (with 50% / 50% chance)
	"""
	return (rumorValue+int((randint(0,1)-0.5)*2)) % (RUMOR_MAX +1) # gives +1 or -1 mod 256
	
def bitflipModify(rumorValue):
	""" This function returns the rumorValue with a random bit flipped
	"""
	return rumorValue^(1<<randint(0,RUMOR_LENGTH-1)) # flips a random bit using XOR
	
def modifyRumor(rumor, modificationFunc, probability):
	"""
	This function returns a value of a rumor modified using modification function
	with the probability given as a parameter
	"""
	newRumor = rumor
	if (random()<probability):
		newRumor = modificationFunc(rumor)
	
	return newRumor

# ------------------ rumor replacement strategies ----------------------------------
# this way of implementing strategies allows to easily add new strategies

def randomRumor(rumorOld, rumorNew):
	"""
	This function return randomly either the old or the new rumor
	"""
	return choice([rumorOld, rumorNew])

def mixRumors(rumorOld, rumorNew):
	"""
	This function mixes two rumors bit by bit and return a new resulting rumor.
	If a bit of rumor0 and rumor1 are identical its value stays the same,
	if it's not then a random value is chosen.
	"""
	result = rumorOld&rumorNew # keep identical bits
	diff = rumorOld^rumorNew # different bits
	for i in range(RUMOR_LENGTH):
		if diff % 2 == 1:
			rumorTmp = rumorOld
			if random() > MIX_KEEP_OWN_PROBABILITY: # take a bit from New Rumor
				rumorTmp = rumorNew
			result = result | (rumorTmp & (1 << i))
		diff = diff>>1 # shift right
	return result

def stableRumor(rumorOld, rumorNew):
	return rumorOld	
	
def rewriteRumor(rumorOld, rumorNew):
	return rumorNew
