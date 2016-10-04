from board import Board

class FourInARowBoard(Board):
	def __init__(self, start_player):
		self.p1 = 1
		self.p2 = 10
		self._victor = -1
		self.board = [ [] for i in range(7) ]
		self._series = {}

		if start_player in { "P1", "P2" }:
			if start_player == "P1":
				self.current_player = self.p1
			else:
				self.current_player = self.p2
		else:
			raise TypeError("Invalid start player!")


	def __repr__(self):
		ret = ""

		for line in range(5, -1, -1):
			line_str = "%d  " % line
			
			for col in range(7):
				if len(self.board[col]) > line:
					if self.board[col][line] == self.p1:
						line_str += "O "
					elif self.board[col][line] == self.p2:
						line_str += "X "
				else:
					line_str += ". "

			line_str += "\n"
			
			ret += line_str

		ret += "\n"
		ret += "   0 1 2 3 4 5 6\n"

		return ret


	def copy(self):
		new_board = FourInARowBoard(self.currentPlayer())
		new_board.board = [x[:] for x in self.board]
		new_board._victor = self._victor
		if len(self._series) != 0:
			new_board._series[self.p1] = [x[:] for x in self._series[self.p1]]
			new_board._series[self.p2] = [x[:] for x in self._series[self.p2]]

		return new_board

	
	def getMoves(self):
		moves = []

		for col in range(7):
			if len(self.board[col]) != 6:
				moves.append(col)

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
		if move in range(7) and len(self.board[move]) < 6:
			self.board[move].append(self.current_player)
			self._series = {}
			self._victor = -1
			self.current_player = self.nextPlayer(self.current_player)
		else:
			raise TypeError("Invalid move!")

	
	def evaluate(self, player=None):
		if player == None:
			selected_player = self.current_player
		else:
			selected_player = player

		s = self.victor()

		if s == None:
			if self.isFull():
				return 0
			serie_player = self.series()[selected_player]
			serie_other_player = self.series()[self.nextPlayer(selected_player)]
			
			if len(serie_player) != 0:
				total_player = sum(serie_player)
			else:
				total_player = 0
			
			if len(serie_other_player) != 0:
				total_other_player = sum(serie_other_player)
			else:
				total_other_player = 0

			return 2*total_player - total_other_player
		elif s == selected_player:
			return 1000
		else:
			return -1000

	
	def currentPlayer(self):
		if self.current_player == self.p1:
			return "P1"
		else:
			return "P2"


	def isFull(self):
		for col in self.board:
			if len(col) != 6:
				return False

		return True


	def series(self):
		if len(self._series) == 0:
			self.calcSeries()
		
		return self._series


	def _calcSeriesCols(self):
		for col in self.board:
			prev_val = 0
			count = 0
			for cell in col:
				if cell == prev_val:
					count += 1
				else:
					if count > 1:
						self._series[prev_val].append(count)
					
					prev_val = cell
					count = 1
			if count > 1:
				self._series[prev_val].append(count)


	def _calcSeriesLines(self):
		for line in range(6):
			prev_val = 0
			count = 0
			for col in range(7):
				if len(self.board[col]) > line:
					if self.board[col][line] == prev_val:
						count += 1
					else:
						if count > 1:
							self._series[prev_val].append(count)
						prev_val = self.board[col][line]
						count = 1
				else:
					if count > 1:
						self._series[prev_val].append(count)
					prev_val = 0
					count = 0
			if prev_val != 0 and count > 1:
				self._series[prev_val].append(count)


	def _calcSeriesDiags1(self):
		for col,line in [ (0,2), (0,1), (0,0), (1,0), (2,0), (3,0) ]:
			c = col
			l = line
			diag = []
			while c < 7 and l < 6:
				if len(self.board[c]) > l:
					diag.append(self.board[c][l])
				else:
					diag.append(0)
				
				c += 1
				l += 1
			
			prev_val = 0
			count = 0
			
			for cell in diag:
				if cell != 0:
					if cell == prev_val:
						count += 1
					else:
						if count > 1:
							self._series[prev_val].append(count)
						prev_val = cell
						count = 1
				else:
					if count > 1 and prev_val != 0:
						self._series[prev_val].append(count)
					prev_val = 0
					count = 0
			if count > 1 and prev_val != 0:
						self._series[prev_val].append(count)


	def _calcSeriesDiags2(self):
		for col,line in [ (0,3), (0,4), (0,5), (1,5), (2,5), (3,5) ]:
			c = col
			l = line
			diag = []
			while c < 7 and l >= 0:
				if len(self.board[c]) > l:
					diag.append(self.board[c][l])
				else:
					diag.append(0)
				
				c += 1
				l -= 1
			
			prev_val = 0
			count = 0
			
			for cell in diag:
				if cell != 0:
					if cell == prev_val:
						count += 1
					else:
						if count > 1:
							self._series[prev_val].append(count)
						prev_val = cell
						count = 1
				else:
					if count > 1 and prev_val != 0:
						self._series[prev_val].append(count)
					prev_val = 0
					count = 0
			if count > 1 and prev_val != 0:
						self._series[prev_val].append(count)


	def calcSeries(self):
		self._series = { self.p1: [], self.p2: [] }
		
		# Check columns
		self._calcSeriesCols()
		
		# Check lines
		self._calcSeriesLines()
		
		# Check LL>UR diags
		self._calcSeriesDiags1()
		
		# Check UL>LR diags
		self._calcSeriesDiags2()


	def _checkCols(self):
		for col in self.board:
			prev_val = 0
			count = 0
			for cell in col:
				if cell == prev_val:
					count += 1
					if count == 4:
						return prev_val
				else:
					prev_val = cell
					count = 1

		return None


	def _checkLines(self):
		for line in range(6):
			prev_val = 0
			count = 0
			for col in range(7):
				if len(self.board[col]) > line:
					if self.board[col][line] == prev_val:
						count += 1
						if count == 4:
							return prev_val
					else:
						prev_val = self.board[col][line]
						count = 1
				else:
					prev_val = 0
					count = 0

		return None


	def _checkDiags1(self):
		for col,line in [ (0,2), (0,1), (0,0), (1,0), (2,0), (3,0) ]:
			c = col
			l = line
			diag = []
			while c < 7 and l < 6:
				if len(self.board[c]) > l:
					diag.append(self.board[c][l])
				else:
					diag.append(0)
				
				c += 1
				l += 1
			
			prev_val = 0
			count = 0
			for cell in diag:
				if cell != 0:
					if cell == prev_val:
						count += 1
						if count == 4:
							return prev_val
					else:
						prev_val = cell
						count = 1
				else:
					prev_val = 0
					count = 0

		return None


	def _checkDiags2(self):
		for col,line in [ (0,3), (0,4), (0,5), (1,5), (2,5), (3,5) ]:
			c = col
			l = line
			diag = []
			while c < 7 and l >= 0:
				if len(self.board[c]) > l:
					diag.append(self.board[c][l])
				else:
					diag.append(0)
				
				c += 1
				l -= 1
			
			prev_val = 0
			count = 0
			for cell in diag:
				if cell != 0:
					if cell == prev_val:
						count += 1
						if count == 4:
							return prev_val
					else:
						prev_val = cell
						count = 1
				else:
					prev_val = 0
					count = 0

		return None


	def calcVictor(self):
		# Check columns
		cc = self._checkCols()
		if cc != None:
			return cc

		# Check lines
		cl = self._checkLines()
		if cl != None:
			return cl

		# Check LL>UR diags
		cd1 = self._checkDiags1()
		if cd1 != None:
			return cd1

		# Check UL>LR diags
		cd2 = self._checkDiags2()
		if cd2 != None:
			return cd2

		return None


	def victor(self):
		if self._victor == -1:
			self._victor = self.calcVictor()

		return self._victor


	def isGameOver(self):
		return self.isFull() or self.victor() != None
