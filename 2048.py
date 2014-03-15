#!/usr/bin/env python
"""
 2048.py - Minimal implementation of 2048 game with python/ncurses
           See http://gabrielecirulli.github.io/2048/ for the original
           game in js

 Copyright (C) 2014 Pablo Martin <pablo@odkq.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import curses
import random


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.board = self._blank_board()

    def _blank_board(self):
        ''' Handy allocator used twice '''
        return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def draw(self):
        score = 0
        for y in range(4):
            for x in range(4):
                value = self.board[y][x]
                score += value
                if self.board[y][x] == 0:
                    svalue = ' '.center(6)
                else:
                    svalue = str(self.board[y][x]).center(6)
                px = (x * 6) + x + 1
                py = (y * 2) + 1
                if curses.has_colors():
                    attr = curses.color_pair(self._get_color_pair(value))
                    self.screen.addstr(py, px, svalue, attr)
                else:
                    self.screen.addstr(py, px, svalue)
        self.screen.addstr(12, 8, str(score).center(6))

    def check_win(self):
        blanks = []
        max = 0
        # check for win
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 2048:
                    return 'You won! Press q to exit                '
        # check for loose (no 0es) while filling an array of blanks
        # to put a 2 in the next turn
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    blanks.append([y, x])
                elif self.board[y][x] >= max:
                    max = self.board[y][x]
        if len(blanks) == 0:
            return 'You loose. press q to exit                      '
        # Now put a '2' randomly in any of the blanks
        y, x = blanks[random.randrange(len(blanks))]
        self.board[y][x] = 2
        return ''

    def _get_color_pair(self, value):
        for i in reversed(range(11)):
            if (value >> i) > 0:
                return i
        return 0

    def shift_right(self):
        for y in range(4):
            x = 0
            while x < 3:
                t = self.board[y][x]
                if t != 0:
                    if self.board[y][x + 1] == self.board[y][x]:
                        self.board[y][x + 1] = self.board[y][x] * 2
                        self.board[y][x] = 0
                        # Shift right and add
                        x += 1
                    elif self.board[y][x + 1] == 0:
                        self.board[y][x] = 0
                        self.board[y][x + 1] = t
                        # Shift right
                x += 1

    def horizontal_transpose(self):
        # transpose all elements
        for y in range(4):
            t = self.board[y][0]
            e = self.board[y][1]
            self.board[y][0] = self.board[y][3]
            self.board[y][1] = self.board[y][2]
            self.board[y][3] = t
            self.board[y][2] = e

    def vertical_transpose(self):
        exit = self._blank_board()
        for y in range(4):
            for x in range(4):
                exit[y][x] = self.board[x][y]
        for y in range(4):
            for x in range(4):
                self.board[x][y] = exit[x][y]

    def move_right(self):
        self.shift_right()

    def move_left(self):
        self.horizontal_transpose()
        self.shift_right()
        self.horizontal_transpose()

    def move_up(self):
        self.vertical_transpose()
        self.horizontal_transpose()
        self.shift_right()
        self.horizontal_transpose()
        self.vertical_transpose()

    def move_down(self):
        self.vertical_transpose()
        self.shift_right()
        self.vertical_transpose()

    def exit(self):
        raise Exception('quitting')


def curses_main(stdscr):
    board = Board(stdscr)
    keys = {curses.KEY_UP: Board.move_up, curses.KEY_DOWN: Board.move_down,
            curses.KEY_LEFT: Board.move_left,
            curses.KEY_RIGHT: Board.move_right, 113: Board.exit}

    if curses.has_colors():
        color = [curses.COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_CYAN,
                 curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_YELLOW,
                 curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_RED,
                 curses.COLOR_RED, curses.COLOR_RED]
        for i in range(1, 11):
            curses.init_pair(i, color[i], curses.COLOR_BLACK)

    for y in range(9):
        if y % 2:
            stdscr.addstr(y, 0, "|      |      |      |      |")
        else:
            stdscr.addstr(y, 0, "+------+------+------+------+")
    stdscr.addstr(10, 0, "Join the numbers and get to the 2048 tile!")
    stdscr.addstr(12, 0, "Score: ")
    stdscr.addstr(14, 0, "Use cursor keys to move, q to exit")

    s = board.check_win()    # Put the first 2 in place
    while True:
        board.draw()
        try:
            keys[stdscr.getch()](board)
        except KeyError:
            pass
        except Exception:
            return
        s = board.check_win()
        if len(s) != 0:
            break

        stdscr.addstr(14, 0, s)
        while(stdscr.getch() != 113):
            pass
        return

curses.wrapper(curses_main)
