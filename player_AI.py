from player import Player

default = [Ship('Aircraft carrier', 5), Ship('Battleship', 4),
		   Ship('Cruiser', 2), Ship('Cruiser', 2), Ship('Cruiser', 2), Ship('Destroyer', 1)]

class Player_AI(Player):
	def __str__(self):
		"""Returns the player's name"""
		return f'{self.name}'

	def left_to_set(self):
		"""Returns a sorted list of ship objects which yet need to be set."""
		dupl = [deepcopy(ship) for ship in self.ship_list if not ship.placed]
		left = []
		for ship in set(dupl):
			count = sum(1 for s in dupl if s == ship)
			if count > 1:
				ship.string = f"{count}x {ship}"
				left.append(ship)
			else:
				left.append(ship)
		return sorted(left, key=lambda s: (s.name, s.length))

		# it should only name nx shipname to the ship on the layer fuurtherst up!!!!!!!!!!!!!!
