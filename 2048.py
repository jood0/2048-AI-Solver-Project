# Importing libraries
import random
import numpy as np
from tabulate import tabulate
import time

# GAME CODE

'''
Resources:

GAME:
https://numpy.org/doc/stable/user/
https://en.wikipedia.org/wiki/2048_(video_game)
https://www.geeksforgeeks.org/2048-game-in-python/
https://play2048.co/

'''


game_score = 0

def board_init():
  # declare an empty board (4x4 grid of 0's)
  board = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])

  # based on the game 2048, 2 random tiles are spawned is start
  board = spawn_random_tile(board)
  board = spawn_random_tile(board)

  return board


def spawn_random_tile(board):
  empty_spots = []
  # go through the board and find the empty cells
  for row in range(4):
    for column in range(4):
      if board[row][column] == 0:
        empty_spots.append([row, column])

  if not empty_spots:
    return board

  row, column = random.choice(empty_spots)

  # basad on the 2048 game author, 2 is 90% likely, 4 is 10% likely
  if random.random() < 0.90:
    board[row][column] = 2
  else:
    board[row][column] = 4

  return board


def merge(row):
  global game_score

  new_row = []

  for num in row:
    if num != 0:
      new_row.append(num)

  for num in range(len(new_row) - 1):
    if new_row[num] == new_row[num + 1]:
      new_row[num] *= 2
      game_score += new_row[num]
      new_row[num + 1] = 0

  new_row2 = []

  for num in new_row:
    if num != 0:
      new_row2.append(num)

  while(len(new_row2) < 4):
    new_row2.append(0)

  return new_row2


def transpose(board):
  transposed = []
  for row in range(4):
    new_row = []
    for col in range(4):
      new_row.append(board[col][row])
    transposed.append(new_row)
  return transposed


def move(board, direction):
  # transpose the matrix for easy merging if up, down, or right
  # left merging is the simplest, so transpose to make each operation left merging and revert back
  if direction == "up":
    board = transpose(board)

  elif direction == "down":
    board = transpose(board)

    rev_board = []
    for row in board:
      rev_row = row[::-1]
      rev_board.append(rev_row)

    board = rev_board

  elif direction == "right":
    rev_board = []
    for row in board:
      rev_row = row[::-1]
      rev_board.append(rev_row)
    board = rev_board


  # merge
  for row in range(4):
    board[row] = merge(board[row])

  # transpose back
  if direction == "up":
    board = transpose(board)

  elif direction == "down":
    rev_board = []
    for row in board:
      rev_row = row[::-1]
      rev_board.append(rev_row)

    board = transpose(rev_board)

  elif direction == "right":
    rev_board = []
    for row in board:
      rev_row = row[::-1]
      rev_board.append(rev_row)
    board = rev_board

  return board


def isSpaceForMove(board):
  if np.any(np.array(board) == 0):
        return True

  # Second check: Are there any adjacent equal numbers?
  # Check horizontally
  for i in range(4):
      for j in range(3):
          if board[i][j] == board[i][j + 1]:
              return True

  # Check vertically
  for i in range(3):
      for j in range(4):
          if board[i][j] == board[i + 1][j]:
              return True

  # If we get here, no moves are possible
  return False

def highestTileValue(board):
    max_tile = 0
    for row in range(4):
      for col in range(4):
        if board[row][col] > max_tile:
          max_tile = board[row][col]
    return max_tile


def print_board(board):
  global game_score
  # print(f"Score: {game_score}")
  print(f"Highest Tile: {highestTileValue(board)}")
  game_board = tabulate(board, tablefmt="fancy_grid")
  print(game_board)


def play():
  global game_score
  score = 0

  board = board_init()

  while isSpaceForMove(board):
    print_board(board)
    # input validation
    direction_to_move = ""
    valid_moves = ["w", "a", "s", "d"]
    while direction_to_move not in valid_moves:

        direction_to_move = input("Enter your move (w, a, s, d): ").strip().lower()
        if direction_to_move not in valid_moves:
            print("Invalid input. Please enter a valid move.")

    prev_board = board.copy()

    if direction_to_move == 'w':
      board = move(board, 'up')
    elif direction_to_move == 'a':
      board = move(board, 'left')
    elif direction_to_move == 's':
      board = move(board, 'down')
    elif direction_to_move == 'd':
      board = move(board, 'right')

    if not np.array_equal(prev_board, board):
      board = spawn_random_tile(board)

  print_board(board)

