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
	x = None
	y = None
	covered = True
	flagged = False 
	percept_number = None
	effective_number = None		# effective_number = percept_number - flagged neighbors

class MyAI( AI ):
	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.rows = rowDimension
		self.cols = colDimension
		self.mines = totalMines
		self.tiles = {}
		self.last_action = "NULL"			# AI.Actions.[ACTION]
		self.last_tile = (startX, startY) 	# The last tile to have an action performed on it
		for i in range(0, self.cols):
			for j in range(0, self.rows):
				t = Tile()
				t.x = i
				t.y = j 
				self.tiles[(i, j)] = t
		print(str(startX) + ", " + str(startY));
		self.uncoveredTile(startX, startY, 0)
		self.tiles[(startX, startY)].effective_number = 0;
		
	def getAction(self, number: int) -> "Action Object":
		# Updating our database after every turn
		if self.last_action == AI.Action.UNCOVER:
			self.uncoveredTile(self.last_tile[0], self.last_tile[1], number)
		elif self.last_action == AI.Action.FLAG:
			self.flaggedTile(self.last_tile[0], self.last_tile[1])
			self.updateEffectiveNumberOfNeighbors(self.last_tile[0], self.last_tile[1])

				

		# Rule of Thumb
			# loop through all tiles we have and if we have a "rule of thumb",
			# take action to uncover (when effective number is 0 and we still have (covered && unflagged) neighbors) 
			# or flag (when effective number is equal to uncovered neighbors, non-zero) and decrement effective number
		for pair in self.tiles:
			tile = self.tiles[pair]
			if tile.effective_number == 0:
				neighbors = self.getNeighborsCoveredAndUnflagged(tile.x, tile.y)
				if neighbors:
					self.updateLast(AI.Action.UNCOVER, neighbors[0].x, neighbors[0].y)
					return Action(AI.Action.UNCOVER, neighbors[0].x, neighbors[0].y)
			if (tile.covered == False):
				covered_neighbors = self.getNeighborsCoveredAndUnflagged(tile.x, tile.y)
				self.updateEffectiveNumberOfCell(tile.x, tile.y)
				if (tile.effective_number != 0) and (tile.effective_number == len(covered_neighbors)):
					self.updateLast(AI.Action.FLAG, covered_neighbors[0].x, covered_neighbors[0].y)
					return Action(AI.Action.FLAG, covered_neighbors[0].x, covered_neighbors[0].y)
		return Action(AI.Action.LEAVE)

	# returns a list of the Tiles at all 8 surrounding tiles of target (x,y), or fewer if the target is at an edge, ordered clockwise starting at top left tile
	def getNeighbors(self, x, y):
		differentials = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 0) and (newY >= 0) and (newX <= self.cols-1) and (newY <= self.rows-1):
				neighbors.append(self.tiles[(newX,newY)])
		return neighbors
		
	def getNeighborsActive(self, x, y): #returns neighbors who are uncovered, flagged, or with a non-zero effective_number
		pass
		
	
	def getNeighborsCovered(self, x, y):
		differentials = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 0) and (newY >= 0) and (newX <= self.cols -1) and (newY <= self.rows-1) and (self.tiles[(newX, newY)].covered == True):
				neighbors.append(self.tiles[(newX,newY)])
		return neighbors

	def getNeighborsFlagged(self, x, y):
		differentials = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 0) and (newY >= 0) and (newX <= self.cols-1) and (newY <= self.rows-1) and (self.tiles[(newX, newY)].flagged == True):
				neighbors.append(self.tiles[(newX,newY)])
		return neighbors

	def getNeighborsCoveredAndUnflagged(self, x, y):
		differentials = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 0) and (newY >= 0) and (newX <= self.cols-1) and (newY <= self.rows-1) and (self.tiles[(newX, newY)].covered == True) and (self.tiles[(newX, newY)].flagged == False):
				neighbors.append(self.tiles[(newX,newY)])
		return neighbors

	def getNeighborsUncovered(self, x, y):
		differentials = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
		neighbors = []
		for col, row in differentials:
			newX = x + col
			newY = y + row
			if (newX >= 0) and (newY >= 0) and (newX <= self.cols-1) and (newY <= self.rows-1) and (self.tiles[(newX, newY)].covered == False):
				neighbors.append(self.tiles[(newX,newY)])
		return neighbors
		
	def getTile(self, x, y):
		return self.tiles[(x, y)]

	# after flagging a tile, use this helper function to update our database
	def flaggedTile(self, x, y):
		if (self.tiles[(x,y)].flagged == True):
			print("FLAGGING ERROR: Tile at (" + str(x+1) + ", " + str(y+1) + ") already flagged!")
		else:
			self.tiles[(x,y)].flagged = True
	
	# after unflagging a tile, use this helper function to update our database
	def unflaggedTile(self, x, y):
		if (self.tiles[(x,y)].flagged == False):
			print("UNFLAGGING ERROR: Tile at (" + str(x+1) + ", " + str(y+1) + ") already unflagged!")
		else:
			self.tiles[(x,y)].flagged = False

	# after uncovering a tile, use this helper function to update our database
	def uncoveredTile(self, x, y, label):
		if (self.tiles[(x, y)].covered == False):
			print("UNCOVERING ERROR: Tile at (" + str(x+1) + ", " + str(y+1) + ") already uncovered!")
		else:
			self.tiles[(x,y)].covered = False
			self.tiles[(x,y)].percept_number = label
			self.updateEffectiveNumberOfCell(x,y)

	def updateEffectiveNumberOfCell(self, x, y):
		self.tiles[(x,y)].effective_number = self.tiles[(x,y)].percept_number - len(self.getNeighborsFlagged(x, y))
		
	def updateEffectiveNumberOfNeighbors(self, x, y): #updates neighbors of a flagged tile
		uncvNeighbors = self.getNeighborsUncovered(x, y)
		for tile in uncvNeighbors:
			self.updateEffectiveNumberOfCell(tile.x, tile.y)

	def updateLast(self, action, x, y):
		self.last_action = action
		self.last_tile = (x, y)

	def getLeastRiskTile(self):
		percept_tiles = []
		for i in range(1, 9):
			for key, tile in self.tiles:
				if tile.percept == i:
					percept_tiles.append((tile, len(self.getNeighborsCoveredAndUnflagged(tile.x, tile.y)-tile.percept_number)))
		leastRiskTuple = min(percept_tiles, key = lambda t: t[1])
		return leastRiskTuple[0]


