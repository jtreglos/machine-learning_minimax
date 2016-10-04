INFINITY = 9999

def abNegamax(board, max_depth, current_depth, alpha, beta):
	# Check if we're done recursing
	if board.isGameOver() or current_depth == max_depth:
		return board.evaluate(), None

	# Otherwise bubble up values from below
	best_move = None
	best_score = -INFINITY

	# Go through each move
	for move in board.getMoves():
		new_board = board.makeMove(move)

		# Recurse
		recursed_score, current_move = abNegamax(new_board, max_depth, current_depth+1, -beta, -max(alpha, best_score))
		current_score = -recursed_score

		# Update the best score
		if current_score > best_score:
			best_score = current_score
			best_move = move

			# If we're outside the bounds, then prune: exit immediately
			if best_score >= beta:
				return best_score, best_move

	return best_score, best_move


def abNegascout(board, max_depth, current_depth, alpha, beta):
	# Check if we're done recursing
	if board.isGameOver() or current_depth == max_depth:
		return board.evaluate(), None

	# Otherwise bubble up values from below
	best_move = None
	best_score = -INFINITY

	# Keep track of the Test window value
	adaptive_beta = beta

	# Go through each move
	for move in board.getMoves():
		new_board = board.makeMove(move)

		# Recurse
		recursed_score, current_move = abNegamax(new_board, max_depth, current_depth+1, -adaptive_beta, -max(alpha, best_score))
		current_score = -recursed_score

		# Update the best score
		if current_score > best_score:
			# If we're in 'narrow-mode' then widen and do a regulare AB Negamax search
			if adaptive_beta == beta or current_depth >= max_depth-2:
				best_score = current_score
				best_move = move

			# Otherwise we can do a Test
			else:
				negative_best_score, best_move = abNegascout(new_board, max_depth, current_depth, -beta, -current_score)
				best_score = -negative_best_score

			# If we're outside the bounds, then prune: exit immediately
			if best_score >= beta:
				return best_score, best_move

			# Otherwise update the window location
			adaptive_beta = max(alpha, best_score) + 1

	return best_score, best_move

def getBestMove(board, max_depth):
	# Get the result of a abNegascout run and return the move
	score, move = abNegascout(board, max_depth, 0, -INFINITY, INFINITY)

	return move