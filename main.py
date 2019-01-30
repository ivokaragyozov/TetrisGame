# TODO
	# - draw the game over screen
	# - make start menu
	# - make an AI to play (maybe not in the near future)
	# - add additional statistics druring gameplay for showing the number of past pieces of each type
	# - add animations when clearing lines
	# - music
	# - include database with results

import pygame
import random
import numpy as np

config = {
	'rows': 21	,
	'columns': 10, 
	'square_size': 40,
	'non_board_part_color': (192, 192, 192)
}

level_speeds = [
	500,
	480,
	460,
	440,
	420,
	400,
	360,
	320,
	280,
	260,
	240,
	220,
	200,
	160,
	140,
	120,
	100,
	80,
	60,
	50
]

piece_matrices = [
	[
		[
			[0, 0, 1, 0],
			[0, 0, 1, 0],
			[0, 0, 1, 0],
			[0, 0, 1, 0]
		],
		[
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[1, 1, 1, 1],
			[0, 0, 0, 0]
		]
	],
	[
		[
			[0, 0, 0, 0],
			[1, 1, 1, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 0]
		],
		[
			[0, 1, 0, 0],
			[0, 1, 0, 0],
			[1, 1, 0, 0],
			[0, 0, 0, 0]
		],
		[
			[1, 0, 0, 0], 
			[1, 1, 1, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]
		],
		[
			[0, 1, 1, 0],
			[0, 1, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 0, 0]
		]
	],
	[
		[
			[0, 0, 0, 0],
			[1, 1, 1, 0],
			[1, 0, 0, 0],
			[0, 0, 0, 0]
		],
		[
			[1, 1, 0, 0],
			[0, 1, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 0, 0]
		], 
		[
			[0, 0, 1, 0],
			[1, 1, 1, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]
		],
		[
			[0, 1, 0, 0],
			[0, 1, 0, 0],
			[0, 1, 1, 0],
			[0, 0, 0, 0]
		]
	],
	[
		[
			[0, 1, 1, 0],
			[0, 1, 1, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]
		]
	],
	[
		[
			[0, 0, 0, 0],
			[0, 1, 1, 0],
			[1, 1, 0, 0],
			[0, 0, 0, 0]
		],
		[
			[0, 1, 0, 0],
			[0, 1, 1, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 0]
		]
	],
	[
		[
			[0, 0, 0, 0],
			[1, 1, 1, 0],
			[0, 1, 0, 0],
			[0, 0, 0, 0]
		],
		[
			[0, 1, 0, 0],
			[1, 1, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 0, 0]
		],
		[
			[0, 1, 0, 0],
			[1, 1, 1, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]
		],
		[
			[0, 1, 0, 0],
			[0, 1, 1, 0],
			[0, 1, 0, 0],
			[0, 0, 0, 0]
		]
	],
	[
		[
			[0, 0, 0, 0],
			[1, 1, 0, 0],
			[0, 1, 1, 0],
			[0, 0, 0, 0]
		],
		[
			[0, 0, 1, 0],
			[0, 1, 1, 0],
			[0, 1, 0, 0],
			[0, 0, 0, 0]
		]
	]
]

piece_number_of_rotations = [
	2, 4, 4, 1, 2, 4, 2
]

piece_colors = [
	(255, 0, 0),
	(255,165,0),
	(255, 0, 255),
	(0, 0, 255),
	(0, 255, 0),
	(128, 128, 0),
	(0, 255, 255),
	(255, 255, 255),
	(0, 0, 0)
]

class Piece:
	def __init__(self, type = -1):
		if type == -1:
			type = random.randrange(7)

		self.type = type
		self.matrix = np.asarray(piece_matrices[self.type][0])

		self.rotation = 0

		self.color = piece_colors[self.type]

		lowest_row = 4
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] == 1:
					lowest_row = min(lowest_row, i)

		self.row = -lowest_row
		self.col = config['columns'] // 2 - 2


	def rotate_clockwise(self):
		self.rotation = (self.rotation + 1) % piece_number_of_rotations[self.type]

		new_matrix = np.asarray(piece_matrices[self.type][self.rotation])

		lowest_row = 4
		lowest_col = 4
		highest_row = -1
		highest_col = -1
		for i in range(4):
			for j in range(4):
				if new_matrix[i][j] == 1:
					if i < lowest_row:
						lowest_row = i
					if i > highest_row:
						highest_row = i
					if j < lowest_col:
						lowest_col = j
					if j > highest_col:
						highest_col = j

		if self.row + lowest_row < 0:
			return
		if self.col + lowest_col < 0:
			return
		if self.row + highest_row >= config['rows']:
			return
		if self.col + highest_col >= config['columns']:
			return

		self.matrix = new_matrix


	def rotate_counter_clockwise(self):
		self.rotate_clockwise()
		self.rotate_clockwise()
		self.rotate_clockwise()

	def move_down(self):
		self.row += 1

	def move_right(self, board):
		will_move = True
		for i in range(4):
			for j in reversed(range(4)):
				if self.matrix[i][j] == 1:
					if self.col + j + 1 >= config['columns']:
						will_move = False
						break

					if board[self.row + i][self.col + j + 1] != 7:
						will_move = False
						break

		if will_move:
			self.col += 1

	def move_left(self, board):
		will_move = True
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] == 1:
					if self.col + j - 1 < 0:
						will_move = False
						break

					if board[self.row + i][self.col + j - 1] != 7:
						will_move = False
						break

		if will_move:
			self.col -= 1

