# Minesweeper

A Python implementation of the classic Minesweeper game. The project consists of a game module that handles all the logic and a PySide6 GUI frontend to play the game.

## Setup

This project uses `uv` for dependency management. Make sure you have `uv` installed, then from the project root:
```
uv sync
```

## How to Play
```
uv run python -m frontend.app
```

Left click to reveal a cell. Right click to flag or unflag a cell. The goal is to reveal all safe cells without hitting a mine.

- Blank — hidden cell
- F — flagged cell
- ' * ' — mine (game over!)
- 0-8 — number of adjacent mines

## Running Tests
```
uv run pytest
```

## Project Structure

- `minesweeper/` — game module containing the core logic and enums
- `frontend/` — PySide6 GUI frontend
- `tests/` — test suite for the game module

## Assumptions

- Grid size is fixed at 8x8
- There are always 10 mines
- Flagging is a toggle — flag a flagged cell to unflag it
- A flagged cell must be unflagged before it can be revealed
- Flagging is for the player's reference only and does not affect win/lose conditions
- First click is not guaranteed to be safe
- Numbers represent count of mines in all 8 adjacent cells including diagonals
- Recursive clearing of empty cells is not implemented as per the task specification
- The game module has no dependency on any frontend and can be used with any GUI framework