"""
    This is the main class of the whole program. Main loops are initialized and handled here.
"""

from threading import Thread
from time import sleep

class ChessHelper:
        """
                This is the main controller object of the whole program.
                It keeps the necessary classes' references, in order to make the necessary actions and calculations.
        """
        from InputHandler import IH
        from ScreenHandler import SH
        from MenuHandler import MH

        def Controller(self):

                self.IH.Start()
                self.findChessBoardProcess = Thread(target = self.SH.FindChessboardOnScreen)
                self.findChessBoardProcess.start()
                print("woah")

                Thread(target = self.MH.loop).start()

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

print(CH.Controller)

Thread(target = CH.Controller).start()