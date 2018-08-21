class Ship:
	next_id = 1
	def __init__(self, name, length, placed=False):
		self.id = Ship.next_id
		Ship.next_id += 1

		self.name = name
		self.length = length
		self.placed = placed
		self.string = f"{self.name} ({self.length})" # I want to edit it from outside

	def __str__(self):
		return self.string

	def __eq__(self, other):
		'''Two ships are equal if they have the same name and the same length.'''
		return self.name == other.name and self.length == other.length

	def __hash__(self):
		'''Two ships are different objects (in a dict for example) if the have
		a differen name and a differenet length.'''
		return hash((self.name, self.length))

	def reset_id(self):
		'''Resets the id, since they are only relevant within one player object.'''
		Ship.next_id = 1
