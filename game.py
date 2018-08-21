import unicurses as uc
# stdscr = uc.initscr()
#
# class Game:
# 	def __init__(self):
# 		uc.noecho() # Disable typing on the screen
# 		uc.cbreak() # catching characters directly without waiting for [ENTER]
# 		uc.curs_set(0) # Disable blinking curser
# 		uc.keypad(stdscr, True) # for catching the arrow keys
#
# 		uc.start_color()
#
# 		Game.max_y, Game.max_x = uc.getmaxyx(stdscr)

def close(max_x, max_y):
	prompt_start_x = max_x//2-19
	prompt_start_y = max_y//3

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
