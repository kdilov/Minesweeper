from enums import GameState, CellVisibility
import random

class Minesweeper:
    """A module that manages the state of a Minesweeper game.

    Provides methods for revealing cells, flagging cells, and
    querying the game state. Designed to be used with any frontend.
    """
    neighbour_cells_coordinates = [(-1, 0), (+1, 0), (0, -1), (0, +1), (-1, -1), (-1, +1), (+1, -1), (+1, +1)]
    MINE = -1
    def __init__(self, preset_mines: list | None = None):
        """Initialize a new Minesweeper game.

        Args:
            preset_mines: Optional list of (row, col) tuples for mine positions.
                          If None, mines are placed randomly.
        """
        self.rows = 8
        self.cols = 8
        self.number_mines = 10
        self.content_grid = [
            [0 for i in range(self.cols)] for j in range(self.rows)
        ]
        self.visibility_grid = [
            [CellVisibility.HIDDEN for i in range(self.cols)] for j in range(self.rows)
        ]
        self.game_state = GameState.PLAYING
        self.counter_safe_cells = (self.rows * self.cols) - self.number_mines
        self.preset_mines = preset_mines
        self._place_mines()
        self._calculate_neighbour_mines()

    def get_game_state(self)-> GameState:
        """Get the current state of the game.

        Returns:
            GameState: Current game state (PLAYING, GAME_OVER, or WON)
        """
        return self.game_state

    def get_mines_count(self) -> int:
        """Get the total number of mines on the board.

        Returns:
            int: Number of mines
        """
        return self.number_mines


    def _place_mines(self) -> None:
        """Place mines on the content grid.

        Uses preset positions if provided, otherwise places mines randomly.
        """
        if self.preset_mines is None:
            all_coordinates = [(r,c) for r in range(self.rows) for c in range(self.cols)]
            random_mines = random.sample(all_coordinates,self.number_mines)
            for r,c in random_mines:
                self.content_grid[r][c] = self.MINE
        else:
            for r,c in self.preset_mines:
                self.content_grid[r][c] = self.MINE


    def _check_bounds(self, row: int, col: int) -> bool:
        """Method that checks if move is out of bounds.

            Args:
                row (int): Row index of the cell
                col (int): Column index of the cell

            Returns:
                 bool: True if coordinates are in bounds , False otherwise

            """
        if (row >= 0 and row < self.rows) and (col >= 0 and col < self.cols):
                return True
        else:
                return False

    def _check_for_mine(self,row: int, col: int) -> bool:
        """Check if a cell contains a mine.

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Returns:
            bool: True if the cell contains a mine, False otherwise
        """
        if self.content_grid[row][col] == self.MINE:
            return True
        else:
            return False


    def _count_neighbouring_mines(self,row: int,col: int) -> int:
        """Count the number of mines neighbouring to a cell.

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Returns:
            int: Number of adjacent mines (0-8)
        """
        counter = 0
        for dr, dc in self.neighbour_cells_coordinates:
            neighbour_row = row + dr
            neighbour_col = col + dc
            if self._check_bounds(neighbour_row, neighbour_col):
                if self.content_grid[neighbour_row][neighbour_col] == self.MINE:
                    counter += 1
        return counter

    def _calculate_neighbour_mines(self) -> None:
        """Calculate and store mine counts for all non-mine cells on the grid."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.content_grid[row][col] != self.MINE:
                    self.content_grid[row][col] = self._count_neighbouring_mines(row, col)


    def reveal(self, row: int, col: int) -> None:
        """Reveal a cell on the board.

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Raises:
            RuntimeError: If the game is already over
            ValueError: If the cell is out of bounds, already revealed, or flagged
        """
        if self.game_state != GameState.PLAYING:
            raise RuntimeError("Game is over")

        if not self._check_bounds(row, col):
            raise ValueError("Move is out of bounds")

        if self.visibility_grid[row][col] == CellVisibility.REVEALED:
            raise ValueError("Cell is already revealed")

        if self.visibility_grid[row][col] == CellVisibility.FLAGGED:
            raise ValueError("Cell is flagged, unflag first")

        self.visibility_grid[row][col] = CellVisibility.REVEALED

        if self.content_grid[row][col] == self.MINE:
            self.game_state = GameState.GAME_OVER
        else:
            self.counter_safe_cells -= 1
            if self.counter_safe_cells == 0:
                self.game_state = GameState.WON

    def flag(self, row: int, col: int) -> None:
        """Toggle flag on a cell.

        If the cell is hidden, it becomes flagged. If flagged, it becomes hidden.

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Raises:
            RuntimeError: If the game is already over
            ValueError: If the cell is out of bounds or already revealed
        """
        if self.game_state != GameState.PLAYING:
            raise RuntimeError("Game is over")

        if not self._check_bounds(row, col):
            raise ValueError("Move is out of bounds")

        if self.visibility_grid[row][col] == CellVisibility.REVEALED:
            raise ValueError("Cannot flag a revealed cell")

        if self.visibility_grid[row][col] == CellVisibility.FLAGGED:
            self.visibility_grid[row][col] = CellVisibility.HIDDEN
        else:
            self.visibility_grid[row][col] = CellVisibility.FLAGGED

    def get_cell_state(self, row: int, col: int) -> str | int:
        """Get the display state of a cell from the player's perspective.

        Hidden cells return 'H', flagged cells return 'F'.
        Revealed cells return '*' for mines or their adjacent mine count.

        Args:
            row: Row index of the cell
            col: Column index of the cell

        Returns:
            str or int: 'H', 'F', '*', or integer mine count (0-8)

        Raises:
            ValueError: If the cell is out of bounds
        """
        if not self._check_bounds(row, col):
            raise ValueError("Cell out of bounds")

        if self.visibility_grid[row][col] == CellVisibility.HIDDEN:
            return "H"
        elif self.visibility_grid[row][col] == CellVisibility.FLAGGED:
            return "F"
        else:
            if self.content_grid[row][col] == self.MINE:
                return "*"
            else:
                return self.content_grid[row][col]


    def get_board_display(self) -> list:
        """Get the full board state from the player's perspective.

        Returns:
            list: 2D list where each cell contains its display value
        """
        board = []
        for row in range(self.rows):
            row_display = []
            for col in range(self.cols):
                row_display.append(self.get_cell_state(row, col))
            board.append(row_display)
        return board






