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
    DARK_FOREGROUND = 12
    LIGHT_FOREGROUND = 13
    FRAME = 14
    BACKGROUND = 15
    
    MIN_X = 80
    MIN_Y = 24
    MIN_ERROR = 'Terminal must be at least %dx%d to play!' % (MIN_X, MIN_Y)
    MIN_ERROR2 = '(Resize terminal or press q to exit)'

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
        self.calculate_tile_dimensions()

    def calculate_tile_dimensions(self):
        ''' Get tile height from the terminal window dimensions '''
        y, x = self.screen.getmaxyx()
        self.tile_width = 17
        if y >= 41:
            self.tile_height = 9
        elif y >= 33:
            self.tile_height = 7
        elif y >= 24:
            self.tile_height = 5

    def minimal_size(self):
        ''' Check terminal height and width are large enough '''
        height, width = self.screen.getmaxyx()
        if width < self.MIN_X or height < self.MIN_Y:
            return False
        return True

    def resize(self):
        ''' Called when terminal window is resized '''
        self.screen.erase()
        self.calculate_tile_dimensions()
        self.print_title()
        self.draw()

    def _blank_board(self):
        ''' Handy allocator used twice '''
        return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def print_title(self):
        if self.check_minimal_size():
            return

        # Print the text on the right
        self.screen.addstr(0, 74, '====  ')
        self.screen.addstr(1, 74, '2048  ')
        self.screen.addstr(2, 74, '====  ')
        self.screen.addstr(3, 74, 'SCORE:')
        self.screen.addstr(4, 74, '      ')

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
                    pattr = self.attribs[self.DARK_FOREGROUND]
                    self.screen.addstr(y + dy, x + dx, ' ', pattr)
                else:
                    self.screen.addstr(y + dy, x + dx, ' ', attr)

    def draw_tile(self, x, y, value):
        ''' Draw a whole tile by drawing it's four (padded with ' 's)
            characters '''
        if value == 0:
            attr = self.attribs[self.BACKGROUND]
            for dy in range(y, y + self.tile_height):
                for dx in range(x, x + self.tile_width):
                    self.screen.addstr(dy, dx, ' ', attr)

            # for dx in range(x - 1, x + 17):
            #    self.screen.addstr(y - 1, dx, ' ', frameattr)
            return

        attr = self.attribs[self._get_color_pair(value)]
        for dy in range(y, y + self.tile_height):
            for dx in range(x, x + self.tile_width):
                self.screen.addstr(dy, dx, ' ', attr)
        chars = str(value).center(4)
        number_y = y + ((self.tile_height - 5)/2)
        for dx in range(4):
            self.draw_number(x + (dx * 4), number_y, chars[dx], attr)
        # draw the last row
        dx = x + self.tile_width - 1
        # draw the margin (to erase anything drawn by a modal window)
        #pattr = self.attribs[self.FRAME]
        #for dy in range(y - 1, y + 5):
        #    self.screen.addstr(dy, x - 1, ' ', pattr)
        #for dx in range(x - 1, x + 17):
        #    self.screen.addstr(y - 1, dx, ' ', pattr)

    def draw_frame(self):
        ''' Draw frame '''
        frameattr = self.attribs[self.FRAME]
        for y in range(5):
            for x in range(5):
                px = (x * (self.tile_width + 1))
                py = (y * (self.tile_height + 1))
                if x < 4:
                    for ppx in range(px, px + self.tile_width + 2):
                        try:
                            self.screen.addstr(py, ppx, ' ', frameattr)
                        except:
                            pass
                if y < 4:
                    for ppy in range(py, py + self.tile_height + 1):
                        try:
                            self.screen.addstr(ppy, px, ' ', frameattr)
                        except:
                            pass
                        # raise Exception('ppy {}'.format(ppy))
