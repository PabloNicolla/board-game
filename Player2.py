from GameTree import GameTree


class PlayerTwo:

    def __init__(self, name="P2 Bot"):
        self.name = name
        self.difficulty = 4

    def get_name(self):
        return self.name

    def get_play(self, board):
        tree = GameTree(board, -1, self.difficulty)
        (row, col) = tree.get_move()
        return (row, col)

    # Set the difficulty of the player
    def change_difficulty(self, new_difficulty):
        self.difficulty = new_difficulty
