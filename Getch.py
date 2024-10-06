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