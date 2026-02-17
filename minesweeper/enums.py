from enum import Enum

class GameState(Enum):
    """Represents the possible states of a Minesweeper game."""
    PLAYING = 1
    GAME_OVER = 2
    WON = 3


class CellVisibility(Enum):
    """Represents the visibility state of a cell from the player's perspective."""
    HIDDEN = 1
    REVEALED = 2
    FLAGGED = 3