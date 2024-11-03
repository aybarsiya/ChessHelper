"""
        ScreenHandler Module

        This module is responsible for making several operations using image processing libraries.

        Features:
        - Taking screenshots of the main screen
                * Only supports main screen in a multi screen setup
        - Determining if there is a default "chess.com" chessboard on the screen
        - If there is a chessboard on the screen
                - Determine chessboard's scale on pixel values
                - Determine the exact coordinates of the chessboard on the screen using the determined scale
        - If there is no chessboard on the screen
                - Acknowledging the situation using some "magic numbers" (lovely!)
                - Early cancellation of the algorithm

        WIP Features:
        - Returning 64 equal sized images of the found chessboard on the screen
                - Will be used for populating the Chessboard module's 2D "Square"s array


        Aybars Ay
        2024
"""

import cv2 as cv
import numpy as np
from time import time

from PIL import ImageGrab as IG

from Enums import PieceColourEnum, PieceTypeEnum
from ResourceHandler import BoardImg, PieceImgs

class ScreenHandler:
        """
                This class is used for all relevant image processing and data analysis functions.
        """

        # This scale variable is used for determining max initial scale of the chessboard
        # that could be found on a screen.
        # Determined by screen resolution's short side's value and applied the multiplier inside the init function.
        _maxScale: float = 1.0
        def __init__(self):

                scrShape = self._TakeScreenshot().shape[:2]
                lowestWidth = 0

                if(scrShape[0] < scrShape[1]):
                        lowestWidth = scrShape[0]
                else:
                        lowestWidth = scrShape[1]

                tempWidth = BoardImg._self.shape[0]

                self._maxScale = round((float(lowestWidth) / (float(tempWidth / 100.0))) / 100.0, 3)
                print(self._maxScale)

                if(self._maxScale > 1.0):
                        self._maxScale = 1.0

        def InitializeChessboard(self):

                startTime = time()
                screenImg = self._TakeScreenshot()
                screenImg = cv.imread("screenshot3.png", cv.IMREAD_GRAYSCALE)
                scale = self._GetChessboardScale(self._maxScale, screenImg)
                result = ScreenHandler._GetScaledBestValues(scale, screenImg, BoardImg._self, BoardImg._mask)
                print(f"{time() - startTime}s")
                print(result, scale, 1200 * scale)

        @staticmethod
        def _GetChessboardScale(startingScale: float, screenImg: cv.typing.MatLike):
                """
                        This function uses black king chess piece object from the ResourceHandler module to;
                        - Find out if there is a chessboard on the screen
                        - If there is, find out the scale of the chessboard with the piece image

                        There are some optimizations included in the algorithm;
                        - Only grayscale original images are used
                        - Magic numbers to stop the algorithm going to far and possibly crashing the function
                        - Scale steps are used for downscaling (several to increase reliability, ex: 10%, 1%, 0.2%)
                        - Determining going up or down in between scale steps
                """

                def _IsDown(_scale: float, _scaleStep: float, _screenImg: cv.typing.MatLike):
                        """
                                This function determines the next step of scale calculation's direction, up or down.
                        """

                        downResult = ScreenHandler._GetScaledBestValues(
                                                                                        (_scale - _scaleStep),
                                                                                        _screenImg,
                                                                                        PieceImgs[PieceColourEnum.BLACK][PieceTypeEnum.KING]._self,
                                                                                        canny = True
                                                                                        )
                        upResult = ScreenHandler._GetScaledBestValues(
                                                                                        (_scale + _scaleStep),
                                                                                        _screenImg,
                                                                                        PieceImgs[PieceColourEnum.BLACK][PieceTypeEnum.KING]._self,
                                                                                        canny = True
                                                                                        )
                        if(downResult[0] > upResult[0]):
                                return (True, downResult)
                        return (False, upResult)

                print(screenImg.shape)
                print(tuple([int(x * 2) for x in screenImg.shape[:2]])[::-1])
                timez = time()
                screenImg = cv.bilateralFilter(screenImg, 5, 220, 220)
                cv.imwrite(r"C:\Users\aybar\Desktop\schoolstuff\prog\ChessHelper\imgb.png", screenImg)
                print(time() - timez)
                screenImg = cv.resize(screenImg, tuple([int(x / 62 * 100) for x in screenImg.shape[:2]])[::-1], interpolation = cv.INTER_LINEAR_EXACT)
                cv.imwrite(r"C:\Users\aybar\Desktop\schoolstuff\prog\ChessHelper\imgr.png", screenImg)
                timez = time()
                screenImg = cv.Canny(screenImg, 160, 255, apertureSize = 3)
                print(time() - timez)
                cv.imwrite(r"C:\Users\aybar\Desktop\schoolstuff\prog\ChessHelper\imgc.png", screenImg)
                print(screenImg.shape)

                boardImg = cv.bilateralFilter(BoardImg._self, 3, 125, 125)
                cv.imwrite(r"C:\Users\aybar\Desktop\schoolstuff\prog\ChessHelper\boardb.png", boardImg)
                boardImg = cv.Canny(boardImg, 75, 255, apertureSize = 7)
                cv.imwrite(r"C:\Users\aybar\Desktop\schoolstuff\prog\ChessHelper\boardc.png", boardImg)

                kingImg = PieceImgs[PieceColourEnum.WHITE][PieceTypeEnum.KING]._self
                kingImg = cv.bilateralFilter(kingImg, 5, 130, 130)
                cv.imwrite(r"C:\Users\aybar\Desktop\schoolstuff\prog\ChessHelper\kingb.png", kingImg)
                kingImg = cv.Canny(kingImg, 240, 255, apertureSize = 3)
                cv.imwrite(r"C:\Users\aybar\Desktop\schoolstuff\prog\ChessHelper\kingc.png", kingImg)
                kingImg = cv.resize(kingImg, tuple([int(x * 0.62) for x in kingImg.shape[:2]])[::-1], interpolation = cv.INTER_LINEAR_EXACT)
                cv.imwrite(r"C:\Users\aybar\Desktop\schoolstuff\prog\ChessHelper\kingr.png", kingImg)

                bestScale = startingScale
                initialResult = ScreenHandler._GetScaledBestValues(
                                                                                        bestScale,
                                                                                        screenImg,
                                                                                        PieceImgs[PieceColourEnum.BLACK][PieceTypeEnum.KING]._self,
                                                                                        canny = True
                                                                                        )
                bestValue = initialResult[0]

                print(bestValue, bestScale)

                sweeps = (0.100, 0.010, 0.003)
                down = -1.0

                for i in range(len(sweeps)):

                        if(i > 0):
                                _result = _IsDown(bestScale, round(sweeps[i], 3), screenImg)
                                if(_result[0]):
                                        down = -1.0
                                else:
                                        down = 1.0
                                bestScale = round((bestScale + (sweeps[i] * down)), 3)
                                bestValue = _result[1][0]
                                print(bestValue, bestScale)

                        while(True):
                                possibleBestScale = round((bestScale + (sweeps[i] * down)), 3)
                                result = ScreenHandler._GetScaledBestValues(
                                                                                                possibleBestScale,
                                                                                                screenImg,
                                                                                                PieceImgs[PieceColourEnum.BLACK][PieceTypeEnum.KING]._self,
                                                                                                canny = True
                                                                                                )

                                # FIXME
                                # MAGIC NUMBERS
                                # this if else statement need some small adjustments to get closer to the truest results
                                # error variation can go up to 3.5% sometimes but should not compromise piece finding applications
                                print(bestValue, result[0], possibleBestScale)
                                changePercentage = round((round((result[0] - bestValue), 6) / round((bestValue / 100.0), 6)), 3)
                                print(changePercentage)
                                if(result[0] >= bestValue and bestValue >= 0.300):
                                        bestScale = possibleBestScale
                                        bestValue = result[0]
                                        print(bestValue, bestScale)
                                elif(((bestValue < 0.250) and (((changePercentage > -30.0)) or (changePercentage > 15.0)))):
                                        bestScale = possibleBestScale
                                        bestValue = result[0]
                                        print(bestValue, bestScale)

                                        pass
                                else:
                                        print("broke")
                                        break

                if(bestScale < 0.1):
                        print("There is no chessboard on the screen!")
                        return

                return bestScale


        @staticmethod
        def _GetScaledBestValues(tempImgScale: float, img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None, canny: bool = False) -> tuple[float, cv.typing.Point]:
                """
                        This function scales down template image to find the closest occurance on the screen.
                        Converting both the main image and the template image to "edge detection" resulting type images to minimize calculations
                        Returns the best value of probability and the coordinates
                """

                if(tempImgScale > 1):
                        tempImgScale = 1
                else:
                        tempImgScale = round(tempImgScale, 3)

                if(tempImgScale < 1 and tempImgScale > 0):

                        scaledSizeOnScreen = tuple([int(x * tempImgScale) for x in tempImg.shape[:2]])

                        tempImg = cv.resize(tempImg, scaledSizeOnScreen, interpolation = cv.INTER_AREA)

                        if(isinstance(maskImg, cv.typing.MatLike)):
                                maskImg = cv.resize(maskImg, scaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                else:
                        return (float(0.0), (0, 0))

                if(canny):
                        tempImg = cv.Canny(tempImg, 0, 255, apertureSize = 7)

                return ScreenHandler._GetBestValues(img, tempImg, maskImg)


        @staticmethod
        def _CompareChange(oldImg: cv.typing.MatLike, newImg: cv.typing.MatLike) -> bool:
                """
                        This function compares two images and determines if they are the same or not.
                """
                if(ScreenHandler._GetBestValues(oldImg, newImg)[0] == 1): return True
                return False


        @staticmethod
        def _GetBestValues(img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None) -> tuple[float, cv.typing.Point]:
                """
                        This function uses template (and possibly matching mask) image(s) to find the best probability value and the location on the main image.
                """
                _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(img, tempImg, cv.TM_CCOEFF_NORMED, None, maskImg))
                return (bestValue, bestLocation)

        @staticmethod
        def _TakeScreenshot(bbox: tuple[int, int, int, int] = None) -> cv.typing.MatLike:
                """
                        This function takes the screenshot of the main screen, converts it to opencv grayscale type image and returns it.
                """
                # if(not(bbox == None)):
                #         pass
                return cv.cvtColor(np.array(IG.grab(bbox).convert("RGB"))[:, :, ::-1], cv.COLOR_BGR2GRAY)


SH = ScreenHandler()
SH.InitializeChessboard()

# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://stackoverflow.com/questions/35642497/python-opencv-cv2-matchtemplate-with-transparency
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://post.bytes.com/forum/topic/python/22175-multiply-a-tuple-by-a-constant?t=28276
# https://roboflow.com/use-opencv/convert-pil-image-to-cv2-image#:~:text=You%20can%20convert%20a%20PIL,BGR%20(the%20cv2%20format).
# some parts of these sources are used together to come up with the algorithms above

# https://stackoverflow.com/questions/62461590/grabbing-a-specific-part-of-screen-and-making-it-an-image-that-updates-itself-in