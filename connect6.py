import numpy as np
import random
import pygame
import sys
import math
import tkinter as tk
from tkinter import simpledialog


"""
Connect Six Game Constants

This module defines constants used in a Connect Four game, including colors, player identifiers, and piece identifiers.

Colors:
- BLUE: RGB tuple representing the color blue.
- BLACK: RGB tuple representing the color black.
- RED: RGB tuple representing the color red.
- YELLOW: RGB tuple representing the color yellow.

Player Identifiers:
- PLAYER: Integer identifier for the human player.
- AI: Integer identifier for the artificial intelligence player.

Piece Identifiers:
- EMPTY: Integer identifier representing an empty slot on the game board.
- PLAYER_PIECE: Integer identifier representing a slot occupied by the human player's piece.
- AI_PIECE: Integer identifier representing a slot occupied by the artificial intelligence player's piece.

Usage:
- These constants can be imported into the main Connect Four game code to maintain consistency and readability.
- For example, to set a player's color:
    player_color = BLUE if current_player == PLAYER else RED
"""

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2


BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2


# get_board_size(): Prompts the user to enter the desired board size using a GUI and validates the input.
def get_board_size():
    while True:
        try:
            board_size = simpledialog.askinteger("Board Size", "Enter the desired board size (n):")
            if board_size is None:
                # User pressed Cancel
                print("Board size input canceled. Exiting.")
                exit()
            if board_size < 6:
                print("Board size must be at least 6. Please enter a valid size.")
            else:
                return board_size
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Get user input for the board size using GUI
board_size = get_board_size()

# Update the window length for larger board size
WINDOW_LENGTH = min(6, board_size)


# Define the create_board function
def create_board(n):
    board = np.zeros((n, n))
    return board


'''
    drop_piece(board, row, col, piece): Places a game piece on the game board at the specified row and column.

    Parameters:
    - board (numpy.ndarray): The Connect Four game board.
    - row (int): The row where the piece will be placed.
    - col (int): The column where the piece will be placed.
    - piece (int): The identifier for the player or AI piece (e.g., PLAYER_PIECE or AI_PIECE).

    Returns:
    - None: The function modifies the game board in-place.
'''
def drop_piece(board, row, col, piece):
    board[row][col] = piece



'''
    Function:
    - is_valid_location(board, col): Checks if the specified column is a valid location for placing a game piece.

    Parameters:
    - board (numpy.ndarray): The Connect Four game board.
    - col (int): The column to be checked for validity.

    Returns:
    - bool: True if the location is valid (empty in the bottom row), False otherwise.

'''
def is_valid_location(board, col):
    return board[board.shape[0] - 1][col] == 0


'''
    Function:
    - get_next_open_row(board, col): Finds the next available row in the specified column.

    Parameters:
    - board (numpy.ndarray): The Connect Four game board.
    - col (int): The column for which to find the next available row.

    Returns:
    - int: The row index of the next available (empty) row in the specified column.
'''
def get_next_open_row(board, col):
    for r in range(board.shape[0]):
        if board[r][col] == 0:
            return r

'''
    Function:
    - print_board(board): Prints the Connect Six game board with the bottom row at the top for better readability.

    Parameters:
    - board (numpy.ndarray): The Connect Six game board.

    Returns:
    - None: The function prints the board to the console.
'''
def print_board(board):
    print(np.flip(board, 0))


