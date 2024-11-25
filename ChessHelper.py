"""
    This is the main class of the whole program. Main loops are initialized and handled here.
"""

from threading import Thread
from time import sleep
import cv2 as cv

from ScreenHandler import SH

class ChessHelper:
        """
                This is the main controller object of the whole program.
                It keeps the necessary classes' references, in order to make the necessary actions and calculations.
        """
        from InputHandler import IH
        from MenuHandler import MH

        def Controller(self):

                self.IH.Start()
                self.findChessBoardProcess = Thread(target = ScreenHandler.FindChessboardOnScreen)
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

from Chessboard import Chessboard

result = SH.InitializeChessboard(f"screenshot00.png")

if(result == None):
        raise Exception("There is no chessboard!")

CB = Chessboard(result[0], result[1], result[2], result[3])

cv.imshow("", CB.img)

# CB.img = cv.bilateralFilter(CB.img, 3, 500, 500)
# cv.imshow("b", CB.img)
# cv.waitKeyEx(0)

# for i in range(8):
#         for k in range(8):
#                 cv.imshow("", CB.squares[i][k].img)
# cv.waitKey(0)

CB.DeterminePieces()

# Thread(target = CH.Controller).start()