# HEURISTICS:
'''
Resources:
https://www.wikihow.com/Beat-2048
https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
'''

#1
def amountofemptytile(board):
  empty_tiles = 0
  for row in range(4):
    for col in range(4):
      if board[row][col] == 0:
        empty_tiles += 1
  return empty_tiles

#2
# Largest Tile is already defined above

#3
def adjHeuristic(board):

    ADJACENCY_WEIGHTS = [[4**6, 4**5, 4**4, 4**3],
                         [4**5, 4**4, 4**3, 4**2],
                         [4**4, 4**3, 4**2, 4**1],
                         [4**3, 4**2, 4**1, 4**0]]

    h = 0
    for i in range(4):
        for j in range(4):
            h += board[i][j] * ADJACENCY_WEIGHTS[i][j]
    return h

#4
def SnakePattern(board):
    board = np.array(board)

    WEIGHT_MATRIX = np.array([
        [2**15, 2**14, 2**13, 2**12],
        [2**8,  2**9,  2**10, 2**11],
        [2**7,  2**6,  2**5,  2**4],
        [2**0,  2**1,  2**2,  2**3]
    ])

    EMPTY_WEIGHT = 100.0      # Weight for empty cells
    SNAKE_WEIGHT = 1000.0     # Weight for snake pattern
    MERGE_WEIGHT = 10.0       # Weight for potential merges

    score = 0

    # 1. Snake pattern score: multiply each tile by its position weight
    snake_score = np.sum(board * WEIGHT_MATRIX)
    score += SNAKE_WEIGHT * snake_score

    # 2. Empty tiles bonus
    empty_cells = len(np.where(board == 0)[0])
    score += EMPTY_WEIGHT * empty_cells

    # 3. Mergeable tiles bonus
    for i in range(4):
        for j in range(3):
            # Horizontal merges
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                score += MERGE_WEIGHT * board[i][j]

            # Vertical merges
            if i < 3:
                if (j % 2 == 0 and board[i][j] == board[i + 1][j]) or \
                   (j % 2 == 1 and board[i][j] == board[i - 1][j]):
                    score += MERGE_WEIGHT * board[i][j]

    # 4. Penalty for not following snake pattern
    for i in range(3):
        for j in range(4):
            if j % 2 == 0:  # Even columns should decrease downward
                if i < 3 and board[i][j] < board[i + 1][j] and board[i][j] != 0:
                    score -= abs(board[i][j] - board[i + 1][j])
            else:  # Odd columns should increase downward
                if i < 3 and board[i][j] > board[i + 1][j] and board[i][j] != 0:
                    score -= abs(board[i][j] - board[i + 1][j])

    return score

# Evaluate Function (adding weights to heuristic):

def evalaute_function(board):
  # (A * Heuristic1) + (B * Heuristic2) + (C * Heuristic3)
  # Removed the Largest Tile Heuristic as it was negatively affecting performance.

  weightOfEmptyTiles,  weightOfMergeCount, weightOfSnakePattern = 0.5, 1, 1.5

  weightedEmptyTiles = amountofemptytile(board) * weightOfEmptyTiles
  weightedMergeCount = adjHeuristic(board) * weightOfMergeCount
  weightedSnakePattern = SnakePattern(board) * weightOfSnakePattern

  return weightedEmptyTiles + weightedMergeCount + weightedSnakePattern


# ExpectiMax:
def expectimax(board, depth, player_turn):
    if depth == 0:
        return evalaute_function(board)

    if player_turn:
        # Player's turn: try all possible moves
        max_score = float('-inf')
        moves = ['up', 'down', 'left', 'right']

        for direction in moves:
            new_board = board.copy()
            new_board = move(new_board, direction)

            if not np.array_equal(new_board, board):
                score = expectimax(new_board, depth - 1, False)
                max_score = max(max_score, score)

        return max_score if max_score != float('-inf') else evalaute_function(board)

    else:
        board = np.array(board)
        empty_cells = np.where(board == 0)
        if len(empty_cells[0]) == 0:
            return evalaute_function(board)

        avg_score = 0
        num_possibilities = len(empty_cells[0])

        for i in range(num_possibilities):
            row, col = empty_cells[0][i], empty_cells[1][i]

            # Try spawning a 2 (90% probability)
            new_board = board.copy()
            new_board[row, col] = 2
            avg_score += 0.9 * expectimax(new_board, depth - 1, True) / num_possibilities

            # Try spawning a 4 (10% probability)
            new_board = board.copy()
            new_board[row, col] = 4
            avg_score += 0.1 * expectimax(new_board, depth - 1, True) / num_possibilities

        return avg_score



