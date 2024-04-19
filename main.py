#   the gem images used are from opengameart.org by qubodup
#   https://opengameart.org/content/rotating-crystal-animation-8-step,
#   https://creativecommons.org/licenses/by/3.0/

import pygame
import sys
import math

from Overflow import overflow
from SimpleQueue import Queue
from Player1 import PlayerOne
from Player2 import PlayerTwo


class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y,
                         self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (
                    self.current_option + 1) % len(self.options)

    def get_choice(self):
        return self.current_option


class Board:
    def __init__(self, width, height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.game_board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.game_board[0][0] = 1
        self.game_board[self.height-1][self.width-1] = -1
        self.turn = 0
        self.previous_board_p1 = None  # For undo for player 1
        self.previous_board_p2 = None  # For undo for player 2

    def get_board(self):
        current_board = []
        for i in range(self.height):
            current_board.append(self.game_board[i].copy())
        return current_board

    def valid_move(self, row, col, player):
        if row >= 0 and row < self.height and col >= 0 and col < self.width and (self.game_board[row][col] == 0 or self.game_board[row][col]/abs(self.game_board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player):
        if self.valid_move(row, col, player):
            # If player is human, save the previous board state
            if player == 1:
                self.previous_board_p1 = self.get_board()
            elif player == -1:
                self.previous_board_p2 = self.get_board()
            # If the move is valid, add the piece to the board
            self.game_board[row][col] += player
            # Increment the turn counter
            self.turn += 1
            return True
        return False

    def check_win(self):
        if (self.turn > 0):
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if (self.game_board[i][j] > 0):
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif (self.game_board[i][j] < 0):
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if (num_p1 == 0):
                return -1
            if (num_p2 == 0):
                return 1
        return 0

    def do_overflow(self, q):
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.game_board[i].copy())
        numsteps = overflow(self.game_board, q)
        if (numsteps != 0):
            self.set(oldboard)
        return numsteps

    def set(self, newboard):
        for row in range(self.height):
            for col in range(self.width):
                self.game_board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET,
                                   row * CELL_SIZE+Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.game_board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.game_board[row][col] > 0:
                        sprite = p1_sprites
                    else:
                        sprite = p2_sprites
                    if abs(self.game_board[row][col]) == 1:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.game_board[row][col]) == 2:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

                    elif abs(self.game_board[row][col]) == 3:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.game_board[row][col]) == 4:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

    '''
    This method should undo the last move made by the player
    Parameters:
        player: The player who made the last move
    Returns:
        True if the move was successfully undone, False otherwise
    '''

    def undo_last_move(self, player):
        # Check if the player is player 1 and there is a previous board state to revert to
        if player == 1 and self.previous_board_p1:
            # Revert the board to the previous state
            self.set(self.previous_board_p1)
            # Reset the previous board states to None
            self.previous_board_p2 = None
            self.previous_board_p1 = None
            # Switch the turn back to the player who made the move
            self.turn -= 1
            return True
        # Check if the player is player 2 and there is a previous board state to revert to
        elif player == -1 and self.previous_board_p2:
            # Revert the board to the previous state
            self.set(self.previous_board_p2)
            # Reset the previous board states to None
            self.previous_board_p2 = None
            self.previous_board_p1 = None
            # Switch the turn back to the player who made the move
            self.turn -= 1
            return True
        # If the player is not human or there is no previous board state to revert to, return False
        return False

    '''
    This method calculates the scores of the players
    Returns:
        The scores of player 1 and player 2
    '''

    def calculate_scores(self):
        p1_score = 0
        p2_score = 0
        # Iterate through the board and count the number of cells occupied by each player
        for row in range(self.height):
            for col in range(self.width):
                if self.game_board[row][col] > 0:
                    p1_score += 1
                elif self.game_board[row][col] < 0:
                    p2_score += 1
                    # Return the scores of player 1 and player 2
        return p1_score, p2_score


# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5

# hate the colours?  there are other options.  Just change the lines below to another colour's file name.
# the following are available blue, pink, yellow, orange, grey, green
p1spritesheet = pygame.image.load('images/blue.png')
p2spritesheet = pygame.image.load('images/pink.png')

undo_button_image = pygame.image.load(
    'images/undo_button_image.png')  # Load the undo button image
# Resize the undo button image to a smaller size
undo_button_image = pygame.transform.scale(undo_button_image, (50, 50))
# Get the rect of the undo button image
undo_button_rect = undo_button_image.get_rect()
undo_button_rect.topleft = (750, 50)  # Set the position of the undo button

p1_sprites = []
p2_sprites = []


player_id = [1, -1]


for i in range(8):
    curr_sprite = pygame.Rect(32*i, 0, 32, 32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))


frame = 0

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200, 800))

pygame.font.init()
font = pygame.font.Font(None, 36)  # Change the size as needed
bigfont = pygame.font.Font(None, 108)
# Create the game board
# board = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])


