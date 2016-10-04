import sys

def minimax(board, player, max_depth, current_depth):
	print("-- MINIMAX -- DEPTH: ", current_depth, "/", max_depth)
	INFINITY = 9999

	# Check if we're done recursing
	if board.isGameOver() or current_depth == max_depth:
		return board.evaluate(player), None

	# Otherwise bubble up values from below
	best_move = None
	if board.currentPlayer() == player:
		best_score = -INFINITY
	else:
		best_score = INFINITY

	# Go through each move
	for move in board.getMoves():
		print("========================= ", board.stringCurrentPlayer())
		print("MOVE: ", move)
		new_board = board.makeMove(move)
		print(new_board)

		# Recurse
		current_score, current_move = minimax(new_board, player, max_depth, current_depth+1)
		print("CURRENT SCORE: ", current_score)
		print("CURRENT MOVE: ", current_move)

		# Update the best score
		if board.currentPlayer() == player:
			if current_score > best_score:
				print("BEST UPDATED FOR SAME PLAYER")
				best_score = current_score
				best_move = move
		else:
			if current_score < best_score:
				print("BEST UPDATED FOR OTHER PLAYER")
				best_score = current_score
				best_move = move
	
	# Return the score and the best move
	print("------------------------")
	print("FINAL BEST SCORE:", best_score)
	print("FINAL BEST MOVE:", best_move)
	
	return best_score, best_move



def getBestMove(board, player, max_depth):
	# Get the result of a minimax run and return the move
	score, move = minimax(board, player, max_depth, 0)

	return move
