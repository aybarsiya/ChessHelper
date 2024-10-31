"""
    This is the main class of the whole program. Main loops are initialized and handled here.
"""

import multiprocessing as mp; from multiprocessing import Process
from time import sleep

if __name__ == '__main__':
        mp.freeze_support()

class ChessHelper:
        """
                This is the main controller object of the whole program.
                It keeps the necessary classes' references, in order to make the necessary actions and calculations.
        """
        from InputHandler import IH
        from ScreenHandler import SH

        def Controller(self):

                self.IH.Start()
                Process(target = self.SH.FindChessboardOnScreen()).run()
                print("woah")

                while(self.IH.running):
                        print(self.IH.running)
                        sleep(0.16)
                pass


        def PlayMode(self):
                """
                        This async function handles the operations while playing a chess game.

                """
                from Chessboard import CB

                pass

"""
        We run the ChessHelper program here.
"""
CH = ChessHelper()
Process(target = CH.Controller()).run()