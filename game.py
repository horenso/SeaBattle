# The game class, all unicurses spesific settings should happen here,
# as the game should be implemetable with other types of GUIs as well
import unicurses as uc

stdscr = uc.initscr()

class Game:
	def __init__(self):

		uc.clean()
		uc.noecho() # Disable typing
		uc.cbreak() # catching characters directly without waiting for [ENTER]

		uc.curs_set(0) # Disable blinking curser

		uc.refresh()

		self.max_y, self.max_x = uc.getmaxyx(stdscr)

	def end_game(self):
		endwin()
		print("Thanks for playing")


try:
	g = Game()
finally:
	g.endwin()

g.end_game()
