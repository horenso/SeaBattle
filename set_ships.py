from player import Player
import unicurses as uc
from math import ceil

stdscr = uc.initscr()

class Set_ships:
	def __init__(self, player):
		self.player = player

		self.on_menu = True # Shifts the focus between menu and board, = show new ship
		self.menu_hi = 0 # Which ele is hightlighted in the menu
		self.menu_sel = -1 # Current item selected, relevant when board is active
		self.num_ships_set = 0

		self.menu = self.player.left_to_set()

		self.new_ship_x = 0
		self.new_ship_y = 0
		self.new_ship_hor = True

		self.title = f'Set ships for player: {self.player.name}'

		self.max_y, self.max_x = uc.getmaxyx(stdscr)

		uc.noecho() # Disable typing on the screen
		uc.cbreak() # catching characters directly without waiting for [ENTER]
		uc.curs_set(0) # Disable blinking curser
		uc.keypad(stdscr, True) # for catching the arrow keys
		uc.start_color()

		self.init_wins()

	def init_wins(self):
		uc.wclear(stdscr)
		self.max_y, self.max_x = uc.getmaxyx(stdscr)

		border_x = ceil(self.max_x*2/3)
		c = int(self.max_x % 2 == 1)

		self.win_title = uc.newwin(3, self.max_x, 0, 0) #(h, w, starty, startx)
		self.win_boardarea = uc.newwin(self.max_y-4, border_x, 3, 0)
		self.win_shipmenu = uc.newwin(self.max_y-4, self.max_x-border_x, 3, border_x)
		self.win_statusbar = uc.newwin(1, self.max_x, self.max_y-1, 0)

		x, y = self.player.board.str_size()
		self.win_board = uc.newwin(y, x+2, 0, 0)
		self.pan_board = uc.new_panel(self.win_board)

		uc.move_panel(self.pan_board, 3+(self.max_y-3)//2-y//2, (border_x-3)//2-x//2)

		uc.wrefresh(stdscr)
		self.draw()

	def draw_title(self):
		offset_x = 2
		offset_y = 1

		uc.box(self.win_title, 0, 0)
		uc.wmove(self.win_title, offset_y, offset_x)
		uc.waddstr(self.win_title, self.title)
		uc.wrefresh(self.win_title)

	def draw_board(self):
		uc.wclear(self.win_board)

		offset_x = 2
		offset_y = 1

		uc.box(self.win_boardarea, 0, 0)

		uc.wmove(self.win_boardarea, offset_y, offset_x)
		if self.on_menu:
			s = self.player.board.__str__()
		else:
			s = self.player.board.show_new_ship(self.new_ship_x, self.new_ship_y,
												self.menu[self.menu_hi].id,
												self.menu[self.menu_hi].length,
												self.new_ship_hor)

		uc.init_pair(11, uc.COLOR_BLUE, uc.COLOR_BLACK)
		uc.init_pair(12, uc.COLOR_WHITE, uc.COLOR_BLACK)
		uc.init_pair(13, uc.COLOR_RED, uc.COLOR_BLACK)

		for chr in s:
			if chr == '~':
				uc.wattron(self.win_board, uc.COLOR_PAIR(11))
				uc.waddstr(self.win_board, chr)
				uc.wattroff(self.win_board, uc.COLOR_PAIR(11))
			elif chr == 'O':
				uc.wattron(self.win_board, uc.COLOR_PAIR(12))
				uc.waddstr(self.win_board, chr)
				uc.wattroff(self.win_board, uc.COLOR_PAIR(12))
			elif chr == '#':
				uc.wattron(self.win_board, uc.COLOR_PAIR(13))
				uc.waddstr(self.win_board, chr)
				uc.wattroff(self.win_board, uc.COLOR_PAIR(13))
			else:
				uc.wattron(self.win_board, uc.COLOR_PAIR(12))
				uc.waddstr(self.win_board, chr)
				uc.wattroff(self.win_board, uc.COLOR_PAIR(12))

		uc.wbkgd(self.win_statusbar, uc.COLOR_PAIR(11))

		uc.wrefresh(self.win_boardarea)
		uc.update_panels()

	def draw_shipmenu(self):
		uc.wclear(self.win_shipmenu)

		offset_x = 2
		offset_y = 1

		uc.box(self.win_shipmenu, 0, 0)
		uc.wmove(self.win_shipmenu, offset_y, offset_x)
		uc.waddstr(self.win_shipmenu, 'ship menu:')
		offset_y += 2

		for ele in self.menu:
			if (self.on_menu and self.menu_hi == self.menu.index(ele)):
				uc.wattron(self.win_shipmenu, uc.A_REVERSE)
				uc.mvwaddstr(self.win_shipmenu, offset_y, offset_x, ele)
				uc.wattroff(self.win_shipmenu, uc.A_REVERSE)
				offset_y += 2
			else:
				uc.mvwaddstr(self.win_shipmenu, offset_y, offset_x, ele)
				offset_y += 2

		uc.wrefresh(self.win_shipmenu)

	def draw_statusbar(self):
		uc.wclear(self.win_statusbar)
		s = '[q] quit   '

		if self.on_menu:
			s += '[\u2191\u2193] move   '
			s += '[\u21B5] select   '
		else:
			s += '[\u2190\u2191\u2192\u2193] move   '
			s += '[r] rotate   '
			s += '[s] suggest   '
			s += '[\u21B5] commit   '

		s += f'{self.num_ships_set}/{len(self.player.ship_list)} set'

		uc.waddstr(self.win_statusbar, s)
		uc.init_pair(4, uc.COLOR_WHITE, uc.COLOR_BLUE)
		uc.wbkgd(self.win_statusbar, uc.COLOR_PAIR(4))
		uc.wrefresh(self.win_statusbar)

	def draw(self):
		self.draw_board()
		self.draw_title()
		self.draw_shipmenu()
		self.draw_statusbar()

	def input(self):
		self.key = uc.wgetch(stdscr)

		if self.key == uc.KEY_RESIZE:
			self.max_y, self.max_x = uc.getmaxyx(stdscr)
			if self.max_x > 10 and self.max_y > 10:
				self.init_wins()

		if(self.on_menu):
			if(self.key == uc.KEY_UP):
				self.menu_hi -= 1
				if self.menu_hi == -1:
					self.menu_hi = len(self.menu)-1

			elif(self.key == uc.KEY_DOWN):
				self.menu_hi += 1
				if self.menu_hi >= len(self.menu):
					self.menu_hi = 0

			elif(self.key == ord('\n')):
				for ship in self.player.ship_list:
					if ship.id == self.menu[self.menu_hi].id:
						ship.placed = True

				self.new_ship_id = self.menu[self.menu_hi].id
				self.new_ship_len = self.menu[self.menu_hi].length

				self.new_ship_x = 0
				self.new_ship_y = 0
				self.new_ship_hor = True

				self.on_menu = False
		else:
			if(self.key == uc.KEY_LEFT):
				if self.new_ship_x - 1 >= 0:
					self.new_ship_x -= 1

			elif(self.key == uc.KEY_RIGHT):
				if  self.new_ship_hor:
					if self.new_ship_x + self.menu[self.menu_hi].length < self.player.board.size:
						self.new_ship_x += 1
				else:
					if self.new_ship_x + 1 < self.player.board.size:
						self.new_ship_x += 1

			elif(self.key == uc.KEY_UP):
				if self.new_ship_y - 1 >= 0:
					self.new_ship_y -= 1

			elif(self.key == uc.KEY_DOWN):
				if  self.new_ship_hor:
					if self.new_ship_y + 1 < self.player.board.size:
						self.new_ship_y += 1
				else:
					if self.new_ship_y + self.menu[self.menu_hi].length < self.player.board.size:
						self.new_ship_y += 1

			elif(self.key == ord('r') or self.key == ord('R')):
				if self.new_ship_hor:
					if self.new_ship_y + self.menu[self.menu_hi].length > self.player.board.size:
						self.new_ship_y = self.player.board.size - self.menu[self.menu_hi].length
				else:
					if self.new_ship_x + self.menu[self.menu_hi].length > self.player.board.size:
						self.new_ship_x = self.player.board.size - self.menu[self.menu_hi].length
				self.new_ship_hor = not self.new_ship_hor

			elif(self.key == ord('s') or self.key == ord('S')):
				s = self.player.board.suggest(self.menu[self.menu_hi].length)
				if type(s) != bool:
					x, y, h = s
					self.new_ship_x = x
					self.new_ship_y = y
					self.new_ship_hor = h

			elif(self.key == ord('\n')):
				if self.player.board.check_new_ship(self.new_ship_x, self.new_ship_y,
													self.menu[self.menu_hi].length,
													self.new_ship_hor):

					self.player.board.set_new_ship(self.new_ship_x, self.new_ship_y,
												   self.menu[self.menu_hi].id,
												   self.menu[self.menu_hi].length,
												   self.new_ship_hor)

					self.num_ships_set += 1
					if not self.all_set():
						self.on_menu = True

					self.menu = self.player.left_to_set()
					self.menu_hi = 0

		if self.key == ord('q') or self.key == ord('Q'):
			self.close()

		if self.key == ord('w') or self.key == ord('W'):
			uc.endwin()
			exit()

	def all_set(self):
		'''Returns ture if all ships are placed.'''
		return self.num_ships_set == len(self.player.ship_list)

	def close(self):
		uc.init_pair(1, uc.COLOR_WHITE, uc.COLOR_RED)

		prompt_start_x = self.max_x//2-19
		prompt_start_y = self.max_y//3

		if prompt_start_x < 1:
			prompt_start_x = 1
		if prompt_start_y < 1:
			prompt_start_y = 1

		win_prompt = uc.newwin(3, 38, prompt_start_y, prompt_start_x)
		uc.box(win_prompt, 0, 0)
		uc.mvwaddstr(win_prompt, 1, 1, 'Do you want to close the game? (y|n)')
		uc.wbkgd(win_prompt, uc.COLOR_PAIR(1))
		uc.wrefresh(win_prompt)

		answer = uc.wgetch(stdscr)
		if answer == ord('y') or answer == ord('Y'):
			uc.endwin()
			exit()
		else:
			uc.delwin(win_prompt)

	def del_wins(self):
		pass # If you don't know what to do!!

p = Player('Jannis', 10)

s = Set_ships(p)
try:
	while True:
		s.input()
		if s.all_set():
			break
		s.draw()
finally:
	uc.endwin()
