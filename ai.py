from random import randrange
from tetris import COLS

def make_move(tetris):
	pos_max = COLS - len(tetris.stone[0])
	tetris.move_to(randrange(pos_max + 1))
	# tetris.insta_drop()
