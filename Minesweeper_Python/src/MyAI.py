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
		self.total_tiles = rowDimension*colDimension
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
		self.count_uncovered_or_flagged_tiles = 0
		self.uncoveredTile(startX, startY, 0)
		self.tiles[(startX, startY)].effective_number = 0

		# print(str(startX) + ", " + str(startY))	# For debugging purposes
		
	def getAction(self, number: int) -> "Action Object":

		# Updating our database after every turn
		if self.last_action == AI.Action.UNCOVER:
			self.uncoveredTile(self.last_tile[0], self.last_tile[1], number)
		elif self.last_action == AI.Action.FLAG:
			self.flaggedTile(self.last_tile[0], self.last_tile[1])

		# Code to finish the game when there are cells blocked off by a wall of mines
		## If no mines remain yet there are covered cells, uncover all covered cells
		if(not self.mines and self.total_tiles - self.count_uncovered_or_flagged_tiles != 0):
			for pair in self.tiles:
				tile = self.tiles[pair]
				if (tile.covered and tile.flagged == False):
					return self.returnAction(AI.Action.UNCOVER, tile.x, tile.y)
		## If mines exist and they match the number of covered cells, flag all covered cells
		elif(self.mines and self.total_tiles - self.count_uncovered_or_flagged_tiles == self.mines):
			for pair in self.tiles:
				tile = self.tiles[pair]
				if tile.covered and tile.flagged == False:
					return self.returnAction(AI.Action.FLAG, tile.x, tile.y)

		# Rule of Thumb 🤖
		for pair in self.tiles:
			tile = self.tiles[pair]
			## take action to uncover (when effective number is 0 and we still have (covered && unflagged) neighbors) 
			if tile.effective_number == 0:
				neighbors = self.getNeighborsCoveredAndUnflagged(tile.x, tile.y)
				if neighbors:
					return self.returnAction(AI.Action.UNCOVER, neighbors[0].x, neighbors[0].y)
			## or flag (when effective number is equal to uncovered neighbors, non-zero) and decrement effective number
			if (tile.covered == False):
				covered_neighbors = self.getNeighborsCoveredAndUnflagged(tile.x, tile.y)
				self.updateEffectiveNumberOfCell(tile.x, tile.y)
				if (tile.effective_number != 0) and (tile.effective_number == len(covered_neighbors)):
					return self.returnAction(AI.Action.FLAG, covered_neighbors[0].x, covered_neighbors[0].y)

		# If no certainly safe tiles are uncovered, use getLeastRiskTile 🧠✖️➖➗
		if self.mines != 0:
			guess_tile = self.getLeastRiskTile()
			if (guess_tile):
				guess_neighbors = self.getNeighborsCoveredAndUnflagged(guess_tile.x, guess_tile.y)
				if (len(guess_neighbors) != 0):
					return self.returnAction(AI.Action.UNCOVER, guess_neighbors[0].x, guess_neighbors[0].y)

		# If we don't know what to do and we still have undealt with tiles (neither uncovered nor flagged), uncover one of them
		if(self.total_tiles - self.count_uncovered_or_flagged_tiles != 0): 
			for pair in self.tiles:
				tile = self.tiles[pair]
				if tile.covered and not tile.flagged:
					return self.returnAction(AI.Action.UNCOVER, tile.x, tile.y)

		# No more moves
		return Action(AI.Action.LEAVE)

	def returnAction(self, action, x, y):
		self.last_action = action
		self.last_tile = (x, y)
		return Action(action, x, y)

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
		self.mines -= 1
		self.count_uncovered_or_flagged_tiles += 1
		if (self.tiles[(x,y)].flagged == True):
			print("FLAGGING ERROR: Tile at (" + str(x+1) + ", " + str(y+1) + ") already flagged!")
		else:
			self.tiles[(x,y)].flagged = True
			self.updateEffectiveNumberOfNeighbors(x,y)
	
	# after unflagging a tile, use this helper function to update our database
	def unflaggedTile(self, x, y):
		self.mines += 1
		self.count_uncovered_or_flagged_tiles -= 1
		if (self.tiles[(x,y)].flagged == False):
			print("UNFLAGGING ERROR: Tile at (" + str(x+1) + ", " + str(y+1) + ") already unflagged!")
		else:
			self.tiles[(x,y)].flagged = False
			self.updateEffectiveNumberOfNeighbors(x,y)

	# after uncovering a tile, use this helper function to update our database
	def uncoveredTile(self, x, y, label):
		self.count_uncovered_or_flagged_tiles += 1
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

	def getLeastRiskTile(self): #returns tile with the least mines to neighbor ratio
		percept_tiles = []
		for i in range(1, 9):
			for key in self.tiles:
				tile = self.tiles[key]
				if ((tile.percept_number == i) and (len(self.getNeighborsCoveredAndUnflagged(tile.x, tile.y)) > 0)):
					percept_tiles.append((tile, tile.percept_number/len(self.getNeighborsCoveredAndUnflagged(tile.x, tile.y))))
		if percept_tiles:
			leastRiskTuple = min(percept_tiles, key = lambda t: t[1])
			return leastRiskTuple[0]
		else:
			return False


	def getMineCombos(self, x, y, maxNumberOfMines, totalFlagged = 0, tiles = None, tileToFlag = None, comboList = None):
		if tileToFlag == None: #first call
			combos = [] #list of valid list of tiles that could be flagged
			tilesToFlag = self.getNeighborsCovered(x, y)
			for tile in tilesToFlag:
				self.getMineCombos(x, y, maxNumberOfMines, 0, tilesToFlag, tile, combos)
		else: #every other call
			pass
			#1. flag tileToFlag and increment totalFlagged
            #   note: be sure to update status in tiles
            #2. check if neighpor percept number is violated
            #   2a. if it is, return
            #3. if not, check if maxNumberofMines == totalFlagged
            #   3a. if it is, check if combination is already in combo. add it if not and return

            #for each tile not flagged
            #4. if not, call function on remaining unflagged and uncovered tile



	
