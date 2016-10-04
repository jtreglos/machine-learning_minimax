import cProfile
from tic_tac_toe_board import *
from alphabeta import *

def run():
	b = TicTacToeBoard("P1")

	while not b.isGameOver():
		# Computer plays first
		move = getIterativeBestMove(b)
		# value, move = abnegascout(b, -INFINITY, INFINITY)
		b.applyMove(move)
		print(b)

		if not b.isGameOver():
			# Human plays next
			# line = int(input("Line: "))
			# row = int(input("Row: "))
			# my_move = (row, line)
			move = getIterativeBestMove(b)
			b.applyMove(move)
			print(b)

	print("Game Over! v =", b.evaluate(b.p2))


cProfile.run('run()')