status = ["", ""]
current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)
# Game loop
running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]
# Difficulty buttons
buttons = {
    "Hard": (850, 200, 100, 50),
    "Normal": (850, 260, 100, 50),
    "Easy": (850, 320, 100, 50),
}

"""
This function draws text on the window
Parameters:
    window: The window to draw the text on
    text: The text to display
    position: The position to display the text
    font: The font to use for the text
    color: The color of the text
Returns:
    None
"""


def draw_text(window, text, position, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, position)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            choice[0] = player1_dropdown.get_choice()
            choice[1] = player2_dropdown.get_choice()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE
                # Check if the undo button is clicked
                if undo_button_rect.collidepoint(x, y):
                    # Check if the players are humans
                    if choice[0] == 0 and choice[1] == 0:
                        # Call the undo_last_move method in the Board class
                        had_undo = board.undo_last_move(
                            player_id[current_player] * -1)
                        if had_undo:
                            # Switch the turn back to the previous player
                            current_player = (current_player + 1) % 2
                    else:
                        # If the players are not humans undo to the last player's move
                        board.undo_last_move(player_id[current_player])

                # check difficulty buttons
                for label, (bx, by, bwidth, bheight) in buttons.items():
                    if bx <= x <= bx + bwidth and by <= y <= by + bheight:
                        print(f"{label} button was clicked")
                        # Change the difficulty of the bots based on the button clicked
                        # Hard = 4, Normal = 3, Easy = 2
                        if label == "Hard":
                            bots[0].change_difficulty(4)
                            bots[1].change_difficulty(4)
                        elif label == "Normal":
                            bots[0].change_difficulty(3)
                            bots[1].change_difficulty(3)
                        elif label == "Easy":
                            bots[0].change_difficulty(2)
                            bots[1].change_difficulty(2)

    win = board.check_win()
    if win != 0:
        winner = 1
        if win == -1:
            winner = 2
        has_winner = True

    if not has_winner:
        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next = overflow_boards.dequeue()
                    board.set(next)
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False

                # goes between 0 and 1
                current_player = (current_player + 1) % 2

        else:
            status[0] = "Player " + str(current_player + 1) + "'s turn"
            make_move = False
            if choice[current_player] == 1:
                (grid_row, grid_col) = bots[current_player].get_play(
                    board.get_board())
                status[1] = "Bot chose row {}, col {}".format(
                    grid_row, grid_col)
                if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                    has_winner = True
                    # if p1 makes an invalid move, p2 wins.  if p2 makes an invalid move p1 wins
                    winner = ((current_player + 1) % 2) + 1
                else:
                    make_move = True
            else:
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True

            if make_move:
                board.add_piece(grid_row, grid_col, player_id[current_player])
                numsteps = board.do_overflow(overflow_boards)
                if numsteps != 0:
                    overflowing = True
                    repeat_step = 0
                else:
                    # goes between 0 and 1
                    current_player = (current_player + 1) % 2

                grid_row = -1
                grid_col = -1

    # Draw the game board
    window.fill(WHITE)
    board.draw(window, frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))

    """
    This function draws the buttons on the window
    Parameters:
        window: The window to draw the buttons on
        label: The label to display on the button
        x: The x position of the button
        y: The y position of the button
        width: The width of the button
        height: The height of the button
    Returns:
        None
    """
    def draw_button(window, label, x, y, width, height):
        # Draw the button
        pygame.draw.rect(window, BLACK, (x, y, width, height))
        # Draw the text on the button
        font = pygame.font.Font(None, 36)
        # Render the text
        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(x + width / 2, y + height / 2))
        window.blit(text, text_rect)

    # Constants for button sizes and positions
    button_width = 100
    button_height = 50
    button_start_x = 850  # Starting X position for the first button
    button_start_y = 200  # Starting Y position
    button_spacing = 60  # Space between buttons

    # Drawing the buttons
    # Button for hard difficulty
    draw_button(window, "Hard", button_start_x,
                button_start_y, button_width, button_height)
    # Button for normal difficulty
    draw_button(window, "Normal", button_start_x, button_start_y +
                button_spacing, button_width, button_height)
    # Button for easy difficulty
    draw_button(window, "Easy", button_start_x, button_start_y +
                2 * button_spacing, button_width, button_height)

    # Draw the undo button image
    window.blit(undo_button_image, undo_button_rect)
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)

    if not has_winner:
        text = font.render(status[0], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET, 750))
        text = font.render(status[1], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET,  700))
    else:
        text = bigfont.render("Player " + str(winner) +
                              " wins!", True, (0, 0, 0))  # Black color
        window.blit(text, (300, 250))

    # Calculate scores
    p1_score, p2_score = board.calculate_scores()

    # Display scores
    score_font = pygame.font.Font(None, 36)  # Adjust size as needed
    draw_text(window, f"P1 Score: {p1_score}", (10, 10), score_font, BLACK)
    draw_text(window, f"P2 Score: {p2_score}", (10, 50), score_font, BLACK)

    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
