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
from time import perf_counter, sleep

from PIL import ImageGrab as IG

from Enums import PieceColourEnum, PieceTypeEnum
from ResourceHandler import BoardImg, PieceImgs

from threading import Thread

class ScreenHandler:

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

                self._maxScale = round((float(lowestWidth) / (float(tempWidth / 100.0))), 3)
                print(self._maxScale)

                if(self._maxScale > 100.0):
                        self._maxScale = 100.0

        def InitializeChessboard(self, fileName):

                screenImg = self._TakeScreenshot()
                screenImg = cv.imread(fileName, cv.IMREAD_GRAYSCALE)

                startTime = perf_counter()

                scale = self._GetChessboardScale(self._maxScale, screenImg)

                if(scale == 0.0):
                        return

                currentWidth = round(BoardImg._self.shape[0] * (scale / 100.0))
                extra = currentWidth % 8

                onePercentOfBoardWidth = round((BoardImg._self.shape[0] / 100.0), 3)
                downScale = round((currentWidth - extra) / onePercentOfBoardWidth, 3)
                upScale = round((currentWidth + (8 - extra)) / onePercentOfBoardWidth, 3)

                print(downScale, upScale)

                downResult = ScreenHandler._GetScaledTempImgBestValues(downScale, screenImg, BoardImg._self, BoardImg._mask)
                upResult = ScreenHandler._GetScaledTempImgBestValues(upScale, screenImg, BoardImg._self, BoardImg._mask)

                if(downResult > upResult):
                        result = downResult
                        scale = downScale
                else:
                        result = upResult
                        scale = upScale

                print("total time took:", round(perf_counter() - startTime, 6), "seconds")
                print(result, round(BoardImg._self.shape[0] * (scale / 100.0)), scale)

                return (round(perf_counter() - startTime, 6), result, round(BoardImg._self.shape[0] * (scale / 100.0)), scale)

        @staticmethod
        def _GetChessboardScale(maxScale: float, screenImg: cv.typing.MatLike):

                def _IsDown(_scale: float, _scaleStep: float, _screenImg: cv.typing.MatLike, _tempImg: cv.typing.MatLike):

                        downResult = ScreenHandler._GetScaledImgBestValues(
                                                                                                round((_scale - _scaleStep), 3),
                                                                                                _screenImg,
                                                                                                _tempImg,
                                                                                                )
                        upResult = ScreenHandler._GetScaledImgBestValues(
                                                                                                round((_scale + _scaleStep), 3),
                                                                                                _screenImg,
                                                                                                _tempImg,
                                                                                                )

                        print("up: ", upResult[0], "down: ", downResult[0])
                        if(downResult[0] > upResult[0]):
                                return (True, downResult)
                        return (False, upResult)

                screenImg = cv.bilateralFilter(screenImg, 3, 500, 500)

                kingImg = PieceImgs[PieceColourEnum.WHITE][PieceTypeEnum.KING]._self
                kingImg = cv.bilateralFilter(kingImg, 5, 250, 250)
                kingImg = cv.Canny(kingImg, 240, 255, apertureSize = 3)

                bestScale = maxScale
                initialResult = ScreenHandler._GetScaledImgBestValues(
                                                                                                bestScale,
                                                                                                screenImg,
                                                                                                kingImg,
                                                                                                )
                bestValue = initialResult[0]

                print(bestScale, bestValue)

                sweeps = (4.0, 1.0, 0.5)
                down = -1.0

                for i in range(len(sweeps)):

                        if(i > 0):
                                _result = _IsDown(bestScale, sweeps[i], screenImg, kingImg)

                                if(_result[1][0] < bestValue and (i + 1) != len(sweeps)):
                                        print("broke")
                                        continue

                                if(_result[0]):
                                        down = -1.0
                                else:
                                        down = 1.0
                                bestScale = round(bestScale + (sweeps[i] * down), 3)
                                bestValue = _result[1][0]
                                print(bestValue, bestScale)

                        while(True):
                                possibleBestScale = round(bestScale + (sweeps[i] * down), 3)
                                result = ScreenHandler._GetScaledImgBestValues(
                                                                                                        possibleBestScale,
                                                                                                        screenImg,
                                                                                                        kingImg,
                                                                                                        )

                                print(possibleBestScale, result[0])
                                changePercentage = round(((result[0] - bestValue) / (bestValue / 100.0)), 4)
                                print(changePercentage)
                                if(result[0] >= bestValue or (bestValue < 0.270 and changePercentage > -10.0)):
                                        bestScale = possibleBestScale
                                        bestValue = result[0]
                                        print(bestValue, bestScale)
                                else:
                                        print("broke")
                                        break

                print("bestValue:", bestValue)
                if(bestValue < 0.52):
                        print("There is no chessboard on the screen!")
                        return 0.0

                return bestScale

        @staticmethod
        def _GetScaledImgSize(scale: float, shape):
                return tuple([int(x / scale * 100) for x in shape[:2]])[::-1]

        @staticmethod
        def _GetScaledTempImgSize(scale: float, shape):
                return tuple([int(x * (scale / 100)) for x in shape[:2]])[::-1]

        @staticmethod
        def _GetScaledImgBestValues(imgScale: float, img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None) -> tuple[float, cv.typing.Point]:

                img = cv.resize(img, ScreenHandler._GetScaledImgSize(imgScale, img.shape), interpolation = cv.INTER_LINEAR_EXACT)
                img = cv.Canny(img, 160, 255, apertureSize = 3)

                return ScreenHandler._GetBestValues(img, tempImg, maskImg)

        @staticmethod
        def _GetScaledTempImgBestValues(tempImgScale: float, img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None):

                tempImg = cv.resize(tempImg, ScreenHandler._GetScaledTempImgSize(tempImgScale, tempImg.shape), interpolation = cv.INTER_LINEAR_EXACT)
                maskImg = cv.resize(maskImg, ScreenHandler._GetScaledTempImgSize(tempImgScale, maskImg.shape), interpolation = cv.INTER_LINEAR_EXACT)

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

        @staticmethod
        def _TakeScreenshot(bbox: tuple[int, int, int, int] = None) -> cv.typing.MatLike:
                """
                        This function takes the screenshot of the main screen, converts it to opencv grayscale type image and returns it.
                """
                # if(not(bbox == None)):
                #         pass
                return cv.cvtColor(np.array(IG.grab(bbox).convert("RGB"))[:, :, ::-1], cv.COLOR_BGR2GRAY)


SH = ScreenHandler()
results = []

for x in range(1, 9):
        results.append(SH.InitializeChessboard(f"screenshot{x}.png"))
        sleep(1)

print("------------------------------")

for x in range(len(results)):
        print("total time took:", results[x][0], "seconds")
        print(results[x][1], results[x][2], results[x][3])
        print("-----")

# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://stackoverflow.com/questions/35642497/python-opencv-cv2-matchtemplate-with-transparency
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://post.bytes.com/forum/topic/python/22175-multiply-a-tuple-by-a-constant?t=28276
# https://roboflow.com/use-opencv/convert-pil-image-to-cv2-image#:~:text=You%20can%20convert%20a%20PIL,BGR%20(the%20cv2%20format).

# https://stackoverflow.com/questions/62461590/grabbing-a-specific-part-of-screen-and-making-it-an-image-that-updates-itself-in
# https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga9d7064d478c95d60003cf839430737ed

# https://superfastpython.com/thread-return-values/

# some parts of these sources are used together to come up with the algorithms above