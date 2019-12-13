import sys
import tty
import termios
import select

def clear_screen():
    print('\x1bc', end="")

def gotoxy(x, y):
    print('\x1b['+str(y+1)+';'+str(x+1)+'H', end="")

old_settings = None
def setup_terminal():
    global old_settings
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

def restore_terminal():
    global old_settings
    if old_settings is not None:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    old_settings = None

def keypressed():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getkey():
    return sys.stdin.read(1)

