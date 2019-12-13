#!/usr/bin/python3 -u
import sys
import time
from intcode import intcode
from terminal import *

gridchars = [' ', 'X', '#', '-', 'O']

class Cabinet:
    def __init__(self):
        self.grid_objects = dict()
        self.score = 0
        self.ball_x = 0
        self.ball_y = 0
        self.paddle_x = 0
        self.paddle_y = 0

    def get_infunc_keyboard(self):
        direction = 0
        def infunc():
            nonlocal direction
            if keypressed():
                key = getkey()
                if key == 'a':
                    direction = -1
                elif key == 's':
                    direction = 0
                elif key == 'd':
                    direction = 1
            return direction
        return infunc

    def get_infunc_robot(self):
        def infunc():
            if self.paddle_x > self.ball_x:
                return -1
            elif self.paddle_x < self.ball_x:
                return 1
            else:
                return 0
        return infunc

    def get_outfunc(self, output=False):
        state = 0
        x_pos = 0
        y_pos = 0
        def outfunc(value):
            nonlocal state, x_pos, y_pos
            if state == 0:
                x_pos = value
                state = 1
            elif state == 1:
                y_pos = value
                state = 2
            elif state == 2:
                if x_pos == -1 and y_pos == 0:
                    self.score = value
                    if output:
                        gotoxy(60, 0)
                        print("Score:", self.score, end="")
                else:
                    self.grid_objects[(x_pos, y_pos)] = value
                    if output:
                        gotoxy(x_pos, y_pos)
                        print(gridchars[value], end="")
                        gotoxy(0, 0)
                    if value == 4:
                        self.ball_x = x_pos
                        self.ball_y = y_pos
                        if output:
                            time.sleep(0.01)
                    elif value == 3:
                        self.paddle_x = x_pos
                        self.paddle_y = y_pos
                state = 0
        return outfunc

    def print_map(self):

        goto_top_of_screen()

        print("Score:", self.score)

        max_x = max_y = 0
        for pos in self.grid_objects:
            if pos[0] > max_x:
                max_x = pos[0]
            if pos[1] > max_y:
                max_y = pos[1]
        
        for y in range(0, max_y+1):
            for x in range(0, max_x+1):
                if (x,y) in self.grid_objects:
                    value = self.grid_objects[(x,y)]
                else:
                    value = 0
                print(gridchars[value], end="")
            print()


if __name__ == '__main__':

    show_game = False
    play_game = False

    with open("inputs/input13.txt", "r") as file:
        content = [line.rstrip() for line in file]
    ic_prog = intcode([int(c) for c in content[0].split(',')])
    
    cabinet = Cabinet()
    ic_prog.run(outfunc=cabinet.get_outfunc(output=False),
            copy=True)
    num_blocks = 0
    for v in cabinet.grid_objects.values():
        if v == 2:
            num_blocks += 1
    print("Part 1:", num_blocks)
    if show_game:
        print("Press Enter...")
        input()

    cabinet = Cabinet()
    if show_game:
        setup_terminal()
        clear_screen()
    ic_prog[0] = 2
    if show_game and play_game:
        infunc = cabinet.get_infunc_keyboard()
    else:
        infunc = cabinet.get_infunc_robot()
    ic_prog.run(infunc=infunc, outfunc=cabinet.get_outfunc(output=show_game),
            copy=True)
    if show_game:
        gotoxy(0, 25) 
        restore_terminal()

    print("Part 2:", cabinet.score)
