"""
        Getch Module

        This module is responsible for real-time input logging and returning.

        Features:
        -

        WIP Features:
        - Getting mouse inputs, especially buttons
        - Applying mouse inputs automatically
                - Moving from A to B style algorithm
                - Click and/or drag optionalities
        - Applying keyboard inputs
                - Possible chessboard finding solution in between system processes
                        - Eliminates preperation from the user to setup the chessboard before running the main module of this program

        Aybars Ay
        2024
"""

import pynput

class _Getch:
        def __init__(self):
                try: self.impl = self._GetchWindows()
                except ImportError: self.impl = self._GetchUnix()
        def __call__(self): return self.impl()
        class _GetchUnix:
                def __call__(self):
                        from sys import stdin; import tty, termios
                        fd = stdin.fileno()
                        old_settings = termios.tcgetattr(fd)
                        try:
                                tty.setraw(stdin.fileno())
                                ch = stdin.read(1)
                        finally:
                                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        return ch
        class _GetchWindows:
                def __call__(self):
                        import msvcrt
                        return msvcrt.getch()
Getch = _Getch()

# https://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
# Getch class is from there (about 22 "years" ago!)

async def Loop():

        keys: list = []
        while(True):

                await asyncio.sleep(0.16)

                key = Getch().decode()

                if(key != ''):

                        if(key == 'q' or key == 'Q'):
                                print(keys)
                                break
                        else:
                                keys.append(key)


#
# https://stackoverflow.com/questions/58774718/asyncio-in-corroutine-runtimeerror-no-running-event-loop