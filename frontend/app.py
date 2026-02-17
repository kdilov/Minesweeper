import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from minesweeper.game import Minesweeper
from minesweeper.enums import GameState


class MinesweeperGUI(QWidget):
    """Simple PySide6 frontend for the Minesweeper game module."""

    def __init__(self):
        super().__init__()
        self.game = Minesweeper()
        self.buttons = {}
        self.setWindowTitle("Minesweeper")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the window layout with grid buttons and status label."""
        main_layout = QVBoxLayout()

        self.status_label = QLabel(f"Mines: {self.game.get_mines_count()} | Status: Playing")
        main_layout.addWidget(self.status_label)

        grid_layout = QGridLayout()
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                button = QPushButton(" ")
                button.setFixedSize(40, 40)
                button.clicked.connect(lambda checked, r=row, c=col: self._on_left_click(r, c))
                button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                button.customContextMenuRequested.connect(lambda pos, r=row, c=col: self._on_right_click(r, c))
                grid_layout.addWidget(button, row, col)
                self.buttons[(row, col)] = button

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def _on_left_click(self, row: int, col: int) -> None:
        """Handle left click to reveal a cell.

        Args:
            row: Row index of the clicked cell
            col: Column index of the clicked cell
        """
        if self.game.get_game_state() != GameState.PLAYING:
            return
        try:
            self.game.reveal(row, col)
            self._update_board()
        except (ValueError, RuntimeError) as e:
            self.status_label.setText(str(e))

    def _on_right_click(self, row: int, col: int) -> None:
        """Handle right click to flag/unflag a cell.

        Args:
            row: Row index of the clicked cell
            col: Column index of the clicked cell
        """
        if self.game.get_game_state() != GameState.PLAYING:
            return
        try:
            self.game.flag(row, col)
            self._update_board()
        except (ValueError, RuntimeError) as e:
            self.status_label.setText(str(e))

    def _update_board(self) -> None:
        """Update all button labels and the status label to reflect current game state."""
        board = self.game.get_board_display()
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                cell = board[row][col]
                button = self.buttons[(row, col)]
                if cell == "H":
                    button.setText(" ")
                elif cell == "F":
                    button.setText("F")
                elif cell == "*":
                    button.setText("*")
                else:
                    button.setText(str(cell))

        state = self.game.get_game_state()
        if state == GameState.WON:
            self.status_label.setText("Congratulations! You won!")
        elif state == GameState.GAME_OVER:
            self.status_label.setText("BOOM! You hit a mine. Game over!")
        else:
            self.status_label.setText(f"Mines: {self.game.get_mines_count()} | Status: Playing")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinesweeperGUI()
    window.show()
    sys.exit(app.exec())