class GamePlay:
	def __init__(self, start_level = 1):
		self.board = np.ndarray((config['rows'], config['columns']), int)
		self.board.fill(7)

		self.level = start_level
		self.is_on_initial_level = True
		self.rem_to_next_level = 0

		for i in range(config['columns']):
			self.board[config['rows'] - 1][i] = 8

		self.current_piece = Piece()
		self.next_piece = Piece()

		pygame.init()
		self.screen = pygame.display.set_mode(
			(config['square_size'] * (config['columns'] + 5), config['square_size'] * config['rows'])
		)

		self.is_game_over = False
		self.cnt_removed = 0
		self.score = 0

		self.non_board_part = (config['square_size'] * config['columns'], 0)
		self.draw_non_board_part()

		self.draw_board()
		self.run()

	def run(self):	
		MOVEEVENT, t, trail = pygame.USEREVENT + 1, level_speeds[self.level], []
		pygame.time.set_timer(MOVEEVENT, t)

		while not self.is_game_over:	
			events = pygame.event.get()
			for event in events:
			    if event.type == pygame.KEYDOWN:
			        if event.key == pygame.K_LEFT:
			            self.current_piece.move_left(self.board)
			        if event.key == pygame.K_RIGHT:
			            self.current_piece.move_right(self.board)
			        if event.key == pygame.K_z:
			        	self.current_piece.rotate_counter_clockwise()
			        if event.key == pygame.K_x:
			        	self.current_piece.rotate_clockwise()
			        if event.key == pygame.K_DOWN:
			        	self.current_piece.move_down()
			        if event.key == pygame.K_ESCAPE:
			        	self.is_game_over = True
			    elif event.type == MOVEEVENT:
			    	self.current_piece.move_down()

			if self.is_piece_ready():
				self.current_piece.row -= 1

				self.insert_piece_in_board()
				self.current_piece = self.next_piece
				self.next_piece = Piece()

				self.is_game_over = self.check_is_game_over()

			self.remove_full_lines()
			self.draw()

		self.draw_game_over()

		while True:
			events = pygame.event.get()
			for event in events:
			    if event.type == pygame.KEYDOWN:
			        exit()

	def draw(self):
		self.draw_board()
		self.draw_non_board_part()

	def draw_board(self):
		for i in range(config['rows']):
			for j in range(config['columns']): 
				pygame.draw.rect(self.screen, piece_colors[self.board[i][j]], 
					(j * config['square_size'], i * config['square_size'], config['square_size'], config['square_size']), 0)
				if self.board[i][j] != 7:
					pygame.draw.rect(self.screen, (0, 0, 0), 
						(j * config['square_size'], i * config['square_size'], config['square_size'], config['square_size']), 1)

		for i in range(4):
			for j in range(4):
				if self.current_piece.matrix[i][j] == 1:
					pygame.draw.rect(self.screen, self.current_piece.color, 
						((self.current_piece.col + j) * config['square_size'], 
						(self.current_piece.row + i) * config['square_size'], 
						config['square_size'], config['square_size']), 0)
					pygame.draw.rect(self.screen, (0, 0, 0), 
						((self.current_piece.col + j) * config['square_size'], 
						(self.current_piece.row + i) * config['square_size'], 
						config['square_size'], config['square_size']), 1)

		pygame.display.update()

	def is_piece_ready(self):
		for j in range(4):
			lowest_row = -1
			for i in range(4):
				if self.current_piece.matrix[i, j] == 1:
					lowest_row = self.current_piece.row + i

			if lowest_row != -1:
				if self.board[lowest_row][self.current_piece.col + j] != 7:
					return True

		return False 

	def insert_piece_in_board(self):
		for i in range(0, 4):
			for j in range(0, 4):
				if self.current_piece.matrix[i][j] == 1:
					self.board[self.current_piece.row + i][self.current_piece.col + j] = self.current_piece.type

	def remove_full_lines(self):
		removed_indices = []
		for i in range(config['rows'] - 1):
			is_full = True
			for j in range(config['columns']):
				if self.board[i][j] == 7:
					is_full = False
					break

			if is_full:
				self.board = np.delete(self.board, i, axis = 0)
				self.board = np.insert(self.board, 0, 7, axis = 0)

				removed_indices.append(i)

		self.cnt_removed += len(removed_indices)

		curr = 0
		last = -1
		for x in removed_indices:
			if last == -1:
				curr = 1
			elif last == x - 1:
				curr += 1
			else:
				if curr == 1:
					self.score += 40 * (self.level + 1)
				elif curr == 2:
					self.score += 100 * (self.level + 1)
				elif curr == 3:
					self.score += 300 * (self.level + 1)
				elif curr == 4:
					self.score += 1200 * (self.level + 1)

				curr = 1

			last = x

		if curr == 1:
			self.score += 40 * (self.level + 1)
		elif curr == 2:
			self.score += 100 * (self.level + 1)
		elif curr == 3:
			self.score += 300 * (self.level + 1)
		elif curr == 4:
			self.score += 1200 * (self.level + 1)

		if self.is_on_initial_level:
			if self.cnt_removed >= min(self.level * 10 + 10, max(100, self.level * 10 - 50)):
				self.is_on_initial_level = False;
				self.rem_to_next_level = 10 - (self.cnt_removed - min(self.level * 10 + 10, max(100, self.level * 10 - 50)))
				self.level += 1
		else:
			self.rem_to_next_level -= len(removed_indices)

			if self.rem_to_next_level < 0:
				self.rem_to_next_level += 10
				self.level += 1

	def check_is_game_over(self):
		for i in range(4):
			for j in range(4):
				if self.current_piece.matrix[i][j] == 1:
					if self.board[self.current_piece.row + i][self.current_piece.col + j] != 7:
						return True

		return False

	def draw_game_over(self):
		pygame.draw.rect(self.screen, config['non_board_part_color'], 
			(self.non_board_part[0], self.non_board_part[1], config['square_size'] * 5, config['square_size'] * config['rows']), 0)

		pygame.draw.rect(self.screen, (255, 255, 255), 
			(0, 0, config['columns'] * config['square_size'], config['rows'] * config['square_size']), 0)

		pygame.font.init()
		myfont = pygame.font.SysFont('Comic Sans MS', 30)

		game_over_surface = myfont.render('Game Over! :(', False, (255, 0, 0))
		self.screen.blit(game_over_surface, 
			(config['square_size'] * (config['columns'] // 2 - 2), config['square_size'] * (config['rows'] // 2)))

		myfont = pygame.font.SysFont('Comic Sans MS', 20)
		score_surface = myfont.render('Your score is: ' + str(self.score), False, (0, 255, 0))
		self.screen.blit(score_surface, 
			(config['square_size'] * (config['columns'] // 2 - 2), config['square_size'] * (config['rows'] // 2 + 1)))

		pygame.display.update()

	def draw_non_board_part(self):
		pygame.draw.rect(self.screen, config['non_board_part_color'], 
			(self.non_board_part[0], self.non_board_part[1], config['square_size'] * 5, config['square_size'] * config['rows']), 0)

		pygame.font.init()
		myfont = pygame.font.SysFont('Comic Sans MS', 20)

		score_surface = myfont.render('Score: ' + str(self.score), False, (255, 0, 255))
		self.screen.blit(score_surface, (self.non_board_part[0] + config['square_size'], config['square_size']))

		lines_surface = myfont.render('Lines: ' + str(self.cnt_removed), False, (255, 0, 255))
		self.screen.blit(lines_surface, (self.non_board_part[0] + config['square_size'], config['square_size'] * 2))

		level_surface = myfont.render('Level: ' + str(self.level), False, (255, 0, 255))
		self.screen.blit(level_surface, (self.non_board_part[0] + config['square_size'], config['square_size'] * 3))

		next_piece_surface = myfont.render('Next piece', False, (255, 0, 255))
		self.screen.blit(next_piece_surface, (self.non_board_part[0] + config['square_size'], config['square_size'] * 5))

		lowest_row = 4
		lowest_col = 4
		highest_row = -1
		highest_col = -1
		for i in range(4):
			for j in range(4):
				if self.next_piece.matrix[i][j] == 1:
					if i < lowest_row:
						lowest_row = i
					if j < lowest_col:
						lowest_col = j
					if i > highest_row:
						highest_row = i
					if j > highest_col:
						highest_col = j

		for i in range(lowest_row, highest_row + 1):
			for j in range(lowest_col, highest_col + 1):
				if self.next_piece.matrix[i][j] == 1:
					row = (i - lowest_row) * (config['square_size'] // 2) + config['square_size'] * 6
					col = (j - lowest_col) * (config['square_size'] // 2) + self.non_board_part[0] + config['square_size']

					pygame.draw.rect(self.screen, self.next_piece.color, (col, row, 
						config['square_size'] // 2, config['square_size'] // 2), 0)
					pygame.draw.rect(self.screen, (0, 0, 0), 
						(col, row, config['square_size'] // 2, config['square_size'] // 2), 1)


		pygame.display.update()

game = GamePlay(9)