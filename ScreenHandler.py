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
import time
import asyncio as aio

from PIL import ImageGrab as IG

from Enums import PieceColourEnum, PieceTypeEnum
from ResourceHandler import BoardImg, PieceImgs

class ScreenHandler:
        """
                This class is used for all relevant image processing and data analysis functions.
        """

        # FIXME
        # Remove screenImg in prod
        _screenImg = cv.Canny(cv.imread("screenshot2.png", cv.IMREAD_GRAYSCALE), 225, 255)

        # This scale variable is used for determining max initial scale of the chessboard
        # that could be found on a screen.
        # Determined by screen resolution's short side's value and applied the multiplier inside the init function.
        _tempMaxScale = float()
        def __init__(self):

                scrShape = ScreenHandler._TakeScreenshot().shape[:2]
                lowestWidth = 0

                if(scrShape[0] < scrShape[1]):
                        lowestWidth = scrShape[0]
                else:
                        lowestWidth = scrShape[1]

                tempWidth = BoardImg._self.shape[0]

                if(tempWidth <= lowestWidth):
                        self._tempMaxScale = 1
                        return

                self._tempMaxScale = round((float(lowestWidth) / (float(tempWidth / 100.0))) / 100.0, 3)


        async def FindChessboardOnScreen(self):
                """
                        This function takes screenshots of the main screen and tries to find a chessboard on the screen.
                        If found, returns the scale and the position of the chessboard.
                        *** This function is in testing phase. Only pre-determined screenshots are used.
                        *** There are total of 7 screenshots currently (screenshot, screenshot1-6)
                """

                # screenImg = _TakeScreenshot()
                # FIX THIS BEFORE prod
                self._screenImg = cv.imread("screenshot.png", cv.IMREAD_GRAYSCALE)
                scale = await self._GetChessboardScaleWithPieceImg()

                result = ScreenHandler._GetScaledBestValues(scale, self._screenImg, BoardImg._self, BoardImg._mask)

                print("\nChessboard:")
                print("Scale: ", scale)
                print("Best Probability Score, Coordinates")
                print(result)


        async def _GetChessboardScaleWithPieceImg(self):
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

                        downResult = ScreenHandler._GetScaledBestValues((_scale - _scaleStep), _screenImg, PieceImgs[PieceColourEnum.BLACK - 1][PieceTypeEnum.KING - 1]._self, canny = True)
                        upResult = ScreenHandler._GetScaledBestValues((_scale + _scaleStep), _screenImg, PieceImgs[PieceColourEnum.BLACK - 1][PieceTypeEnum.KING - 1]._self, canny = True)
                        if(downResult[0] > upResult[0]):
                                return (True, downResult)
                        return (False, upResult)

                startTime = time.time()
                screenImg = cv.Canny(ScreenHandler._TakeScreenshot(), 225, 255)
                # remove below when in production
                screenImg = cv.Canny(self._screenImg, 225, 255)

                bestScale = self._tempMaxScale
                initialResult = ScreenHandler._GetScaledBestValues(bestScale, screenImg, PieceImgs[PieceColourEnum.BLACK - 1][PieceTypeEnum.KING - 1]._self, canny = True)
                bestValue = initialResult[0]
                bestLocation = initialResult[1]

                sweeps = (0.100, 0.010, 0.002)
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
                                bestLocation = _result[1][1]

                        while(True):
                                possibleBestScale = round((bestScale + (sweeps[i] * down)), 3)
                                print("Current Scale: ", possibleBestScale)
                                result = ScreenHandler._GetScaledBestValues(possibleBestScale, screenImg, PieceImgs[PieceColourEnum.BLACK - 1][PieceTypeEnum.KING - 1]._self, canny = True)
                                print("Best Probability Score, Best Coordinates Of Black King Piece")
                                print(result)
                                print("------")

                                # FIXME
                                # MAGIC NUMBERS
                                # this if else statement need some small adjustments to get closer to the truest results
                                # error variation can go up to 3.5% sometimes but should not compromise piece finding applications
                                if(result[0] > bestValue and (round((round((result[0] - bestValue), 6) / round((bestValue / 100.0), 6)), 3) > 0.700) or bestValue < 0.300):
                                        bestScale = possibleBestScale
                                        bestValue = result[0]
                                        bestLocation = result[1]
                                else:
                                        break

                print("|||||||||||||||||||||||||||||||||||||||||||||")
                print("Results:")
                print("time took:", time.time() - startTime)

                if(bestScale < 0.1):
                        print("There is no chessboard on the screen!")
                        return

                scaledSizeOnScreen = tuple([int(x * bestScale) for x in BoardImg._self.shape[:2]])

                print("Best Probable Scale:", bestScale, "Best Coordinates Of Black King Piece: ", bestLocation, "Scaled Size Of Chessboard:", scaledSizeOnScreen, sep = '\n')

                return bestScale


        @staticmethod
        def _GetScaledBestValues(tempImgScale: float, img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None, canny: bool = False) -> tuple[float, cv.typing.Point]:
                """
                        This function scales down template image to find the closest occurance on the screen.
                        Converting both the main image and the template image to "edge detectection" resulting type images to minimize calculations
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
                                maskImg = cv.resize(maskImg, scaledSizeOnScreen, interpolation = cv.INTER_AREA)
                else:
                        return (float(0.0), (0, 0))

                if(canny):
                        tempImg = cv.Canny(tempImg, 225, 255, apertureSize = 3)

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
                _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(img, tempImg, cv.TM_CCORR_NORMED, None, maskImg))
                return (bestValue, bestLocation)

        """
                This function takes the screenshot of the main screen, converts it to opencv grayscale type image and returns it.
        """
        @staticmethod
        def _TakeScreenshot(): return cv.cvtColor(np.array(IG.grab().convert("RGB"))[:, :, ::-1], cv.COLOR_BGR2GRAY)


sh = ScreenHandler()
aio.run((sh.FindChessboardOnScreen()))

# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://stackoverflow.com/questions/35642497/python-opencv-cv2-matchtemplate-with-transparency
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://post.bytes.com/forum/topic/python/22175-multiply-a-tuple-by-a-constant?t=28276
# https://roboflow.com/use-opencv/convert-pil-image-to-cv2-image#:~:text=You%20can%20convert%20a%20PIL,BGR%20(the%20cv2%20format).
# some parts of these sources are used together to come up with the algorithms above