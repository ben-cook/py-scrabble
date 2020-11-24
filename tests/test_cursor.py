import curses
import pytest

from scrabble import Board


@pytest.fixture
def new_board():
    # create a new board to use in other tests
    stdscr = curses.initscr()
    BOARD_WIDTH = 15
    BOARD_HEIGHT = 15
    board = Board.Board(BOARD_WIDTH, BOARD_HEIGHT, stdscr)
    return board


def test_initial_board_cursor_position(new_board):
    # test that the board starts with the cursor at the correct position
    assert new_board.board_x == 7
    assert new_board.board_y == 6


def test_cursor_out_of_bounds_top(new_board):
    # test that the board will not let the cursor go out of bounds at the top
    new_board.board_y = 0
    new_board.pressedUp()
    assert new_board.board_y == 0


def test_cursor_out_of_bounds_bottom(new_board):
    # test that the board will not let the cursor go out of bounds at the bottom
    new_board.board_y = new_board.height
    new_board.pressedDown()
    assert new_board.board_y == new_board.height


def test_cursor_out_of_bounds_left(new_board):
    # test that the board will not let the cursor go out of bounds on the left
    new_board.board_x = 0
    new_board.pressedLeft()
    assert new_board.board_x == 0


def test_cursor_out_of_bounds_right(new_board):
    # test that the board will not let the cursor go out of bounds on the right
    new_board.board_x = new_board.width
    new_board.pressedRight()
    assert new_board.board_x == new_board.width
