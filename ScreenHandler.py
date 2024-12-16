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

        @staticmethod
        def InitializeChessboard():

                screenImg = ScreenHandler._TakeScreenshot()

                scrShape = screenImg.shape[:2]
                lowestWidth = int()

                if(scrShape[0] < scrShape[1]):
                        lowestWidth = scrShape[0]
                else:
                        lowestWidth = scrShape[1]

                tempWidth = BoardImg._self.shape[0]

                maxScale = round((float(lowestWidth) / (float(tempWidth / 100.0))), 3)
                print(maxScale)

                startTime = perf_counter()

                scale = ScreenHandler._GetChessboardScale(maxScale, screenImg)

                if(scale == 0.0):
                        return None

                currentWidth = round(BoardImg._self.shape[0] * (scale / 100.0))
                extra = currentWidth % 8

                onePercentOfBoardWidth = round((BoardImg._self.shape[0] / 100.0), 3)
                downScale = round((currentWidth - extra) / onePercentOfBoardWidth, 3)
                upScale = round((currentWidth + (8 - extra)) / onePercentOfBoardWidth, 3)

                print(downScale, upScale)

                # TODO
                # Need to implement the flipped version checking of the chessboard template image.

                downResult = ScreenHandler._GetScaledTempImgBestValues(downScale, screenImg, BoardImg._self, BoardImg._mask)
                upResult = ScreenHandler._GetScaledTempImgBestValues(upScale, screenImg, BoardImg._self, BoardImg._mask)

                algoScale = scale

                if(downResult[0] > upResult[0]):
                        result = downResult
                        scale = downScale
                else:
                        result = upResult
                        scale = upScale

                realWidth = round(BoardImg._self.shape[0] * (scale / 100.0))

                print("total time took:", round(perf_counter() - startTime, 6), "seconds")
                print(result, realWidth, scale)

                croppedImg = screenImg[result[1][1]:result[1][1] + realWidth, result[1][0]:result[1][0] + realWidth]

                croppedImg = ScreenHandler._CropImage(screenImg, result[1], realWidth)
                # return (round(perf_counter() - startTime, 6), result, realWidth, scale, screenImg[result[1][1]:result[1][1] + realWidth, result[1][0]:result[1][0] + realWidth])
                # return (scale, screenImg[result[1][1]:result[1][1] + realWidth, result[1][0]:result[1][0] + realWidth], result[1])
                return (croppedImg, scale, result[1], realWidth)

        @staticmethod
        def _CropImage(img: cv.typing.MatLike, point: cv.typing.Point, width: int):
                return img[point[1]:point[1] + width, point[0]:point[0] + width]


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
                return tuple([int(round(x / scale * 100)) for x in shape[:2]])[::-1]

        @staticmethod
        def _GetScaledTempImgSize(scale: float, shape):
                return tuple([int(round(x * (scale / 100))) for x in shape[:2]])[::-1]

        @staticmethod
        def _GetUpscaledImg(img: cv.typing.MatLike, scale: float):
                img = cv.resize(img, ScreenHandler._GetScaledImgSize(scale, img.shape), interpolation = cv.INTER_LINEAR_EXACT)
                return img

        @staticmethod
        def _GetScaledImgBestValues(imgScale: float, img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None) -> tuple[float, cv.typing.Point]:

                img = cv.resize(img, ScreenHandler._GetScaledImgSize(imgScale, img.shape), interpolation = cv.INTER_LINEAR_EXACT)
                img = cv.Canny(img, 160, 255, apertureSize = 3)

                return ScreenHandler._GetBestValues(img, tempImg, maskImg)

        @staticmethod
        def _GetScaledTempImgBestValues(tempImgScale: float, img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None):

                tempImg = cv.resize(tempImg, ScreenHandler._GetScaledTempImgSize(tempImgScale, tempImg.shape), interpolation = cv.INTER_LINEAR_EXACT)

                if(isinstance(maskImg, cv.typing.MatLike)):
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

# cv.imshow("", cv.threshold(PieceImgs[0][3].processedImgBlack, 128, 255, cv.THRESH_BINARY)[1])
# cv.waitKeyEx(0)
# cv.imshow("", cv.threshold(PieceImgs[1][3].processedImgWhite, 128, 255, cv.THRESH_BINARY)[1])
# cv.waitKeyEx(0)

# print(SH._GetBestValues(cv.threshold(PieceImgs[0][3].processedImgBlack, 128, 255, cv.THRESH_BINARY)[1], cv.threshold(PieceImgs[1][3].processedImgWhite, 128, 255, cv.THRESH_BINARY)[1])[0])

# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://stackoverflow.com/questions/35642497/python-opencv-cv2-matchtemplate-with-transparency
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://post.bytes.com/forum/topic/python/22175-multiply-a-tuple-by-a-constant?t=28276
# https://roboflow.com/use-opencv/convert-pil-image-to-cv2-image#:~:text=You%20can%20convert%20a%20PIL,BGR%20(the%20cv2%20format).
# https://learnopencv.com/cropping-an-image-using-opencv/

# https://stackoverflow.com/questions/62461590/grabbing-a-specific-part-of-screen-and-making-it-an-image-that-updates-itself-in
# https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga9d7064d478c95d60003cf839430737ed

# https://superfastpython.com/thread-return-values/

# https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image

# some parts of these sources are used together to come up with the algorithms above