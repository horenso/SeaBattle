class Ship:
	next_id = 0
	def __init__(self, name, length, placed=False):
		Ship.next_id += 1

		self.id = Ship.next_id
		self.name = name
		self.length = length
		self.placed = placed
		self.string = f"{self.name} ({self.length})" # I want to edit it from outside

	def __str__(self):
		return self.string

	def __eq__(self, other):
		"""Two ships are equal if they have the same name and the same length"""
		return self.name == other.name and self.length == other.length

	def __hash__(self):
		"""Two ships are different objects (in a dict for example) if the have
		a differen name and a differenet length"""
		return hash((self.name, self.length))
