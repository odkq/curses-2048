#!/usr/bin/env python
import curses
import sys
import random

def draw_board(stdscr, board):
    for y in range(3):
        for x in range(3):
            value = str(board[y][x]).center(6)
            px = (x * 6) + x + 1
            py = (y * 2) + 1
            stdscr.addstr(py, px, value)

def shift_right(board):
    blanks = []
    while shift_righty(board):
        # check for win
        for y in range(3):
            for x in range(2):
                if board[y][x] == 2048:
                    raise Exception('You won mothaf**r')
        # check for loose (no 0es) while filling an array of blanks
        # to put a 2 in the next turn
        loose = True
        for y in range(3):
            for x in range(2):
                if board[y][x] == 0:
                    blanks.append([y, x])
        if len(blanks) == 0:
            raise Exception('You fruiting loosa')
        # Now put a '2' randomly in any of the blanks
        y, x = blanks[random.randrange(len(blanks))]
        board[y][x] = 2

def shift_righty(board):
    for y in range(3):
        for x in range(2):
            t = board[y][x]
            if t != 0:
                if board[y][x + 1] == 0:
                    board[y][x] = 0
                    board[y][x + 1] = t
                    return True
                elif board[y][x + 1] == board[y][x]:
                    board[y][x + 1] = board[y][x] * 2
                    board[y][x] = 0
    return False

def move_right(board):
    shift_right(board)
    return board

def horizontal_transpose(board):
    # transpose all elements
    for y in range(3):
        t = board[y][0]
        board[y][0] = board[y][2]
        board[y][2] = t

def vertical_transpose(board):
    exit = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for y in range(3):
        for x in range(3):
            exit[y][x] = board[x][y]
    for y in range(3):
        for x in range(3):
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
    board = [[4, 0, 0],
             [1, 2, 0],
             [0, 2, 2]]
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
