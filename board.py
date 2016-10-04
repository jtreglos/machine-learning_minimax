class Board:
	"""Abstract class for any two-player perfect information board game (Tic-Tac-Toe, Chess, etc.).
	The following methods must be overriden in your game-specific class!"""

	def getMoves(self):
		raise NotImplementedError("This method must be overriden in your game-specific class!")

	def makeMove(self, move):
		raise NotImplementedError("This method must be overriden in your game-specific class!")

	def evaluate(self, player=None):
		raise NotImplementedError("This method must be overriden in your game-specific class!")

	def currentPlayer(self):
		raise NotImplementedError("This method must be overriden in your game-specific class!")

	def isGameOver(self):
		raise NotImplementedError("This method must be overriden in your game-specific class!")
