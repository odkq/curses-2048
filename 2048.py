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


class ExitException(Exception):
    pass

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
        self.score = 0
        self.board = self._blank_board()

    def _blank_board(self):
        ''' Handy allocator used twice '''
        return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def draw_number(self, x, y, char, attr):
        ''' Draw a number from x,y to the right (4) and down (5)
            using it's bitmap, changing font attributes '''
        gliph = Board.font[char]
        for dy in range(5):
            for dx in range(4):
                if dx == 0:
                    bit = 0     # Margin
                else:
                    bit = gliph[dy * 3 + (dx - 1)]  # minus the margin
                if bit == 1:
                    pattr = self.attribs[self._get_color_pair(0)]
                    self.screen.addstr(y + dy, x + dx, ' ', pattr)
                else:
                    self.screen.addstr(y + dy, x + dx, ' ', attr)

    def draw_tile(self, x, y, value):
        ''' Draw a whole tile by drawing it's four (padded with ' 's)
            characters '''
        attr = self.attribs[self._get_color_pair(value)]
        chars = str(value).center(4)
        for dx in range(4):
            self.draw_number(x + (dx * 4), y, chars[dx], attr)
        # draw the last row
        dx = x + 16
        for dy in range(y, y + 5):
            self.screen.addstr(dy, dx, ' ', attr)
        # draw the black margin (to erase anything drawn by a modal window)
        pattr = self.attribs[self._get_color_pair(0)]
        for dy in range(y -1, y + 5):
            self.screen.addstr(dy, x - 1, ' ', pattr)
        for dx in range(x - 1, x + 17):
            self.screen.addstr(y - 1, dx, ' ', pattr)

    def draw(self):
        ''' Draw all the tiles in the board and print the score '''
        score = 0
        for y in range(4):
            for x in range(4):
                value = self.board[y][x]
                score += value
                px = (x * 18) + 1
                py = (y * 6) + 1
                self.draw_tile(px, py, value)
        self.screen.addstr(4, 73, str(score).center(6))

    def check_win(self, some_movement):
        ''' Check for winning/loosing condition, returning a string to
            show the user in either case. If '' is returned, the game
            continues '''
        blanks = []
        max = 0
        # check for win
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 2048:
                    return 'You won!'
        # check for loose (no 0es) while filling an array of blanks
        # to put a 2 in the next turn
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    blanks.append([y, x])
                elif self.board[y][x] >= max:
                    max = self.board[y][x]
        # Now put a '2' or a '4' with 10% probability
        # randomly in any of the blanks, but only if a movement was reported
        if some_movement:
            choosen = random.randrange(len(blanks))
            y, x = blanks[choosen]
            randvalue = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
            self.board[y][x] = randvalue  # Allow for one 4 in ten
            del blanks[choosen]     # Remove element for next check 
        if len(blanks) == 0:
            # If an addition can be made, then it is not a loose yet
            lost = True
            for y in range(4):
                for x in range(3):
                    if self.board[y][x + 1] == self.board[y][x]:
                        lost = False
            for x in range(4):
                for y in range(3):
                    if self.board[y + 1][x] == self.board[y][x]:
                        lost = False
            if lost:
                return 'You loose!'
        return ''

    def _get_color_pair(self, value):
        ''' Return the allocated color pair for a certain power of 2
            (it's exponent from 0 to 11) '''
        for i in reversed(range(11)):
            if (value >> i) > 0:
                return i
        return 0

    def move_row(self, row):
        ''' Try to move elements from left to right, return true if a
            movement happened '''
        moved = False
        for x in range(3):
            t = self.board[row][x]
            if t == 0:
                continue
            if self.board[row][x + 1] == 0:
                self.board[row][x] = 0
                self.board[row][x + 1] = t
                moved = True
        return moved

    def add_row(self, row):
        ''' Try to add elements right-to-left, return true if an addition
            happened '''
        added = False
        x = 3
        while x > 0:
            if self.board[row][x] == 0:
                x -= 1
                continue
            if self.board[row][x - 1] == self.board[row][x]:
                self.board[row][x] = (self.board[row][x]) * 2
                self.board[row][x - 1] = 0
                added = True
            x -= 1
        return added

    def move_right(self):
        ''' Perform a right movement. The rest of movements end up
            doing this after transposing the board '''
        some_movement = False
        for y in range(4):
            added = False
            moved = True
            while (moved and not added):
                added = self.add_row(y)
                moved = self.move_row(y)
                if added or moved:
                    some_movement = True
            if added:
                moved = self.move_row(y)
        return some_movement

    def horizontal_transpose(self):
        ''' Transpose all rows left->right right->left '''
        for y in range(4):
            t = self.board[y][0]
            e = self.board[y][1]
            self.board[y][0] = self.board[y][3]
            self.board[y][1] = self.board[y][2]
            self.board[y][3] = t
            self.board[y][2] = e

    def vertical_transpose(self):
        ''' Transpose all columns up->down down->up '''
        exit = self._blank_board()
        for y in range(4):
            for x in range(4):
                exit[y][x] = self.board[x][y]
        for y in range(4):
            for x in range(4):
                self.board[x][y] = exit[x][y]

    def move_left(self):
        ''' Transpose horizontally, move and retranspose '''
        self.horizontal_transpose()
        ret = self.move_right()
        self.horizontal_transpose()
        return ret

    def move_up(self):
        ''' Transpose vertically and horizontally, move and retranspose '''
        self.vertical_transpose()
        self.horizontal_transpose()
        ret = self.move_right()
        self.horizontal_transpose()
        self.vertical_transpose()
        return ret

    def move_down(self):
        ''' Transpose vertically, move and retranspose '''
        self.vertical_transpose()
        ret = self.move_right()
        self.vertical_transpose()
        return ret

    def exit(self):
        raise ExitException('quiting')

    def draw_modal(self, text, keys):
        ''' Draw a 'modal window' by means of overlapping everything over '''
        key = None
        lines = text.split('\n')
        maxlength = max([len(x) for x in lines])
        frame = '+' + ('-' * (maxlength + 2)) + '+'
        sx = 40 - ((maxlength + 4) / 2)
        sy = 12 - (len(lines) / 2)
        self.screen.addstr(sy, sx, frame)
        for line in lines:
            sy += 1
            s = '| ' + line.ljust(maxlength) + ' |'
            self.screen.addstr(sy, sx, s)
        self.screen.addstr(sy + 1, sx, frame)
        while True:
            ch = self.screen.getch()
            if len(keys) == 0:  # Any key
                break
            elif ch in keys:
                key = ch
                break
        self.draw()
        return key

