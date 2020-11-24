import curses
import copy
from collections import Counter
import os
import sys


def load_words():
    if "pytest" in sys.modules:
        with open(os.path.join('./scrabble', 'words.txt')) as word_file:
            valid_words = set(word_file.read().split())
    else:
        with open(os.path.join(os.path.dirname(__file__), 'words.txt')) as word_file:
            valid_words = set(word_file.read().split())

    return valid_words


def transpose2DArray(array):
    return [list(i) for i in zip(*array)]


def list_difference(a, b):
    # this implements the set difference a \ b, but does not remove all duplicates
    # as the set difference would.
    remaining = Counter(b)
    out = []

    for val in a:
        if remaining[val]:
            remaining[val] -= 1
        else:
            out.append(val)
    return out


class Board():

    def __init__(self, width, height, stdscr):
        self.width = width
        self.height = height
        self.board = [['_' for _ in range(width)] for _ in range(height)]
        # temp_board keeps track of the new tiles places during a player's turn
        self.temp_board = [['_' for _ in range(width)] for _ in range(height)]
        self.window_x, self.window_y = 15, 8
        self.board_x, self.board_y = 7, 6
        self.win = stdscr
        self.win.addstr(0, 0, self.showBoard())
        self.displayHelpText()
        self.valid_words = load_words()
        self.current_board_score = 0
        self.current_words_on_board = []

    def showBoard(self):
        display = []
        display.append('{:_^31}'.format('Board-Start'))
        display.append('_'.join([' ' for _ in range(self.width + 1)]))

        for row in self.board:
            display.append("|" + "|".join(row) + "|")

        display.append('{:_^31}'.format('Board-End'))
        return '\n'.join(display)

    def turnEnded(self):
        # Assign points to the largest words made; substrings don't count

        validBoardState = True
        newBoardState = [['_' for _ in range(self.width)] for _ in range(self.height)]

        if self.temp_board == newBoardState:
            return False, -1

        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] != '_':
                    newBoardState[j][i] = self.board[j][i]
                if self.temp_board[j][i] != '_':
                    if self.board[j][i] != '_':
                        print("Board and Temp Board overlap! This shouldn't happen.")
                    newBoardState[j][i] = self.temp_board[j][i]

        self.resetTempBoard()

        h_words = list(filter(lambda word: len(word) > 1, self.findHorizontalWords(newBoardState)))
        v_words = list(filter(lambda word: len(word) > 1, self.findVerticalWords(newBoardState)))

        valid_words = list(filter(lambda word: self.validWord(word), h_words + v_words))
        print('\n----')
        print("current words: " + str(self.current_words_on_board))
        print("valid words: " + str(valid_words))

        new_score = sum(map(lambda x: len(x), list_difference(valid_words, self.current_words_on_board)))

        self.current_words_on_board = valid_words
        print('hwords:' + str(h_words))
        for word in h_words:
            if self.validWord(word):
                # print("Found a valid word {}".format(word))
                pass
            else:
                # print("Found a invalid word {}".format(word))
                validBoardState = False

        for word in v_words:
            if self.validWord(word):
                # print("Found a valid word {}".format(word))
                pass

        self.win.addstr(30, 5, "{}".format("Valid Move" if validBoardState else "Invalid"), curses.A_BOLD)
        # self.win.addstr(50, 5, "hi")
        print("board is valid: " + str(validBoardState))

        if validBoardState:
            # Go to the next player's turn
            new_board_score = sum(map(lambda word: len(word), h_words + v_words))
            delta_score = new_board_score - self.current_board_score
            self.current_board_score = new_board_score
            return True, new_score
        else:
            # Clear the placed tiles and have the player try again
            self.temp_board = [['_' for _ in range(self.width)] for _ in range(self.height)]
            self.win.addstr(0, 0, self.showBoard())
            self.displayHelpText()
            return False, -1

    def getHorizontalWord(self, x, y, board):
        if board[y][x] == '_':
            print("Something went wrong.")

        letters = []
        while board[y][x] != '_':
            letters.append(board[y][x])
            x += 1
        return ''.join(letters)

    def getVerticalWord(self, x, y, board):
        if board[y][x] == '_':
            print("Something went wrong.")

        letters = []
        while board[y][x] != '_':
            letters.append(board[y][x])
            y += 1
        return ''.join(letters)

    def findHorizontalWords(self, board):
        words = []

        for j, row in enumerate(board):
            found_word = False
            for i, letter in enumerate(row):
                if not found_word:
                    if letter != '_':
                        words.append(self.getHorizontalWord(i, j, board))
                        found_word = True
                else:
                    if letter == '_':
                        found_word = False

        return words

    def findVerticalWords(self, board):
        words = []

        for i in range(self.width):
            found_word = False
            for j in range(self.height):
                if not found_word:
                    if board[j][i] != '_':
                        words.append(self.getVerticalWord(i, j, board))
                        found_word = True
                else:
                    if board[j][i] == '_':
                        found_word = False

        return words

    def resetTempBoard(self):
        self.temp_board = [['_' for _ in range(self.width)] for _ in range(self.height)]
        self.showBoard()

    def validWord(self, word):
        return word in self.valid_words

    def canPlaceTile(self):
        return self.board[self.board_y][self.board_x] == '_'

    def hasTempTile(self):
        return self.temp_board[self.board_y][self.board_x] != '_'

    def getTempTile(self):
        return self.temp_board[self.board_y][self.board_x]

    def getChar(self):
        return self.win.getch(self.window_y, self.window_x)

    def putChar(self, char):
        self.win.addch(self.window_y, self.window_x, char, curses.A_BOLD)
        self.win.refresh()
        self.temp_board[self.board_y][self.board_x] = chr(char)

    def pressedRight(self):
        if self.window_x < 2 * self.width - 1 and self.board_x < self.width:
            self.window_x += 2
            self.win.refresh()
            self.board_x += 1

    def pressedLeft(self):
        if self.window_x > 1 and self.board_x > 0:
            self.window_x -= 2
            self.win.refresh()
            self.board_x -= 1

    def pressedDown(self):
        if self.window_y < self.height + 1 and self.board_y < self.height:
            self.window_y += 1
            self.win.refresh()
            self.board_y += 1

    def pressedUp(self):
        if self.window_y > 2 and self.board_y > 0:
            self.window_y -= 1
            self.win.refresh()
            self.board_y -= 1

    def displayHelpText(self):
        self.win.addstr(1, self.width + 25, "Leave Program: Escape (ESC)")
        self.win.addstr(2, self.width + 25, "Navigate Board: Arrow Keys")
        self.win.addstr(3, self.width + 25, "Finish Turn: Enter")
        self.win.addstr(4, self.width + 25, "Pass Turn (and end the game): Backspace")
        self.win.addstr(6, self.width + 25, "To place a tile from your rack,")
        self.win.addstr(7, self.width + 25, "just type the letter on your keyboard.")
        self.win.addstr(9, self.width + 25, "To clear a placed tile during your turn,")
        self.win.addstr(10, self.width + 25, "press Spacebar and it will be returned")
        self.win.addstr(11, self.width + 25, "to your tile rack.")
