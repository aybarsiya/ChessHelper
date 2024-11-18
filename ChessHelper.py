"""
    This is the main class of the whole program. Main loops are initialized and handled here.
"""

from threading import Thread
from time import sleep
import cv2 as cv

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

result = CH.SH.InitializeChessboard(f"screenshot1.png")
cv.imshow("", result[4])
cv.waitKeyEx(0)

from Chessboard import Chessboard

cb = Chessboard()
cb.SetImg(result[4])

for i in range(8):
        for k in range(8):
                cv.imshow("", cb.squares[i][k].img)
cv.waitKey(0)

# Thread(target = CH.Controller).start()