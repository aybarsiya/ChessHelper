"""
    This is the main class of the whole program. Main loops are initialized and handled here.
"""

from threading import Thread
from time import sleep
import cv2 as cv

from ScreenHandler import SH
from InputHandler import IH
from MenuHandler import MH
from Chessboard import Chessboard

class ChessHelper:
        """
                This is the main controller object of the whole program.
                It keeps the necessary classes' references, in order to make the necessary actions and calculations.
        """

        def Test(self):

                result = SH.InitializeChessboard(f"screenshot1.png")

                if(result == None):
                        raise Exception("There is no chessboard!")

                CB = Chessboard(result[0], result[1], result[2], result[3])

                cv.imshow("", CB.img)

                CB.DeterminePieces()

                IH.Start()

                pass


"""
        We run the ChessHelper program here.
"""
CH = ChessHelper()
CH.Test()




# CB.img = cv.bilateralFilter(CB.img, 3, 500, 500)
# cv.imshow("b", CB.img)
# cv.waitKeyEx(0)

# for i in range(8):
#         for k in range(8):
#                 cv.imshow("", CB.squares[i][k].img)
# cv.waitKey(0)



# Thread(target = CH.Controller).start()