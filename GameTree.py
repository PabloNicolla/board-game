from Overflow import overflow


def copy_board(board):
    current_board = []
    height = len(board)
    for i in range(height):
        current_board.append(board[i].copy())
    return current_board


def evaluate_board(board, player):
    height = len(board)
    width = len(board[0])
    win_score = len(board) * len(board[0]) * 20
    player_points, opponent_points = 0, 0

    if player == 1:
        for row_index in range(height):
            for col_index in range(width):
                cell = board[row_index][col_index]

                if cell > 0:
                    player_points += cell_score(board,
                                                player, row_index, col_index)
                elif cell < 0:
                    opponent_points += cell_score(board,
                                                  player, row_index, col_index)

        if player_points == 0:
            return -win_score
        elif opponent_points == 0:
            return win_score
        else:
            return player_points - abs(opponent_points)

    elif player == -1:
        for row_index in range(height):
            for col_index in range(width):
                cell = board[row_index][col_index]

                if cell < 0:
                    player_points += cell_score(board,
                                                player, row_index, col_index)
                elif cell > 0:
                    opponent_points += cell_score(board,
                                                  player, row_index, col_index)

        if player_points == 0:
            return -win_score
        elif opponent_points == 0:
            return win_score
        else:
            return abs(player_points) - opponent_points


def cell_score(board, player, row, col):
    height, width = len(board), len(board[0])
    cell_value = board[row][col]

    def get_position_score(row, col):
        # Enhanced positional scoring
        if (row in [0, height-1] and col in [0, width-1]):
            return 5  # Corners are more valuable
        elif row in [0, height-1] or col in [0, width-1]:
            return 3  # Edges have intermediate value
        else:
            return 1  # Center cells

    def calculate_overflow_potential(row, col, position_score):
        neighbors = 4 - (row in [0, height-1]) - (col in [0, width-1])
        overflow_potential = (
            abs(cell_value) / max(1, neighbors)) * position_score
        return overflow_potential

    def calculate_capture_potential(board, player, row, col):
        enemy_gems = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row+i < len(board) and 0 <= col+j < len(board[0]):
                    if (board[row+i][col+j] * player < 0):  # Opponent's cell
                        enemy_gems += abs(board[row+i][col+j])
        # Adjust the multiplier based on game strategy
        capture_potential = enemy_gems * 0.5
        return capture_potential

    def calculate_strategic_value(board, player, row, col):
        # Example: Increase value for cells that block opponent's progress
        strategic_value = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row+i < len(board) and 0 <= col+j < len(board[0]):
                    if board[row+i][col+j] * player > 0:  # Adjacent ally cells
                        strategic_value += 1  # Encourage clustering for defense
                    elif board[row+i][col+j] == 0:  # Neutral cells
                        strategic_value += 0.5  # Potential for expansion
        return strategic_value

    position_score = get_position_score(row, col)
    overflow_potential = calculate_overflow_potential(
        row, col, position_score)
    capture_potential = calculate_capture_potential(
        board, player, row, col)
    strategic_value = calculate_strategic_value(board, player, row, col)

    # Summing up the individual scores for the final cell score
    return overflow_potential + capture_potential + strategic_value


class GameTree:
    class Node:
        def __init__(self, board, depth, player, tree_height=4):
            self.board = board
            self.depth = depth
            self.player = player
            self.tree_height = tree_height
            self.children = []
            self.board_eval = None
            self.move = None

        def create_child(self):
            if self.depth == self.tree_height - 1:
                return

            possible_moves = []
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    if self.board[row][col] == 0 or self.board[row][col] * self.player > 0:
                        possible_moves.append((row, col))

            for move in possible_moves:
                new_board = copy_board(self.board)
                new_board[move[0]][move[1]] += self.player
                overflow(new_board)
                new_node = GameTree.Node(
                    new_board, self.depth + 1, -self.player, self.tree_height)
                new_node.move = move
                self.children.append(new_node)

    def __init__(self, board, player, tree_height=4):
        self.player = player
        self.height = tree_height
        self.board = copy_board(board)
        self.root = self.Node(self.board, 0, self.player, self.height)
        self.create_tree(self.root)
        self.minimax(self.root)

    def create_tree(self, node):
        node.create_child()
        for child in node.children:
            self.create_tree(child)

    def minimax(self, node, a=float('-inf'), b=float('inf')):
        if not node.children:
            node.board_eval = evaluate_board(node.board, self.player)

            return node.board_eval

        if node.player == self.player:
            max_eval = float('-inf')
            for child in node.children:
                evaluation = self.minimax(child, a, b)
                max_eval = max(max_eval, evaluation)
                a = max(a, evaluation)
                if b <= a:
                    break
            node.board_eval = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                evaluation = self.minimax(child, a, b)
                min_eval = min(min_eval, evaluation)
                b = min(b, evaluation)
                if b <= a:
                    break
            node.board_eval = min_eval
            return min_eval

    def get_move(self):
        if self.root.board_eval is None:
            self.minimax(self.root, self.player)

        best_move = None
        best_value = float('-inf')
        for child in self.root.children:
            if child.board_eval > best_value:
                best_value = child.board_eval
                best_move = child.move
        return best_move

    def clear_tree(self):
        self.clear_tree_r(self.root)

    def clear_tree_r(self, node):
        for child in node.children:
            self.clear_tree_r(child)
        node.children = []
