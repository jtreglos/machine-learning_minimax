import copy
from board import Board

class TicTacToeBoard(Board):
	def __init__(self, start_player, size=3):
		self.p1 = 1
		self.p2 = size + 1
		self.size = size
		self.isize = size * size
		self.r = range(size)
		self.complete_seq = {size*self.p1, size*self.p2}
		self.board = [0 for i in range(self.isize)]
		self.evaluate_win = None

		if start_player in { "P1", "P2" }:
			if start_player == "P1":
				self.current_player = self.p1
			else:
				self.current_player = self.p2
		else:
			raise TypeError("Invalid start player!")


	def idx(self, col, line):
		return line * self.size + col
	

	def __repr__(self):
		ret = ""

		for line in self.r:
			for col in self.r:
				cell = self.board[self.idx(col, line)]
				
				if cell == 0:
					ret += "  "
				elif cell == self.p1:
					ret += "X "
				elif cell == self.p2:
					ret += "O "
			ret += "\n"

		return ret

	
	def copy(self):
		new_board = TicTacToeBoard(self.currentPlayer(), self.size)
		new_board.board = self.board[:]

		return new_board

	
	def getMoves(self):
		moves = []

		for line in self.r:
			for col in self.r:
				if self.board[self.idx(col, line)] == 0:
					moves.append((col, line))

		return moves

	
	def nextPlayer(self, player):
		if player == self.p1:
			return self.p2
		else:
			return self.p1


	def makeMove(self, move):
		new_board = self.copy()
		new_board.applyMove(move)

		return new_board


	def applyMove(self, move):
		col,line = move
		i = self.idx(col, line)
		
		if col in self.r and line in self.r and self.board[i] == 0:
			self.board[i] = self.current_player
			self.current_player = self.nextPlayer(self.current_player)
			self.evaluate_win = None
		else:
			raise TypeError("Invalid move!")

	
	def evaluate(self, player=None):
		if player == None:
			selected_player = self.current_player
		else:
			selected_player = player

		s = self.evaluateWin()

		if s == 0:
			return 0
		elif s == selected_player * self.size:
			return 1
		else:
			return -1

	
	def currentPlayer(self):
		if self.current_player == self.p1:
			return "P1"
		else:
			return "P2"


	def _checkLines(self):
		for line in self.r:
			i = self.size * line
			s = sum(self.board[i:i+self.size])
			if s in self.complete_seq:
				return s

		return None

	def _checkCols(self):
		for col in self.r:
			s = sum(self.board[col:self.isize:self.size])

			if s in self.complete_seq:
				return s			

		return None


	def _checkDiags1(self):
		s = sum(self.board[::self.size+1])
		if s in self.complete_seq:
			return s

		return None


	def _checkDiags2(self):
		s = sum(self.board[self.size-1:self.isize-1:self.size-1])
		if s in self.complete_seq:
			return s

		return None

	
	def evaluateWin(self):
		if self.evaluate_win == None:
			self.evaluate_win = self._calcEvaluateWin()

		return self.evaluate_win


	def _calcEvaluateWin(self):
		# Check lines:
		s = self._checkLines()
		if s != None:
			return s

		# Check cols:
		s = self._checkCols()
		if s != None:
			return s

		# Check 1st diag:
		s = self._checkDiags1()
		if s != None:
			return s

		# Check 2nd diag:
		s = self._checkDiags2()
		if s != None:
			return s

		return 0


	def isFull(self):
		return 0 not in self.board


	def isGameOver(self):
		return self.isFull() or self.evaluateWin() != 0
