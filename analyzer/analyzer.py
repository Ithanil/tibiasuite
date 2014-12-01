import sys
from pylab import *
import copy

def sumstrings(stringarr):
	sumstring = ""
	for string in stringarr:
		string = string.strip()
		if (string != "") and (sumstring != ""):
			sumstring += " "
		sumstring += string
	return sumstring

def clockmins(clocktime):
	print clocktime
	clocksplit = clocktime.strip().split(":")
	return 60*int(clocksplit[0]) + int(clocksplit[1])

class Entity:

	count = 0

	def __init__(self, name, unique, killed = 0, dmggot = 0, dmgdone = 0, healdone = 0, healgot = 0, expgot = 0, loot = []):
		self.name = name
		self.unique = unique # distinguish unique players/boss mobs from non-unique normal mobs

		self.killed = killed
		self.dmggot = dmggot
		self.dmgdone = dmgdone
		self.healdone = healdone
		self.healgot = healgot
		self.expgot = expgot
		self.loot = loot
		
		Entity.count += 1

	def add_loot(self, lootitem):
		for item in self.loot:
			if item.name == lootitem.name:
				item.add(lootitem.number)
				return
		self.loot.append(lootitem)
				
	def add_values(self, entity):
		self.killed += entity.killed
		self.dmggot += entity.dmggot
		self.dmgdone += entity.dmgdone
		self.healdone += entity.healdone
		self.healgot += entity.healgot
		self.expgot += entity.expgot
		for lootitem in entity.loot:
			self.add_loot(lootitem)

	def printall(self):
		print("---  Entity Report  ---")
		print("Name     :   "+self.name)
		print("unique?  :   "+str(self.unique))
		print("# killed :   "+str(self.killed))
		print("DMG_in   :   "+str(self.dmggot))
		print("DMG_out  :   "+str(self.dmgdone))
		print("HEAL_in  :   "+str(self.healgot))
		print("HEAL_out :   "+str(self.healdone))
		print("EXP      :   "+str(self.expgot))
		print("\n")
#		print("Lootlist :")
#		print(self.loot)

class Item:

	count = 0
	
	def __init__(self, name, number = 0):
		self.name = name
		
		self.number = number
		
		Item.count +=1

	def add(self, addnumber):
		self.number += addnumber

	def remove(self, delnumber):
		self.number -= delnumber



def addEntity(entitylist, newentity):
	listnames = []
	for entity in entitylist:
		listnames.append(entity.name)

	if newentity.name in listnames:
		entindex = listnames.index(newentity.name)
		entitylist[entindex].add_values(newentity)
	else:
		entitylist.append(newentity)


def line_analyze(line, entitylist):
	splitline = line.replace(".","").replace("\n","").split(" ")
	#	print(clockmins(splitline[0]))
	if ("hitpoints" in splitline):# or ("mana" in splitline):
		if "healed" in splitline:
			healed_keyword(line, entitylist)
		elif "lose" in splitline:
			lose_keyword(line,entitylist,"lose")
		elif "loses" in splitline:
			lose_keyword(line,entitylist, "loses")
	elif ("experience" in splitline) and ("gained" in splitline):
		gain_keyword(line, entitylist)
	elif ("Loot" in splitline):
		loot_keyword(line, entitylist)

def healed_keyword(line, entitylist):
	healsplit = line.split("healed")
	
	leftside = healsplit[0].strip().split(" ")
	rightside = healsplit[1].strip().split(" ")
	
	if "were" in leftside:
		leftsplit = sumstrings(leftside).split("were")
		leftsplit = leftsplit[0].strip().split(" ")
	elif "was" in leftside:
		leftsplit = sumstrings(leftside).split("was")
		leftsplit = leftsplit[0].strip().split(" ")
	else:
		leftsplit = leftside

	if (leftsplit[1] == "A") or (leftsplit[1] == "An"):
		healedEntity = Entity(sumstrings(leftsplit[2:]), False)
	else:
		healedEntity = Entity(sumstrings(leftsplit[1:]), True)

#	print(healedEntity)
	rightsplit = sumstrings(rightside).split("for")
	
	doerstr = rightsplit[0].strip()
	if (doerstr=="yourself") or (doerstr=="itself") or (doerstr=="himself") or (doerstr=="herself"):
		healingEntity = copy.deepcopy(healedEntity)
	else:
		doersplit = doerstr.split(" ")
		if "by" in doersplit:
			if (doersplit[1] == "a") or (doersplit[1] == "an"):
				healingEntity = Entity(sumstrings(doersplit[2:]), False)
			else:
				healingEntity = Entity(sumstrings(doersplit[1:]), True)
		else:
			healingEntity = None

	healvalue = int(rightsplit[1].strip().split(" ")[0])
	healedEntity.healgot += healvalue
	addEntity(entitylist, healedEntity)

	if healingEntity is not None:
		healingEntity.healdone += healvalue
		addEntity(entitylist, healingEntity)


def lose_keyword(line, entitylist, splitword):
	
	dmgsplit = line.split(splitword)
	
	leftside = dmgsplit[0].strip().split(" ")
	rightside = dmgsplit[1].strip().split(" ")
	
	if (leftside[1] == "A") or (leftside[1] == "An"):
		dmgedEntity = Entity(sumstrings(leftside[2:]), False)
	else:
		dmgedEntity = Entity(sumstrings(leftside[1:]), True)
	
	if "due" in rightside:
		if "your" in rightside:
			dmgingEntity = Entity("You", True)
		else:
			rightsplit = sumstrings(rightside).split("due to an attack by")
		
			doersplit = rightsplit[1].replace(".","").strip().split(" ")
			if (doersplit[0] == "a") or (doersplit[0] == "an"):
				dmgingEntity = Entity(sumstrings(doersplit[1:]), False)
			else:
				dmgingEntity = Entity(sumstrings(doersplit[0:]), True)
	else:
		dmgingEntity = None

	dmgvalue = int(rightside[0])

	dmgedEntity.dmggot += dmgvalue
	addEntity(entitylist, dmgedEntity)
	
	if dmgingEntity is not None:
		dmgingEntity.dmgdone += dmgvalue
		addEntity(entitylist, dmgingEntity)

def gain_keyword(line, entitylist):
	expsplit = line.split("gained")
	leftside = expsplit[0].strip().split(" ")
	rightside = expsplit[1].strip().split(" ")

	if (leftside[1] == "A") or (leftside[1] == "An"):
		expingEntity = Entity(sumstrings(leftside[2:]), False)
	else:
		expingEntity = Entity(sumstrings(leftside[1:]), True)

	expvalue = int(rightside[0])
	expingEntity.expgot += expvalue
	addEntity(entitylist, expingEntity)

def loot_keyword(line, entitylist):
	lootsplit = line.split(":")
	namesplit = lootsplit[2].strip().split(" ")
	lootlist = lootsplit[3].strip().split(" ")
	if (namesplit[2] == "a") or (namesplit[2] == "an"):
		lootEntity = Entity(sumstrings(namesplit[3:]), False, killed=1)
	else:
		lootEntity = Entity(sumstrings(namesplit[2:]), True, killed=1)
	addEntity(entitylist, lootEntity)
#	------------------------------------------------------------------------	#

youentity = Entity("You", True)
entitylist = [youentity]	# players and monsters


if len(sys.argv)>=2:
	
	logfile=open(sys.argv[1],'r')
	for line in logfile:
		line_analyze(line, entitylist)

	for entity in entitylist:
		entity.printall()
else:
	print("At least one argument is needed: The name of the server log file.")

entitylist.sort()
print("You gained "+str(youentity.expgot)+" experience points.")