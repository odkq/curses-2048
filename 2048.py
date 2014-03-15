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
import sys
import random

def draw_board(stdscr, board):
    score = 0
    for y in range(4):
        for x in range(4):
            value = board[y][x]
            score += value
            if board[y][x] == 0:
                svalue = ' '.center(6)
            else:
                svalue = str(board[y][x]).center(6)
            px = (x * 6) + x + 1
            py = (y * 2) + 1
            if curses.has_colors():
                attr = curses.color_pair(get_color_pair(value))
                stdscr.addstr(py, px, svalue, attr)
            else:
                stdscr.addstr(py, px, svalue)
    stdscr.addstr(12, 8, str(score).center(6))

def check_win(board):
    blanks = []
    loose = True
    max = 0
    # check for win
    for y in range(4):
        for x in range(4):
            if board[y][x] == 2048:
                return 'You won! Press q to exit                '
    # check for loose (no 0es) while filling an array of blanks
    # to put a 2 in the next turn
    for y in range(4):
        for x in range(4):
            if board[y][x] == 0:
                blanks.append([y, x])
            elif board[y][x] >= max:
                max = board[y][x]
    if len(blanks) == 0:
        return 'You loose. press q to exit                      '
    # Now put a '2' randomly in any of the blanks
    y, x = blanks[random.randrange(len(blanks))]
    board[y][x] = 2
    return ''

def get_color_pair(value):
    for i in reversed(range(11)):
        if (value >> i) > 0:
            return i
    return 0

def shift_right(board):
    for y in range(4):
        x = 0
        while x < 3:
            t = board[y][x]
            if t != 0:
                if board[y][x + 1] == board[y][x]:
                    board[y][x + 1] = board[y][x] * 2
                    board[y][x] = 0
                    # Shift right and add
                    x += 1
                elif board[y][x + 1] == 0:
                    board[y][x] = 0
                    board[y][x + 1] = t
                    # Shift right
            x += 1
    return False

def move_right(board):
    shift_right(board)
    return board

def horizontal_transpose(board):
    # transpose all elements
    for y in range(4):
        t = board[y][0]
        e = board[y][1]
        board[y][0] = board[y][3]
        board[y][1] = board[y][2]
        board[y][3] = t
        board[y][2] = e

def vertical_transpose(board):
    exit = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for y in range(4):
        for x in range(4):
            exit[y][x] = board[x][y]
    for y in range(4):
        for x in range(4):
            board[x][y] = exit[x][y]

def move_left(board):
    horizontal_transpose(board)
    shift_right(board)
    horizontal_transpose(board)

def move_up(board):
    vertical_transpose(board)
    horizontal_transpose(board)
    shift_right(board)
    horizontal_transpose(board)
    vertical_transpose(board)

def move_down(board):
    vertical_transpose(board)
    shift_right(board)
    vertical_transpose(board)

def exit(board):
    sys.exit(0)

def curses_main(stdscr):
    board = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]
    
    keys = { curses.KEY_UP: move_up,
             curses.KEY_DOWN: move_down,
             curses.KEY_LEFT: move_left,
             curses.KEY_RIGHT: move_right,
             113: exit }

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

    s = check_win(board)    # Put the first 2 in place
    while True:
        draw_board(stdscr, board)
        try:
            keys[stdscr.getch()](board)
        except KeyError:
            pass
        s = check_win(board)
        if len(s) != 0:
            stdscr.addstr(14, 0, s)
            while(stdscr.getch() != 113):
                pass
            return

curses.wrapper(curses_main)