'''

    Function:
    - winning_move(board, piece): Checks for a winning move on the game board for a specified player or AI.

    Parameters:
    - board (numpy.ndarray): The Connect Six game board.
    - piece (int): The identifier for the player or AI piece (e.g., PLAYER_PIECE or AI_PIECE).

    Returns:
    - bool: True if there is a winning move, False otherwise.

'''
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(board.shape[1] - WINDOW_LENGTH + 1):
        for r in range(board.shape[0]):
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    
    # Check vertical locations for win
    for c in range(board.shape[1]):
        for r in range(board.shape[0] - WINDOW_LENGTH + 1):
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True
    
    # Check positively sloped diagonals
    for c in range(board.shape[1] - WINDOW_LENGTH + 1):
        for r in range(board.shape[0] - WINDOW_LENGTH + 1):
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    
    # Check negatively sloped diagonals
    for c in range(board.shape[1] - WINDOW_LENGTH + 1):
        for r in range(WINDOW_LENGTH - 1, board.shape[0]):
            if all(board[r - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True


'''
    Function:
    - evaluate_window(window, piece): Evaluates the score of a window of game pieces for a specified player or AI.

    Parameters:
    - window (list): A list representing a window of game pieces.
    - piece (int): The identifier for the player or AI piece (e.g., PLAYER_PIECE or AI_PIECE).

    Returns:
    - int: The score calculated based on the evaluation rules.
'''

# heuristic function
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 6:
        score += 1000
    elif window.count(piece) == 5 and window.count(EMPTY) == 1:
        score += 50
    elif window.count(piece) == 4 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 5 and window.count(EMPTY) == 1:
        score -= 40

    return score

'''
    Function:
    - score_position(board, piece): Scores the position of a Connect Six game board for a specified player or AI.

    Parameters:
    - board (numpy.ndarray): The Connect Six game board.
    - piece (int): The identifier for the player or AI piece (e.g., PLAYER_PIECE or AI_PIECE).

    Returns:
    - int: The overall score calculated based on the heuristic evaluation.
'''

# heuristic function
def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, board.shape[1] // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(board.shape[0]):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(board.shape[1] - 5):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(board.shape[1]):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(board.shape[0] - 5):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonal
    for r in range(board.shape[0] - 5):
        for c in range(board.shape[1] - 5):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(board.shape[0] - 5):
        for c in range(board.shape[1] - 5):
            window = [board[r + 5 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


'''

    Function:
    - is_terminal_node(board): Checks if the game has reached a terminal state.

    Parameters:
    - board (numpy.ndarray): The Connect Six game board.

    Returns:
    - bool: True if the game is in a terminal state, False otherwise.

'''

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


'''
    Function:
    - minimax(board, depth, alpha, beta, maximizingPlayer): Executes the Minimax algorithm to find the best move.

    Parameters:
    - board (numpy.ndarray): The Connect Six game board.
    - depth (int): The depth of the search tree in the algorithm.
    - alpha (float): The alpha value for alpha-beta pruning.
    - beta (float): The beta value for alpha-beta pruning.
    - maximizingPlayer (bool): True if the current player is the AI (maximizing), False if the current player is the human player (minimizing).

    Returns:
    - tuple: The best move (column) and its corresponding score.
'''

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


'''

    Function:
    - get_valid_locations(board): Finds valid locations for placing a game piece on the game board.

    Parameters:
    - board (numpy.ndarray): The Connect Six game board.

    Returns:
    - list: A list of valid locations (columns) where a piece can be placed.

'''


def get_valid_locations(board):
    valid_locations = []
    for col in range(board.shape[1]):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


'''

    Function:
    - pick_best_move(board, piece): Picks the best move for a specified player or AI.

    Parameters:
    - board (numpy.ndarray): The Connect Six game board.
    - piece (int): The identifier for the player or AI piece (e.g., PLAYER_PIECE or AI_PIECE).

    Returns:
    - int: The best move (column) for the specified player or AI.

'''
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


'''
    Function:
    - draw_board(board): Draws the Connect Six game board on the screen.

    Parameters:
    - board (numpy.ndarray): The Connect Four game board.

    Returns:
    - None: The function updates the Pygame display.

'''
def draw_board(board):
    # Dynamically adjust circle size based on the board size
    circle_radius = int(min(SQUARESIZE / 2 - 5, height / (2 * board.shape[0])))

    for c in range(board.shape[1]):
        for r in range(board.shape[0]):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            
            pygame.draw.circle(screen, BLACK,
                               (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                circle_radius)

    for c in range(board.shape[1]):
        for r in range(board.shape[0]):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), circle_radius)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), circle_radius)

    pygame.display.update()


# Create the game board
board = create_board(board_size)

# Initialize the game state
game_over = False

# Print the initial board
print_board(board)

# Initialize pygame
pygame.init()

# Set the size of each square on the board
SQUARESIZE = min(800 // board_size, 100)

# Set the width and height of the board based on the size of the board
width = board.shape[1] * SQUARESIZE
height = (board.shape[0] + 1) * SQUARESIZE

# Dynamically adjust window size based on the board size
if board_size > 6:
    width = min(width, 800)
    height = min(height, 800)

size = (width, height)

# Set the radius of each game piece
RADIUS = int(SQUARESIZE / 2 - 5)

# Create the game window
screen = pygame.display.set_mode(size)

# Draw the initial board
draw_board(board)

# Update the display
pygame.display.update()

# Set the font for displaying messages
myfont = pygame.font.SysFont("monospace", 75)

# Determine the starting player
turn = random.randint(PLAYER, AI)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True  # Set the game_over flag to exit the loop

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True
                elif winning_move(board, AI_PIECE):
                    label = myfont.render("Ai wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True
                elif len(get_valid_locations(board)) == 0:
                    label = myfont.render("It's a draw!", 1, (255, 255, 255))
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board)

    if turn == AI and not game_over:
        col, minimax_score = minimax(board, 3, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

        if winning_move(board, AI_PIECE):
                label = myfont.render("AI wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
        elif len(get_valid_locations(board)) == 0:
                label = myfont.render("It's a draw!", 1, (255, 255, 255))
                screen.blit(label, (40, 10))
                game_over = True

        print_board(board)
        draw_board(board)

        turn += 1
        turn = turn % 2

    if game_over:
        pygame.time.delay(2000)  # Increased delay to 3 seconds

# Quit pygame and exit the program
pygame.quit()
sys.exit()