#            for ppy in range(py, py + 6):
#                try:
#                    self.screen.addstr(ppy, 57, ' ', frameattr)
#                except:
#                    pass
    def check_minimal_size(self):
        if not self.minimal_size():
            y, x = self.screen.getmaxyx()
            #if x < len(self.MIN_ERROR):
            try:
                self.screen.addstr(y/2, ((x - len(self.MIN_ERROR)) / 2),
                                       self.MIN_ERROR)
                self.screen.addstr(y/2 + 1, ((x - len(self.MIN_ERROR2)) / 2),
                                       self.MIN_ERROR2)
            except curses.error:
                pass
            return True
        return False

    def draw(self):
        ''' Draw all the tiles in the board and print the score '''
        score = 0
        if self.check_minimal_size():
            return

        self.draw_frame()
        for y in range(4):
            for x in range(4):
                value = self.board[y][x]
                score += value
                px = (x * (self.tile_width + 1)) + 1
                py = (y * (self.tile_height + 1)) + 1
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
        if self.check_minimal_size():
            return

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
    curses.curs_set(0)
    curses.use_default_colors()

    # Bind keys with the Board methods for them
    keys = {curses.KEY_UP: Board.move_up, curses.KEY_DOWN: Board.move_down,
            curses.KEY_LEFT: Board.move_left,
            curses.KEY_RIGHT: Board.move_right, 113: Board.exit,
            curses.KEY_RESIZE: Board.resize}

    if curses.has_colors():
        if curses.COLORS != 256:
            # Use standard (16) colors
            color = [[curses.COLOR_BLACK, curses.COLOR_BLACK],    # 0
                     [curses.COLOR_BLACK, curses.COLOR_WHITE],    # 2
                     [curses.COLOR_BLACK, curses.COLOR_CYAN],     # 4
                     [curses.COLOR_BLACK, curses.COLOR_BLUE],     # 8
                     [curses.COLOR_BLACK, curses.COLOR_GREEN],    # 16
                     [curses.COLOR_BLACK, curses.COLOR_YELLOW],   # 32
                     [curses.COLOR_BLACK, curses.COLOR_MAGENTA],  # 64
                     [curses.COLOR_BLACK, curses.COLOR_RED],      # 128
                     [curses.COLOR_BLACK, curses.COLOR_RED],      # 256
                     [curses.COLOR_BLACK, curses.COLOR_RED],      # 512
                     [curses.COLOR_BLACK, curses.COLOR_RED],      # 1024
                     [curses.COLOR_BLACK, curses.COLOR_RED],      # 2048
                     [curses.COLOR_BLACK, curses.COLOR_BLACK],  # dark fg
                     [curses.COLOR_BLACK, curses.COLOR_BLACK],  # light fg
                     [curses.COLOR_BLACK, curses.COLOR_BLACK],  # frame
                     [curses.COLOR_BLACK, curses.COLOR_BLACK]]  # background
        else:
            # Use 256 colors to mimick the original ones in the page
            # for curses.COLORS to be 256 you must use a suitable terminal
            # emulator (xterm and gnome terminal are known to support 256
            # colors) _and_ set your TERM environment variable accordingly
            # export TERM=xterm-256color or TERM=screen-256color if using
            # screen or tmux.
            color = [[0, 240],  # 0
                     [0, 231],  # 2
                     [0, 229],  # 4
                     [0, 215],  # 8
                     [7, 209],  # 16
                     [7, 203],  # 32
                     [7, 196],  # 64
                     [7, 222],  # 128
                     [7, 227],  # 256
                     [7, 226],  # 512
                     [7, 214],  # 1024
                     [7, 9],    # 2048
                     [0, 234],  # dark fg
                     [0, 250],  # light fg
                     [0, 240],  # frame
                     [0, 250]]  # background

        for i in range(1, 16):
            try:
                curses.init_pair(i, color[i][0], color[i][1])
            except:
                raise Exception('i {}'.format(i))

    # Setup attributes array with colors if the terminal have them, or
    # just as NORMAL/INVERSE if it has not
    board.attribs = []
    for i in range(16):
        if curses.has_colors():
            attr = curses.color_pair(i)
        else:
            if i == 0:
                attr = curses.A_NORMAL
            else:
                attr = curses.A_REVERSE
        board.attribs.append(attr)

    board.print_title()

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
