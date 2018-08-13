from player import Player

player1 = Player("Jannis", 10)

# print(player1.board)
for i in range(5):
    player1.board.auto_set_new_ship(3)
print(player1.board)
