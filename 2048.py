#!/usr/bin/env python
import curses

def curses_main(stdscr):
    for y in range(7):
        if y % 2:
            stdscr.addstr(y, 0, "|      |      |      |")
        else:
            stdscr.addstr(y, 0, "+------+------+------+")
    stdscr.getch()

curses.wrapper(curses_main)

