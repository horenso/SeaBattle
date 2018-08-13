'''
	0		unknown ' '
	1		water '~'
	2		ship 'O'
	3		hit ship '#'

'''
from random import randint
from copy import deepcopy


class Board:
	def __init__(self, size):
		if size < 1:
			size = 1
		if size > 26:
			size = 26
		self.size = size
		self.board = [[0 for i in range(size)] for j in range(size)]

		self.show_cur = False
		self.cur_x = 0
		self.cur_y = 0

	def __str__(self):
		#Beginning
		s = ' '*4 #row 2
		if self.size >= 10:
			s += ' '

		#Adds ABC
		for i in range(self.size):
			s += chr(ord('A')+i) + ' '
		s += '\n'

		if self.size >= 10:
			s += ' '

		s += ' '*2 + '\u250c' + '\u2500'*(self.size*2+1) + '\u2510' + '\n' #row 3

		#Middle
		for col in range(self.size):
			if self.size >= 10:
				s += '{:2} \u2502'.format(str(col+1))
			else:
				s += str(col+1)+' \u2502'

			if(self.show_cur and col == self.cur_y and self.cur_x == 0):
				s += '['
			else:
				s += ' '

			for row in range(self.size):
				if(self.board[row][col] == 0):
					s += '~'
				elif(1 <= self.board[row][col] <= 9):
					s+= str(self.board[row][col])
				elif(self.board[row][col] == -1):
					s+= '#'

				#curser
				if(self.show_cur and row == self.cur_x and col == self.cur_y):
					s+= ']'
				elif(self.show_cur and col == self.cur_y and row+1 == self.cur_x):
					s+= '['
				else:
					s += ' '

			s += '\u2502 ' + str(1+col)

			if(row < 9):
				s += ' '
			s += '\n'

		#ABC at the end
		if self.size >= 10:
			s += ' '
		s += ' '*2 + '\u2514' + '\u2500'*(self.size*2+1) + '\u2518' + '\n'
		s += ' '*4

		if self.size >= 10:
			s += ' '

		for i in range(self.size):
			s += chr(ord('A')+i) + ' '

		return s

	def str_size(self):
		'''Returns a tuple (x, y) of the size of __str__'''
		x = 7 + 2*self.size
		if self.size >= 10:
			x += 2

		return (x, self.__str__().count('\n')+1)

	def reset(self):
		'''Resets the board (time will tell whether I keep this methode)'''
		self.board = [[0 for i in range(self.size)] for j in range(self.size)]

	def cur_movex(self, x):
		''' Is used to move the curser along the x-axis '''
		if(self.cur_x+x >= 0 and self.cur_x+x < self.size):
			self.cur_x += x

	def cur_movey(self, y):
		''' Is used to move the curser on the y-axis '''
		if(self.cur_y+y >= 0 and self.cur_y+y < self.size):
			self.cur_y += y

	def cur_moveto(self, x, y):
		''' Is used to move the curser to a spesific place '''
		if cur_movex(self, x) and self.cur_y(self, y):
			self.cur_x = x
			self.cur_y = y

	def cur_pos_str(self):
		'''Returns the cursers coordinates, e.g. 'A1' '''
		return chr(ord('A')+self.cur_x) + str(self.cur_y+1)

	def check_new_ship(self, x, y, length, horizontal = True):
		'''Checks if a new ship fits within the grid and doesn't
		collides with preset once
		x/y is the point furthest up or to the left!'''
		if x < 0 or y < 0:
			return False
		if x >= self.size or y >= self.size:
			return False

		if horizontal:
			if x+length > self.size:
				return False
			for pos in range(x, x+length):
				if self.board[pos][y] != 0:
					return False
		else:
			if y+length > self.size:
				return False
			for pos in range(y, y+length):
				if self.board[x][pos] != 0:
					return False

		return True

	def set_new_ship(self, x, y, id, length, horizontal = True):
		'''Checks if a new ship fits within the grid and doesn't
		collides with preset once '''

		if horizontal:
			for pos in range(x, x+length):
				if self.board[pos][y] == 0:
					self.board[pos][y] = id
				else:
					self.board[pos][y] = -1
		else:
			for pos in range(y, y+length):
				if self.board[x][pos] == 0:
					self.board[x][pos] = id
				else:
					self.board[x][pos] = -1

	def show_new_ship(self, x, y , id, length, horizontal = True):
		'''Returns __str__, but with a new ship on display. If Two ships '''
		new_board = Board(self.size)
		new_board.board = deepcopy(self.board)
		new_board.set_new_ship(x, y, id, length, horizontal)
		return new_board.__str__()

	def suggest(self, length):
		'''This is still in testing!!'''
		for i in range(100): #testwise I'll try it max 100 times
			x = randint(0, self.size)
			y = randint(0, self.size)
			horizontal = bool(randint(0,1))
			if self.check_new_ship(x, y, length, horizontal):
				return (x, y, horizontal)
		return False
