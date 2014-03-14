#!/usr/bin/env python
import curses
import sys

def draw_board(stdscr, board):
    for i, x, y in map((lambda i: [i, i % 3, i / 3]), range(9)):
        value = str(board[i]).center(6)
        px = (x * 6) + x + 1
        py = (y * 2) + 1
        stdscr.addstr(py, px, value)

def move_right(board):
    pass

def move_left(board):
    pass

def move_up(board):
    pass

def move_down(board):
    pass

def exit(board):
    sys.exit(0)

def curses_main(stdscr):
    board = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]
    keys = { curses.KEY_UP: move_up,
             curses.KEY_DOWN: move_down,
             curses.KEY_LEFT: move_left,
             curses.KEY_RIGHT: move_right,
             113: exit }
    for y in range(7):
        if y % 2:
            stdscr.addstr(y, 0, "|      |      |      |")
        else:
            stdscr.addstr(y, 0, "+------+------+------+")
        stdscr.addstr(9, 0, "Use cursor keys to move, q to exit")

    while True:
        draw_board(stdscr, board)
        try:
            keys[stdscr.getch()](board)
        except KeyError:
            pass

curses.wrapper(curses_main)
