# 2048 AI Solver

An autonomous solver for the game **2048** built in Python using the **Expectimax search algorithm** and heuristic board evaluation.

The program implements the complete game logic, evaluates possible future board states, models random tile generation, and selects the move with the highest expected outcome.

---

## Overview

2048 is a stochastic puzzle game in which new tiles appear randomly after each valid move. Because of this uncertainty, the solver uses **Expectimax** rather than a standard deterministic search algorithm.

At each turn, the program:

1. Generates all valid player moves.
2. Simulates the possible random placement of `2` and `4` tiles.
3. Evaluates future board states using several heuristics.
4. Selects the move with the highest expected score.

The default search depth is **3**.

---

## Features

* Complete 2048 game implementation
* Automated gameplay using Expectimax
* Random tile generation using:

  * 90% probability of spawning a `2`
  * 10% probability of spawning a `4`
* Depth-limited game-tree search
* Minimax implementation with alpha-beta pruning for comparison
* Custom heuristic evaluation functions
* Optional multi-game performance testing
* Terminal-based board visualization

---

## Heuristic Evaluation

The solver evaluates board quality using a weighted combination of the following heuristics:

### Empty Tiles

Rewards board states with more empty cells, preserving flexibility for future moves.

### Adjacency Weighting

Assigns higher values to tiles located near a preferred corner and encourages high-value tiles to remain grouped together.

### Snake Pattern

Encourages tiles to follow a descending snake-shaped arrangement across the board.

The snake-pattern heuristic also considers:

* Empty cells
* Potential tile merges
* Tile positioning
* Penalties for breaking the preferred ordering

---

## Search Algorithms

### Expectimax

Expectimax models the random spawning of new tiles using chance nodes.

* **Max nodes:** Choose the best player move.
* **Chance nodes:** Evaluate every possible empty-cell placement.
* **Tile probabilities:** `2` with 90% probability and `4` with 10% probability.

### Minimax with Alpha-Beta Pruning

The project also includes a Minimax implementation for comparison. Unlike Expectimax, Minimax treats random tile placement as an adversarial action.

The active automated solver uses Expectimax.

---

## Technologies

* Python
* NumPy
* Tabulate

---


## Running Multiple Simulations

The file includes commented functions for running multiple automated games and recording:

* Highest tile reached
* Number of games that reach 2048
* Runtime per game
* Average runtime

To enable the experiment:

1. Uncomment the simulation functions near the bottom of `2048.py`.
2. Uncomment the following line:

```python
run_experiment(10)
```

3. Change `10` to the desired number of simulations.

---

## Configuration

The search depth can be changed inside the `play_ai()` function:

```python
best_move = get_best_move(board, 3)
```

Increasing the depth allows the solver to examine more future states but also increases execution time.

---

## Course Information

ECS 170: Introduction to Artificial Intelligence
University of California, Davis


