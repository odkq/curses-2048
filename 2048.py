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
    font = {'0': [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
            '1': [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
            '2': [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
            '3': [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            '4': [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            '5': [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            '6': [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            '7': [1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
            '8': [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            '9': [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            ' ': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

    def __init__(self, screen):
        self.screen = screen
        self.board = self._blank_board()

    def _blank_board(self):
        ''' Handy allocator used twice '''
        return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def draw_number(self, x, y, char, attr):
        gliph = Board.font[char]
        for dy in range(5):
            for dx in range(4):
                if dx == 0:
                    bit = 0     # Margin
                else:
                    bit = gliph[dy * 3 + (dx - 1)]  # minus the margin
                if bit == 1:
                    pattr = curses.color_pair(self._get_color_pair(0))
                    self.screen.addstr(y + dy, x + dx, ' ', pattr)
                else:
                    self.screen.addstr(y + dy, x + dx, ' ', attr)

    def draw_tile(self, x, y, value):
        attr = curses.color_pair(self._get_color_pair(value))
        chars = str(value).center(4)
        for dx in range(4):
            self.draw_number(x + (dx * 4), y, chars[dx], attr)

    def draw(self):
        score = 0
        for y in range(4):
            for x in range(4):
                value = self.board[y][x]
                score += value
                px = (x * 18) + 1
                py = (y * 6) + 1
                self.draw_tile(px, py, value)
        self.screen.addstr(4, 72, str(score).center(6))

    def check_win(self):
        blanks = []
        max = 0
        # check for win
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 2048:
                    return 'You won! Press q to exit'
        # check for loose (no 0es) while filling an array of blanks
        # to put a 2 in the next turn
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    blanks.append([y, x])
                elif self.board[y][x] >= max:
                    max = self.board[y][x]
        if len(blanks) == 0:
            return 'You loose. press q to exit'
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
        raise Exception('quiting')


def curses_main(stdscr):
    board = Board(stdscr)
    keys = {curses.KEY_UP: Board.move_up, curses.KEY_DOWN: Board.move_down,
            curses.KEY_LEFT: Board.move_left,
            curses.KEY_RIGHT: Board.move_right, 113: Board.exit}

    if curses.has_colors():
        color = [[curses.COLOR_BLACK, curses.COLOR_BLACK],
                 [curses.COLOR_BLACK, curses.COLOR_WHITE],
                 [curses.COLOR_BLACK, curses.COLOR_CYAN],
                 [curses.COLOR_BLACK, curses.COLOR_BLUE],
                 [curses.COLOR_BLACK, curses.COLOR_GREEN],
                 [curses.COLOR_BLACK, curses.COLOR_YELLOW],
                 [curses.COLOR_BLACK, curses.COLOR_MAGENTA],
                 [curses.COLOR_BLACK, curses.COLOR_RED],
                 [curses.COLOR_BLACK, curses.COLOR_RED],
                 [curses.COLOR_BLACK, curses.COLOR_RED],
                 [curses.COLOR_BLACK, curses.COLOR_RED]]
        for i in range(1, 11):
            curses.init_pair(i, color[i][0], color[i][1])

    stdscr.addstr(0, 72, ' ==== ')
    stdscr.addstr(1, 72, ' 2048 ')
    stdscr.addstr(2, 72, ' ==== ')
    stdscr.addstr(3, 72, 'SCORE:')
    stdscr.addstr(4, 72, '      ')
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
    # Draw endgame string
    s = '| ' + s + ' |'
    frame = '+' + ('-' * (len(s) - 2)) + '+'
    stdscr.addstr(11, 40 - (len(s) / 2), frame)
    stdscr.addstr(12, 40 - (len(s) / 2), s)
    stdscr.addstr(13, 40 - (len(s) / 2), frame)
    s = ('curses-2048 <pablo@odkq.com> JS Original: ' +
         'gabrielecirulli.github.io/2048/')
    stdscr.addstr(24, 1, s)
    while(stdscr.getch() != 113):
        pass
    return

curses.wrapper(curses_main)
