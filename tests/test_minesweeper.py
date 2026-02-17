from minesweeper.game import Minesweeper
from minesweeper.enums import GameState, CellVisibility
import pytest

PRESET_MINES = [(0,0),(1,3),(5,6),(6,6),(4,2),(7,1),(0,7),(2,3),(7,0),(2,6)]

@pytest.fixture
def preset_game():
    game = Minesweeper(preset_mines=PRESET_MINES)
    return game


#  Initial State Tests

def test_grid_rows(preset_game):
    assert preset_game.rows == 8

def test_grid_cols(preset_game):
    assert preset_game.cols == 8

def test_initial_game_state(preset_game):
    assert preset_game.get_game_state() == GameState.PLAYING

def test_mine_count(preset_game):
    assert preset_game.get_mines_count() == 10

def test_safe_cell_counter(preset_game):
    assert preset_game.counter_safe_cells == 54

def test_all_cells_hidden(preset_game):
    for row in range(preset_game.rows):
        for col in range(preset_game.cols):
            assert preset_game.get_cell_state(row, col) == "H"


#  Mine Placement Tests

def test_mine_placed_correctly(preset_game):
    assert preset_game.content_grid[0][0] == Minesweeper.MINE

def test_safe_cell_not_mine(preset_game):
    assert preset_game.content_grid[0][1] != Minesweeper.MINE

def test_correct_number_of_mines(preset_game):
    mine_count = 0
    for row in preset_game.content_grid:
        for cell in row:
            if cell == Minesweeper.MINE:
                mine_count += 1
    assert mine_count == 10


#  Neighbour Count Tests

def test_neighbour_count_corner(preset_game):
    # Cell (0,1) is next to mine at (0,0)
    assert preset_game.content_grid[0][1] == 1

def test_neighbour_count_multiple(preset_game):
    # Cell (1,2) is next to mines at (1,3) and (2,3)
    assert preset_game.content_grid[1][2] == 2


#  Reveal Tests

def test_reveal_safe_cell(preset_game):
    preset_game.reveal(0, 1)
    assert preset_game.get_cell_state(0, 1) == 1

def test_reveal_mine_game_over(preset_game):
    preset_game.reveal(0, 0)
    assert preset_game.get_game_state() == GameState.GAME_OVER

def test_reveal_out_of_bounds(preset_game):
    with pytest.raises(ValueError):
        preset_game.reveal(0, 10)

def test_reveal_already_revealed(preset_game):
    preset_game.reveal(0, 1)
    with pytest.raises(ValueError):
        preset_game.reveal(0, 1)

def test_reveal_after_game_over(preset_game):
    preset_game.reveal(0, 0)
    with pytest.raises(RuntimeError):
        preset_game.reveal(0, 1)


#  Flag Tests

def test_flag_cell(preset_game):
    preset_game.flag(0, 1)
    assert preset_game.get_cell_state(0, 1) == "F"

def test_unflag_cell(preset_game):
    preset_game.flag(0, 1)
    preset_game.flag(0, 1)
    assert preset_game.get_cell_state(0, 1) == "H"

def test_flag_revealed_cell(preset_game):
    preset_game.reveal(0, 1)
    with pytest.raises(ValueError):
        preset_game.flag(0, 1)

def test_flag_out_of_bounds(preset_game):
    with pytest.raises(ValueError):
        preset_game.flag(0, 10)

def test_reveal_flagged_cell(preset_game):
    preset_game.flag(0, 1)
    with pytest.raises(ValueError):
        preset_game.reveal(0, 1)


#  Win Condition Test

def test_win_condition(preset_game):
    for row in range(preset_game.rows):
        for col in range(preset_game.cols):
            if (row, col) not in PRESET_MINES:
                preset_game.reveal(row, col)
    assert preset_game.get_game_state() == GameState.WON