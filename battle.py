from player import Player
import unicurses as uc

class Battle:
	def __init__(self, player, player_enemy):
		self.player = player
		self.player_enemy = player_enemy

		self.player.board.show_cur = True

		self.str_title = f'Battle between {self.player.name} and {self.player_enemy.name}'

		self.max_y, self.max_x = uc.getmaxyx(stdscr)

		self.init_colors()

		self.init_wins()

	def __del__(self):
		uc.del_panel(self.pan_board)
		uc.delwin(self.win_board)
		uc.delwin(self.win_board)

		uc.delwin(self.win_boardarea)
		uc.delwin(self.win_shipmenu)
		uc.delwin(self.win_statusbar)
		uc.delwin(self.win_title)

	def init_wins(self):
		'''Creates win and panel objects. '''
		uc.wclear(stdscr)
		self.max_y, self.max_x = uc.getmaxyx(stdscr)

		self.win_title = uc.newwin(3, self.max_x, 0, 0) #(h, w, starty, startx)
		self.win_boardarea = uc.newwin(self.max_y-4, self.max_x, 3, 0)
		self.win_statusbar = uc.newwin(1, self.max_x, self.max_y-1, 0)

		x, y = self.player.board.str_size()
		self.win_board1 = uc.newwin(y, x+2, 0, 0)
		self.win_board2 = uc.newwin(y, x+2, 0, 0)

		self.pan_board1 = uc.new_panel(self.win_board1)
		self.pan_board2 = uc.new_panel(self.win_board2)

		uc.move_panel(self.pan_board1, 0, 0)
		uc.move_panel(self.pan_board2, 0, 0)

		uc.wrefresh(stdscr)
		self.draw_all()

	def init_colors(self):
		# Draw board
		# uc.init_pair(11, uc.COLOR_BLUE, uc.COLOR_BLACK)

	def draw_title(self):
		uc.box(self.win_title, 0, 0)
		uc.wmove(self.win_title, 1, 2)
		uc.waddstr(self.win_title, self.str_title)
		uc.wrefresh(self.win_title)

	def draw_board(self):
		uc.wclear(self.win_board1)
		uc.wclear(self.win_baord2)

		uc.box(self.win_boardarea, 0, 0)

		uc.wmove(self.win_boardarea, 1, 2)

		s1 = self.player.board.__str__()
		s2 = self.player_enemy.board.__str__()

		for chr in s1:
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

		uc.wbkgd(self.win_statusbar, uc.COLOR_PAIR(4))
		uc.wrefresh(self.win_statusbar)

	def draw_all(self):
		self.draw_board()
		self.draw_title()
		self.draw_shipmenu()
		self.draw_statusbar()

	def input(self):
		self.key = uc.wgetch(stdscr)

		if self.key == ord('q') or self.key == ord('Q'):
			self.close()

		if self.key == ord('w') or self.key == ord('W'):
			uc.endwin()
			exit()

	def close(self):
		'''Lets a close prompt pop up. '''
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
