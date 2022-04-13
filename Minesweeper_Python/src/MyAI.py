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

from re import T
from AI import AI
from Action import Action

class Tile():
	x = 0
	y = 0
	covered = True
	flag = False
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
		self.sy = starty
		self.tiles = {}
		for i in range(1, cols+1):
			for j in range(1, rows+1):
				t = Tile()
				t.x = i
				t.y = j 
				tiles[(i, j)] = t
		self.tiles[sx, sy].covered = False




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

	def getNeighbors(self, x, y):
		
		pass
		
	def getNeighborsActive(self, x, y):
		pass
		
	def getNeighborsFlagged(self, x, y):
		pass
		
	def getTile(self, x, y):
		return self.tiles[x, y]

	def flagTile(self, x, y):
		# if (self.tiles)
			
		