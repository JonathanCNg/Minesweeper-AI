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
	number = 0
	effective_number = 0


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		print("hello world")
		self.rows = rowDimension
		self.cols = colDimension
		self.mines = totalMines
		self.sx = startX
		self.sy = startY
		self.tiles = {}
		for i in range(1, self.cols+1):
			for j in range(1, self.rows+1):
				t = Tile()
				t.x = i
				t.y = j 
				self.tiles[(i, j)] = t
		self.tiles[self.sx, self.sy].covered = False




		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		



		
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
		
	def getNeighborsActive(self, x, y):
		pass
		
	def getNeighborsFlagged(self, x, y):
		pass
		
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
			self.tiles[x,y].number = label
	
	
			
		