# Minimax with alpha beta pruning (to compare w/ Expectimax)
def minimax(board, alpha, beta, depth, player_turn):
    if depth == 0:
        return evalaute_function(board)

    if player_turn:
        # Player's turn: try all possible moves
        max_score = float('-inf')
        moves = ['up', 'down', 'left', 'right']

        for direction in moves:
            new_board = board.copy()
            new_board = move(new_board, direction)

            if not np.array_equal(new_board, board):
                score = minimax(new_board, alpha, beta, depth - 1, False)
                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                if max_score >= beta:
                  break

        return max_score if max_score != float('-inf') else evalaute_function(board)

    else:
        min_score = float('inf')
        board = np.array(board)
        empty_cells = np.where(board == 0)
        if len(empty_cells[0]) == 0:
            return evalaute_function(board)

        num_possibilities = len(empty_cells[0])

        for i in range(num_possibilities):
            row, col = empty_cells[0][i], empty_cells[1][i]

            # Try spawning a 2 (90% probability)
            new_board = board.copy()
            new_board[row, col] = 2
            score = minimax(new_board, alpha, beta, depth - 1, True)
            min_score = min(min_score,score)
            beta = min(min_score, beta)
            if min_score <= alpha:
              break
            # Try spawning a 4 (10% probability)
            new_board = board.copy()
            new_board[row, col] = 4
            score = minimax(new_board, alpha, beta, depth - 1, True)
            min_score = min(min_score,score)
            beta = min(min_score, beta)
            if min_score <= alpha:
              break
        return min_score if min_score != float('inf') else evalaute_function(board)



# Find the best move in the game tree based on ExpectiMax
def get_best_move(board, depth):
    moves = ['up', 'down', 'left', 'right']
    best_score = float('-inf')
    best_move = None

    for direction in moves:
        new_board = board.copy()
        new_board = move(new_board, direction)

        if not np.array_equal(new_board, board):
            score = expectimax(new_board, depth, player_turn=False)
            if score > best_score:
                best_score = score
                best_move = direction

    return best_move

# Play 2048 w/ ExpectiMax Algorithm (1 simulation and shows the board)
def play_ai(show_each_move=True):
    global game_score
    game_score = 0
    board = board_init()

    # Loop until no moves left
    while isSpaceForMove(board):
        if show_each_move:
            print_board(board)
        best_move = get_best_move(board, 3) # Change depth here (currently it is 3)
        if best_move is None:
            # No moves available (should already be caught by isSpaceForMove, but just in case)
            break

        prev_board = board.copy()
        board = move(board, best_move)

        # If the board changed, spawn a random tile
        if not np.array_equal(prev_board, board):
            board = spawn_random_tile(board)

    print("Game Over!")
    print_board(board)

play_ai()

# # RUN SIMULATION TO SEE HOW MANY TIMES IT SCORES 2048 IN ___ TRIALS

# def run_single_game(depth):
#     global game_score
#     score = 0
#     board = board_init()

#     # Run the game until no moves left
#     while isSpaceForMove(board):
#         best_move = get_best_move(board, depth)
#         if best_move is None:
#             break
#         prev_board = board.copy()
#         board = move(board, best_move)
#         if not np.array_equal(prev_board, board):
#             board = spawn_random_tile(board)
#     return highestTileValue(board)


# def run_experiment(num_runs):
#     # Change depth here
#     depth = 2
#     hits_2048 = 0
#     total_time = 0  # To track total time for all runs

#     for i in range(1, num_runs + 1):
#         start_time = time.time()  # Start timing
#         highest_tile = run_single_game(depth)
#         end_time = time.time()  # End timing

#         run_time = end_time - start_time
#         total_time += run_time

#         print(f"Run {i}: Highest tile was {highest_tile}, Time taken: {run_time:.2f} seconds")

#         if highest_tile >= 2048:
#             hits_2048 += 1

#     print(f"Reached 2048 {hits_2048} times out of {num_runs} runs.")
#     print(f"Total time for {num_runs} runs: {total_time:.2f} seconds")
#     print(f"Average time per run: {total_time / num_runs:.2f} seconds")


# # pass in how many simulation to run (3 would be 3 games of 2048 played by AI)
# run_experiment(10)