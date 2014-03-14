#!/usr/bin/env python
import curses

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

def curses_main(stdscr):
    board = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for y in range(7):
        if y % 2:
            stdscr.addstr(y, 0, "|      |      |      |")
        else:
            stdscr.addstr(y, 0, "+------+------+------+")
    while True:
        draw_board(stdscr, board)
        stdscr.getch()

curses.wrapper(curses_main)
