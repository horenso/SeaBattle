import unicurses as uc
stdscr = uc.initscr()

from setships import SetShips
from player import Player


p = Player('Jannis', 10)

s = SetShips(p)
try:
	while True:
		s.input()
		if s.all_set():
			break
		s.draw()
finally:
	uc.endwin()
