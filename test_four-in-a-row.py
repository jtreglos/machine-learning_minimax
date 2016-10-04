import cProfile
from four_in_a_row_board import *
from alphabeta import *

def run():
	b = FourInARowBoard("P1")

	while not b.isGameOver():
		move = getIterativeBestMove(b)
		b.applyMove(move)
		print(b)

		if not b.isGameOver():
			# col = int(input("Col: "))
			move = getIterativeBestMove(b)
			b.applyMove(move)
			print(b)

	print("Game Over! v =", b.evaluate(b.p2))

cProfile.run('run()')