def curses_main(stdscr, replay=False):
    ''' Main function called by curses_wrapper once in curses mode '''
    board = Board(stdscr)

    # Bind keys with the Board methods for them
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

    # Setup attributes array with colors if the terminal have them, or
    # just as NORMAL/INVERSE if it has not
    board.attribs = []
    for i in range(11):
        if curses.has_colors():
            attr = curses.color_pair(i)
        else:
            if i == 0:
                attr = curses.A_NORMAL
            else:
                attr = curses.A_REVERSE
        board.attribs.append(attr)

    # Print the text on the right
    stdscr.addstr(0, 73, ' ==== ')
    stdscr.addstr(1, 73, ' 2048 ')
    stdscr.addstr(2, 73, ' ==== ')
    stdscr.addstr(3, 73, 'SCORE:')
    stdscr.addstr(4, 73, '      ')

    board.check_win(True)    # Put the first 2 2/4 in place
    board.check_win(True)
    board.draw()
    s = '''
                 2048

 HOW TO PLAY: Use your arrow keys to move
 the tiles. When two tiles with the same
 number touch, they merge into one!
 
 Press any key to start, press q at any time
 to quit the game

 curses-2048 <pablo@odkq.com>
 Original game: gabrielecirulli.github.io/2048'''
    if not replay:
        board.draw_modal(s, [])
    while True:
        board.draw()
        try:
            some_movement = keys[stdscr.getch()](board)
        except KeyError:
            some_movement = False   # Wrong key, do not add anything in check_
            pass
        except ExitException:
            return
        s = board.check_win(some_movement)
        if len(s) != 0:
            break
    # Redraw board (in case of a win show the 2048)
    board.draw()
    # Draw endgame string
    s += '\n Press q to exit, or n to start a new game'
    key = board.draw_modal(s, [113, 110])
    if key == 110:
        curses_main(stdscr, replay=True)
    return

def main():
    curses.wrapper(curses_main)
    
main()
