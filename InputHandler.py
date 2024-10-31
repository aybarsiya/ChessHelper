"""
        InputHandler Module

        This module is responsible for real time keyboard and mouse I/O.

        Aybars Ay
        2024
"""

import asyncio
from pynput import keyboard

class _InputHandler():

        running = False

        def __init__(self):

                asyncio.run(self._Controller())
                pass

        async def _Controller(self):

                self.running = True
                listener = keyboard.Listener(on_press=self._KeyboardPress, on_release=self._KeyboardRelease)
                listener.start()

                while(self.running):
                        await asyncio.sleep(0.16)


                pass

        #@staticmethod
        def _KeyboardPress(self, key: keyboard.KeyCode):

                print(key)

        #@staticmethod
        def _KeyboardRelease(self, key: keyboard.KeyCode):
                print('{0} released'.format(key))
                if key == keyboard.Key.esc:
                        # Stop listener
                        self.running = False
                        return False


        pass

IH = _InputHandler()

# https://pypi.org/project/pynput/
# https://raspberrypi.stackexchange.com/questions/55431/read-keyboad-input-from-background-process
# https://docs.python.org/3/library/threading.html
# https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing