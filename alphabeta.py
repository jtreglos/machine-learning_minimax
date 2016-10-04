import time

INFINITY = 9999
TIMEOUT = 10

def abnegamax(board, max_depth, current_depth, alpha, beta):
	if board.isGameOver() or current_depth == max_depth:
		return board.evaluate(), None

	best_move = None
	best_val = -INFINITY

	for move in board.getMoves():
		new_board = board.makeMove(move)

		new_val, new_move = abnegamax(new_board, max_depth, current_depth+1, -beta, -max(alpha, best_val))
		new_val = -new_val

		if new_val > best_val:
			best_val = new_val
			best_move = move

			if best_val >= beta:
				return best_val, best_move

	return best_val, best_move


def getBestMove(board, max_depth=10):
	value, move = abnegamax(board, max_depth, 0, -INFINITY, INFINITY)
	return move


def getIterativeBestMove(board, max_depth=100):
	t0 = time.time()
	
	for depth in range(1, max_depth):
		value, move = abnegamax(board, depth+1, 0, -INFINITY, INFINITY)
		dt = time.time() - t0
		if dt > TIMEOUT and move != None:
			break
	
	print("%.2f s (depth: %d, player: %s, value: %.2f)" % (dt, depth, board.currentPlayer(), value))
	return move


# def abnegascout(board, max_depth, current_depth, alpha, beta):
# 	# print("alpha=", alpha, " / beta=", beta)
# 	if board.isGameOver() or current_depth == max_depth:
# 		# print("-- LEAF NODE --")
# 		# print(board)
# 		# print("utility=", board.evaluate())
# 		return board.evaluate(), None
# 	# else:
# 		# print("===============")
# 		# print(board)

# 	best_move = None
# 	best_val = -INFINITY

# 	adaptive_beta = beta

# 	for move in board.getMoves():
# 		new_board = board.makeMove(move)
# 		new_val, new_move = abnegascout(new_board, max_depth, current_depth+1, -adaptive_beta, -max(alpha, best_val))
# 		new_val = -new_val

# 		if new_val > best_val:
# 			if adaptive_beta == beta:
# 				best_val = new_val
# 				best_move = move
# 			else:
# 				new_val, best_move = abnegascout(new_board, max_depth, current_depth+1, -beta, -new_val)
# 				best_val = -new_val

# 			if best_val >= beta:
# 				return best_val, best_move

# 			adaptive_beta = max(alpha, best_val) + 1

# 	return best_val, best_move

