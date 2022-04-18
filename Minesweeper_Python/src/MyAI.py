# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from pickle import FALSE
from re import T
from AI import AI
from Action import Action

class Tile():
	x = 0
	y = 0
	covered = True
	flagged = False
	percept_number = 0				# 
	effective_number = 0	# effective_number = percept_number - flagged neighbors


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		print("hello world")
		self.rows = rowDimension
		self.cols = colDimension
		self.mines = totalMines
		self.tiles = {}
		self.last_action = "NULL"	# Options are "FLAG", "UNCOVER", "UNFLAG"
		self.last_tile = (startX, startY) # The last tile to have an action performed on it
		self.UNCOVER = 1
		self.FLAG = 2
		self.UNFLAG = 3
		for i in range(1, self.cols+1):
			for j in range(1, self.rows+1):
				t = Tile()
				t.x = i
				t.y = j 
				self.tiles[(i, j)] = t
		self.uncoveredTile(startX, startY, 0)




		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		
		# loop through all tiles we have and if we have a "rule of thumb",
		# take action to uncover (when effective number is 0 and we still have (covered && unflagged) neighbors) 
		# or flag (when effective number is equal to uncovered neighbors, non-zero)
		
		########################################################################
		if self.last_action == "UNCOVER":
			self.tiles[self.last_tile].percept_number = number
			self.tiles[self.last_tile].effective_number = number - self.getNeighborsFlagged(self.last_tile[0], self.last_tile[1])
		elif self.last_action == "FLAG": #Maybe move down to when we're actively flagging tiles
			for tile in self.getNeighborsUncovered(self.last_tile[0], self.last_tile[1]):
				self.tiles[self.last_tile].effective_number -= 1
				

		
		for tile in self.tiles:
			if tile.effective_number == 0:
				neighbors = self.getNeighborsCoveredAndUnflagged(tile.x, tile.y)
				if neighbors:
					return Action(self.UNCOVER, neighbors[0].x, neighbors[0].y)
			
			covered_neighbors = self.getNeighborsCovered(tile.x, tile.y)
			if (tile.effective_number != 0) and (tile.effective_number == len(covered_neighbors)):
				return Action(self.FLAG, covered_neighbors[0].x, covered_neighbors[0].y)




		
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	# returns a list of the Tiles at all 8 surrounding tiles of target (x,y), or fewer if the target is at an edge, ordered clockwise starting at top left tile
	def getNeighbors(self, x, y):
		differentials = [
			(-1, 1),
			(0, 1),
			(1, 1),
			(1, 0),
			(1, -1),
			(0, -1),
			(-1, -1),
			(-1, 0)
		]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 1) and (newY >= 1) and (newX <= self.cols) and (newY <= self.rows):
				neighbors.append(self.tiles[newX,newY])
		return neighbors
		
	def getNeighborsActive(self, x, y): #returns neighbors who are uncovered, flagged, or with a non-zero effective_number
		pass
		

	def getNeighborsCovered(self, x, y):
		differentials = [
			(-1, 1),
			(0, 1),
			(1, 1),
			(1, 0),
			(1, -1),
			(0, -1),
			(-1, -1),
			(-1, 0)
		]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 1) and (newY >= 1) and (newX <= self.cols) and (newY <= self.rows) and (self.tile[newX, newY].covered == True):
				neighbors.append(self.tiles[newX,newY])
		return neighbors

	def getNeighborsFlagged(self, x, y):
		differentials = [
			(-1, 1),
			(0, 1),
			(1, 1),
			(1, 0),
			(1, -1),
			(0, -1),
			(-1, -1),
			(-1, 0)
		]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 1) and (newY >= 1) and (newX <= self.cols) and (newY <= self.rows) and (self.tile[newX, newY].flagged == True):
				neighbors.append(self.tiles[newX,newY])
		return neighbors

	def getNeighborsCoveredAndUnflagged(self, x, y):
		differentials = [
			(-1, 1),
			(0, 1),
			(1, 1),
			(1, 0),
			(1, -1),
			(0, -1),
			(-1, -1),
			(-1, 0)
		]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 1) and (newY >= 1) and (newX <= self.cols) and (newY <= self.rows) and (self.tile[newX, newY].covered == True) and (self.tile[newX, newY].flagged == False):
				neighbors.append(self.tiles[newX,newY])
		return neighbors

	def getNeighborsUncovered(self, x, y):
		differentials = [
			(-1, 1),
			(0, 1),
			(1, 1),
			(1, 0),
			(1, -1),
			(0, -1),
			(-1, -1),
			(-1, 0)
		]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 1) and (newY >= 1) and (newX <= self.cols) and (newY <= self.rows) and (self.tile[newX, newY].covered == False):
				neighbors.append(self.tiles[newX,newY])
		return neighbors
		
	def getTile(self, x, y):
		return self.tiles[x, y]

	# after flagging a tile, use this helper function to update our database
	def flaggedTile(self, x, y):
		if (self.tiles[x,y].flagged == True):
			print("FLAGGING ERROR: Tile at (" + str(x) + ", " + str(y) + ") already flagged!")
		else:
			self.tiles[x,y].flagged = True
	
	# after unflagging a tile, use this helper function to update our database
	def unflaggedTile(self, x, y):
		if (self.tiles[x,y].flagged == False):
			print("UNFLAGGING ERROR: Tile at (" + str(x) + ", " + str(y) + ") already unflagged!")
		else:
			self.tiles[x,y].flagged = False

	# after uncovering a tile, use this helper function to update our database
	def uncoveredTile(self, x, y, label):
		if (self.tiles[x,y].covered == False):
			print("UNCOVERING ERROR: Tile at (" + str(x) + ", " + str(y) + ") already uncovered!")
		else:
			self.tiles[x,y].covered = False
			self.tiles[x,y].percept_number = label
		# should we update effective number immediately? probably
	
			
		