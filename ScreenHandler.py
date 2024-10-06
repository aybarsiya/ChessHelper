from tracemalloc import start
import cv2 as cv
import numpy as np
import time
import asyncio as aio

from PIL import ImageGrab as IG

class ScreenHandler:

        _screenImg = cv.imread("screenshot2.png", cv.IMREAD_GRAYSCALE)
        _tempImg = cv.imread(r"resources\board\greenboard.png", cv.IMREAD_GRAYSCALE)
        _maskImg = cv.merge([cv.imread(r"resources\board\greenboard_mask.png", cv.IMREAD_UNCHANGED)[:,:,3]])

        _scale = float()

        def __init__(self):

                scrShape = ScreenHandler._TakeScreenshot().shape[:2]
                lowestWidth = 0

                if(scrShape[0] < scrShape[1]):
                        lowestWidth = scrShape[0]
                else:
                        lowestWidth = scrShape[1]

                tempWidth = self._tempImg.shape[0]

                if(tempWidth <= lowestWidth):
                        self._scale = 1
                        return

                self._scale = (float(lowestWidth) / (float(tempWidth) / 100.0)) / 100.0

                pass

        async def FindChessboardPosition(self):

                startTime = time.time()

                screenImg = ScreenHandler._TakeScreenshot()

                closestValue = float()
                closestPosition = tuple[int(), int()]

                print("|||||||||||||||||||||||||||||||||||||||||||||")

                while(self._scale >= 0.500):

                        print(self._scale)
                        print(await ScreenHandler._GetScaledBestValues(self._scale, self._screenImg, self._tempImg, self._maskImg))
                        print("------")
                        self._scale = round((self._scale - 0.100), 3)

                print("|||||||||||||||||||||||||||||||||||||||||||||")

                print("time took:", time.time() - startTime)

        @staticmethod
        async def _GetScaledBestValues(tempImgScale: float, img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None) -> tuple[float, cv.typing.Point]:

                if(tempImgScale > 1):
                        tempImgScale = 1
                else:
                        tempImgScale = round(tempImgScale, 3)

                if(tempImgScale < 1):

                        scaledSizeOnScreen = tuple([int(x * tempImgScale) for x in tempImg.shape[:2]])

                        tempImg = cv.resize(tempImg, scaledSizeOnScreen, interpolation = cv.INTER_AREA)
                        maskImg = cv.resize(maskImg, scaledSizeOnScreen, interpolation = cv.INTER_AREA)

                return await ScreenHandler._GetBestValues(img, tempImg, maskImg)

        @staticmethod
        async def _CompareChange(oldImg: cv.typing.MatLike, newImg: cv.typing.MatLike) -> bool:
                if(await ScreenHandler._GetBestValues(oldImg, newImg)[0] == 1): return True
                return False

        @staticmethod
        async def _GetBestValues(img: cv.typing.MatLike, tempImg: cv.typing.MatLike, maskImg: cv.typing.MatLike = None) -> tuple[float, cv.typing.Point]:
                _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(img, tempImg, cv.TM_CCORR_NORMED, None, maskImg))
                return (bestValue, bestLocation)

        @staticmethod
        def _TakeScreenshot(): return cv.cvtColor(np.array(IG.grab().convert("RGB"))[:, :, ::-1], cv.COLOR_BGR2GRAY)


sh = ScreenHandler()


aio.run((sh.FindChessboardPosition()))

# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://stackoverflow.com/questions/35642497/python-opencv-cv2-matchtemplate-with-transparency
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://post.bytes.com/forum/topic/python/22175-multiply-a-tuple-by-a-constant?t=28276
# https://roboflow.com/use-opencv/convert-pil-image-to-cv2-image#:~:text=You%20can%20convert%20a%20PIL,BGR%20(the%20cv2%20format).
# some parts of these sources are used together to come up with the algorithm above