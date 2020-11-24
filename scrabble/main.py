from Board import Board

import curses
from curses import ascii
import string
import random
import math

BOARD_WIDTH = 15
BOARD_HEIGHT = 15
NUM_PLAYERS = 2
BAG_SIZE = 100
RACK_SIZE = 10


def refillRack(rack, bag):
    while len(rack) < RACK_SIZE:
        rack.append(bag.pop(random.randrange(len(bag))))
        if len(bag) == 0:
            print("Bag has run out of letters.")
    return sorted(rack), bag


def main():
    # curses initialisation
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # init bag and racks
    letters = string.ascii_lowercase * (math.ceil(BAG_SIZE / len(string.ascii_lowercase)))
    bag = list(letters[:BAG_SIZE])
    racks = [sorted([bag.pop(random.randrange(len(bag))) for _ in range(RACK_SIZE)]) for _ in range(NUM_PLAYERS)]
    scores = [0, 0]
    board = Board(BOARD_WIDTH, BOARD_HEIGHT, stdscr)
    current_player = 1

    # bottom text
    stdscr.addstr(BOARD_HEIGHT + 4, 0, "Player {}'s turn: {}".format(current_player, ' '.join(racks[current_player - 1])))
    stdscr.addstr(BOARD_HEIGHT + 6, 0, "Scores:")
    stdscr.addstr(BOARD_HEIGHT + 7, 0, "Player 1: {}".format(scores[0]))
    stdscr.addstr(BOARD_HEIGHT + 8, 0, "Player 2: {}".format(scores[1]))

    gameEnded = False
    while not gameEnded:
        turnHasEnded = False
        while not turnHasEnded:
            letters_used_this_turn = []
            char = board.getChar()
            if char == curses.ascii.ESC:
                gameEnded = True
                break
            elif char == curses.KEY_UP:
                board.pressedUp()
            elif char == curses.KEY_DOWN:
                board.pressedDown()
            elif char == curses.KEY_LEFT:
                board.pressedLeft()
            elif char == curses.KEY_RIGHT:
                board.pressedRight()

            elif curses.ascii.islower(char):
                if char in map(lambda x: ord(x), racks[current_player - 1]):
                    if board.canPlaceTile():
                        if board.hasTempTile():
                            charToAdd = board.getTempTile()
                            racks[current_player - 1].append(charToAdd)
                            racks[current_player - 1] = sorted(racks[current_player - 1])
                        board.putChar(char)
                        letters_used_this_turn.append(chr(char))
                        racks[current_player - 1].remove(chr(char))

            elif char == curses.ascii.SP:
                if board.hasTempTile():
                    print('replacing')
                    charToAdd = board.getTempTile()
                    racks[current_player - 1].append(charToAdd)
                    racks[current_player - 1] = sorted(racks[current_player - 1])
                board.putChar(ord('_'))

            elif char == curses.KEY_ENTER or char == 10 or char == 13:
                validTurn, player_score = board.turnEnded()

                if validTurn:
                    letters_used_this_turn = []
                    scores[current_player - 1] += player_score
                    racks[current_player - 1], bag = refillRack(racks[current_player - 1], bag)
                    if current_player == 1:
                        stdscr.addstr(BOARD_HEIGHT + 7, 0, "Player 1: {}  (+{})".format(scores[0], player_score))
                    else:
                        stdscr.addstr(BOARD_HEIGHT + 8, 0, "Player 2: {}  (+{})".format(scores[1], player_score))
                    current_player = current_player % NUM_PLAYERS + 1
                    stdscr.addstr(BOARD_HEIGHT + 4, 0, "Player {}'s turn: {}".format(current_player, ' '.join(racks[current_player - 1])))
                else:
                    for letter in letters_used_this_turn:
                        racks[current_player - 1].append(letter)
                    letters_used_this_turn = []
                    board.displayHelpText()
            elif char == curses.KEY_BACKSPACE:
                gameEnded = True

    # leave curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    # pass


if __name__ == '__main__':
    main()
