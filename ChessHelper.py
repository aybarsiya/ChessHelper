"""
    This is the main class of the whole program. Main loop and instances of classes are initialized and handled here.
"""

from threading import Thread
from time import sleep
import cv2 as cv

from Enums import PieceTypeEnum, PieceColourEnum
from Enums import MS_PER_FRAME
from ScreenHandler import SH
from InputHandler import IH
from MenuHandler import MH
from Chessboard import Chessboard
from playsound import playsound

import ScreenHandler
import os

class ChessHelper:
        """
                This is the main controller object of the whole program.
                It keeps the necessary classes' references, in order to make the necessary actions and calculations.
        """

        CB: Chessboard = None

        def Controller(self):
                """
                        Main loop of the program. Does operations based on the outputs of the InputHandler.
                """
                while IH._keyboard._listening:
                        sleep(MS_PER_FRAME / 1000)

                        if( (not isinstance(self.CB, Chessboard) or (not self.CB.initialized)) and IH._keyboard._initializeChessBoard):

                                result = SH.InitializeChessboard()

                                if(result == None):
                                        raise Exception("There is no chessboard!")

                                self.CB = Chessboard(cv.threshold(result[0], 128, 255, cv.THRESH_BINARY)[1], result[1], result[2], result[3])

                                self.CB.DeterminePieces()
                                IH._keyboard._initializeChessBoard = False
                                Thread(target = ChessHelper._PlaySound, args = ["ready"]).start()

                        if (IH._speech.responseTextAvailable and (isinstance(self.CB, Chessboard) and self.CB.initialized)):
                                resp = IH._speech.GetResponse()
                                Thread(target = self._MakeMove, args = [resp,]).start()
                                pass

        def _MakeMove(self, moveText: str):
                """
                        This method tries to make a move on the chessboard with the speect-to-text result.
                """
                if(len(moveText) != 4):
                        Thread(target = ChessHelper._PlaySound, args = ["invalid",]).start()
                        return


                print("makemovechesshelper")
                moveText = moveText.lower()

                firstMove = True
                letter = True

                move = [""] * 2

                for i in range(len(moveText)):
                        print(moveText[i], ord(moveText[i]))

                for i in range(len(moveText)):
                        if(firstMove):
                                if(letter):
                                        if(ord(moveText[i]) >= 97 and ord(moveText[i]) <= 104):
                                                move[0] += moveText[i]
                                        else:
                                                Thread(target = ChessHelper._PlaySound, args = ["invalid",]).start()
                                                return
                                        letter = not letter
                                        continue
                                else:
                                        if(ord(moveText[i]) >= 49 and ord(moveText[i]) <= 57):
                                                move[0] += moveText[i]
                                        else:
                                                Thread(target = ChessHelper._PlaySound, args = ["invalid",]).start()
                                                return
                                        letter = not letter
                                        firstMove = not firstMove
                                        continue
                        else:
                                if(letter):
                                        if(ord(moveText[i]) >= 97 and ord(moveText[i]) <= 104):
                                                move[1] += moveText[i]
                                        else:
                                                Thread(target = ChessHelper._PlaySound, args = ["invalid",]).start()
                                                return
                                        letter = not letter
                                        continue
                                else:
                                        if(ord(moveText[i]) >= 49 and ord(moveText[i]) <= 57):
                                                move[1] += moveText[i]
                                        else:
                                                Thread(target = ChessHelper._PlaySound, args = ["invalid",]).start()
                                                return
                                        letter = not letter
                                        firstMove = not firstMove
                                        continue


                x1 = ord(move[0][0]) - 97
                y1 = 8 - (ord(move[0][1]) - 49) - 1
                x2 = ord(move[1][0]) - 97
                y2 = 8 - (ord(move[1][1]) - 49) - 1

                print(x1, y1, x2, y2)

                # cv.imshow("", self.CB.img)
                # cv.waitKeyEx(0)
                # sleep(0.5)

                print(self.CB.squares[y1][x1].piece(), self.CB.squares[y2][x2].piece())
                print(self.CB.squares[y1][x1].piece.colour, self.CB.squares[y2][x2].piece.colour)

                if(self.CB.squares[y1][x1].piece.colour != self.CB.squares[y2][x2].piece.colour):
                        pieceEx = int(150 * self.CB.scale / 100)
                        print("%%%%%%%%%%%%%%%%%%%%%%%", self.CB.scale)
                        print(self.CB.pos, (150 * self.CB.scale / 100))
                        pos1 = (int(self.CB.pos[0] + (x1 * pieceEx) + (pieceEx / 2)), int(self.CB.pos[1] + (y1 * pieceEx) + (pieceEx / 2)))
                        pos2 = (int(self.CB.pos[0] + (x2 * pieceEx) + (pieceEx / 2)), int(self.CB.pos[1] + (y2 * pieceEx) + (pieceEx / 2)))
                        IH._mouse.MakeMove(pos1, pos2)
                        sleep(0.5)
                        newImage = cv.threshold(SH._TakeScreenshot(), 128, 255, cv.THRESH_BINARY)[1]
                        newImage = SH._CropImage(newImage, self.CB.pos, self.CB.width)
                        newImage = SH._GetUpscaledImg(newImage, self.CB.scale)
                        # cv.imshow("", newImage)
                        # cv.waitKeyEx(0)

                        if(SH._CompareChange(self.CB.img, newImage)):
                                Thread(target = ChessHelper._PlaySound, args = ["invalid",]).start()
                        else:
                                self.CB.UpdateBoard(newImage)
                                Thread(target = ChessHelper._PlaySound, args = ["mademove",]).start()
                                print("successfully made a move")
                else:
                        Thread(target = ChessHelper._PlaySound, args = ["invalid",]).start()

                pass

        def _PlaySound(name: str):
                """
                        Plays a sound based on the outcome of operations.
                """
                path = os.getcwd() + rf"\{name}.mp3"

                try:
                        if (name == "ready"):
                                playsound(path, True)
                        elif (name == "invalid"):
                                playsound(path, True)
                        elif (name == "mademove"):
                                playsound(path, True)
                except:
                        pass


"""
        We run the ChessHelper program here.
"""
CH = ChessHelper()

Thread(target = CH.Controller).start()




# CB.img = cv.bilateralFilter(CB.img, 3, 500, 500)
# cv.imshow("b", CB.img)
# cv.waitKeyEx(0)

# for i in range(8):
#         for k in range(8):
#                 cv.imshow("", CB.squares[i][k].img)
# cv.waitKey(0)



# Thread(target = CH.Controller).start()