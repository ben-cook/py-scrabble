import curses
import pytest
import os

from scrabble import Board


@pytest.fixture
def new_board():
    # create a new board to use in other tests
    stdscr = curses.initscr()
    BOARD_WIDTH = 15
    BOARD_HEIGHT = 15
    board = Board.Board(BOARD_WIDTH, BOARD_HEIGHT, stdscr)
    return board


@pytest.fixture
def new_board_with_cat(new_board):
    # create a new board with the word "cat"
    new_board.putChar(ord('c'))
    new_board.pressedRight()
    new_board.putChar(ord('a'))
    new_board.pressedRight()
    new_board.putChar(ord('t'))
    return new_board


def test_cat(new_board_with_cat):
    # test that playing the word "cat" gives 3 points as described in project spec
    valid, score = new_board_with_cat.turnEnded()
    assert valid == True
    assert score == 3


def test_cater(new_board_with_cat):
    # test that adding "er" to "cat" to make "cater" gives 5 points
    new_board_with_cat.pressedRight()
    new_board_with_cat.putChar(ord('e'))
    new_board_with_cat.pressedRight()
    new_board_with_cat.putChar(ord('r'))
    valid, score = new_board_with_cat.turnEnded()
    assert valid == True
    assert score == 5
