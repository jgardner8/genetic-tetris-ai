from tetris import check_collision, COLS, join_matrices, rotate_clockwise
import heuristic

class AI(object):
	def __init__(self, tetris):
		self.tetris = tetris

	def board_with_stone(self, x, y, stone):
		"""Return new board with stone included"""
		return join_matrices(self.tetris.board, stone, (x, y))

	def intersection_point(self, x, stone):
		"""Find the y coordinate closest to the top where stone will collide"""
		tetris = self.tetris
		y = 0
		while not check_collision(tetris.board, stone, (x, y)):
			y += 1
		return y

	@staticmethod
	def max_x_pos_for_stone(stone):
		"""The furthest position you can move stone to the right"""
		return COLS - len(stone[0])

	@staticmethod
	def num_rotations(stone):
		"""The number of unique rotated positions of stone"""
		stones = [stone]
		while True:
			stone = rotate_clockwise(stone)
			if stone in stones:
				return len(stones)
			stones.append(stone)

	@staticmethod
	def utility(board, heuristics):
		"""heuristics is a dictionary containing function/weight pairs.
		e.g. heuristic_weights = {
			holes_in_board: -0.5,
			avg_height: -2,
		} 
		"""
		return sum([fun(board)*weight for (fun, weight) in heuristics.items()])

	def make_move(self):
		"""Move the current stone to the desired position by modifying TetrisApp's state"""
		tetris = self.tetris
		heuristics = {
			heuristic.num_holes: -8,
			heuristic.num_blocks_above_holes: -5,
			heuristic.num_gaps: -5,
			heuristic.max_height: -6,
			heuristic.avg_height: -4,
			heuristic.num_blocks: -15,
		}

		# TODO: extend this to make two moves
		moves = []
		stone = tetris.stone
		for r in range(AI.num_rotations(tetris.stone)):
			for x in range(self.max_x_pos_for_stone(stone)+1):
				y = self.intersection_point(x, stone)
				board = self.board_with_stone(x, y, stone)
				moves.append( (x, r, board) )
			stone = rotate_clockwise(stone)
		best_move = max(moves, key=lambda m: AI.utility(m[2], heuristics))
		
		# Perhaps this should be a class
		x, r, board = best_move
		for _ in range(r):
			tetris.stone = rotate_clockwise(tetris.stone)
		tetris.move_to(x)
		# tetris.insta_drop()
