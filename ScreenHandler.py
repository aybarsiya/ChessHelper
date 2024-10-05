import cv2 as cv
import numpy as np
import time
import asyncio as aio

from PIL import ImageGrab as IG

class ScreenHandler:        
        
        _screenImgUntouched = cv.imread("screenshot2.png", cv.IMREAD_GRAYSCALE)        
        _tempImgUntouched = cv.imread(r"resources\board\greenboard.png", cv.IMREAD_GRAYSCALE)
        _maskImgUntouched = cv.merge([cv.imread(r"resources\board\greenboard_mask.png", cv.IMREAD_UNCHANGED)[:,:,3]])
        
        _screenImgDownsized = None
        _tempImgDownsized = None
        _maskImgDownsized = None
        _downsizedScale = None
                
        _tempImgSize = _tempImgUntouched.shape[:2]
        
        _downsizeScale = 0.500
        
        _downsizeInterpolation = cv.INTER_LINEAR
        
        async def FindChessboardPosition(self):
                
                # await aio.sleep(3)
                screenshot = self._TakeScreenshot()
                                
                closestValue = float()
                closestPosition = (int(), int())
                closestScale = float()
                
                # scaleStepPercentage = self._initialScaleStepPercentage
                
                # totalScaleSteps = int((self._maxScale - self._minScale) / scaleStepPercentage) + 1
                
                # print(totalScaleSteps)
                
                scaledSizeOnScreen = (0, 0)
                
                startTime = time.time()
                
                scale = 0.900
                
                stime = time.time()
                
                self._DownsizeImgs()
                
                while(scale >= 0.400):
                        
                        print(scale)
                        print(self._FindMinMaxLoc(scale, self._screenImg))
                        print("------")
                        scale = round((scale - 0.100), 20)
                        
                print(time.time() - stime)
                
                
                
                for scale in np.linspace(self._minScale, self._maxScale, totalScaleSteps)[::-1]:        
                        
                        scaledSizeOnScreen = tuple[int]()
                        scaledSizeOnScreen = (int(self._tempImgSize[0] * scale), int(self._tempImgSize[1] * scale))
                        
                        scaledTempImg = cv.resize(self._tempImg, scaledSizeOnScreen, interpolation = cv.INTER_AREA)
                        scaledMaskImg = cv.resize(self._maskImg, scaledSizeOnScreen, interpolation = cv.INTER_AREA)

                        _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(self._screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                                        
                        if(bestValue > closestValue):
                                
                                closestValue = bestValue
                                closestScale = float(scale)
                                
                                print(scaledSizeOnScreen, bestValue, closestScale, sep = '\n')
                        else:
                                break
                        
                scaleStepPercentage = 0.002
                
                upScaledSizeOnScreen = (int(self._tempImgSize[0] * (closestScale + scaleStepPercentage)), int(self._tempImgSize[1] * (closestScale + scaleStepPercentage)))
                downScaledSizeOnScreen = (int(self._tempImgSize[0] * (closestScale - scaleStepPercentage)), int(self._tempImgSize[1] * (closestScale - scaleStepPercentage)))
                
                scaledTempImg = cv.resize(self._tempImg, upScaledSizeOnScreen, interpolation = cv.INTER_AREA)
                scaledMaskImg = cv.resize(self._maskImg, upScaledSizeOnScreen, interpolation = cv.INTER_AREA)
                _, upBestValue, _, upBestLocation = cv.minMaxLoc(cv.matchTemplate(self._screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                
                scaledTempImg = cv.resize(self._tempImg, downScaledSizeOnScreen, interpolation = cv.INTER_AREA)
                scaledMaskImg = cv.resize(self._maskImg, downScaledSizeOnScreen, interpolation = cv.INTER_AREA)
                _, downBestValue, _, downBestLocation = cv.minMaxLoc(cv.matchTemplate(self._screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                
                if(downBestValue > upBestValue):
                        
                        scaleStepPercentage *= -1.0
                        closestValue = downBestValue
                        closestPosition = downBestLocation
                else:
                        
                        closestValue = upBestValue
                        closestPosition = upBestLocation

                print(scaleStepPercentage, upBestValue, downBestValue)
                closestScale += scaleStepPercentage
                
                closestScaledSizeOnScreen = (0, 0)
                        
                while(True):
                        scaledSizeOnScreen = (int(self._tempImgSize[0] * (closestScale + scaleStepPercentage)), int(self._tempImgSize[1] * (closestScale + scaleStepPercentage)))
                        
                        scaledTempImg = cv.resize(self._tempImg, scaledSizeOnScreen, interpolation = cv.INTER_AREA)
                        scaledMaskImg = cv.resize(self._maskImg, scaledSizeOnScreen, interpolation = cv.INTER_AREA)
                        
                        _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(self._screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                        
                        print(f"bv {bestValue}")
                
                        if(bestValue > closestValue):
                                closestValue = bestValue
                                closestPosition = bestLocation
                                closestScale += scaleStepPercentage
                                
                                closestScaledSizeOnScreen = scaledSizeOnScreen
                                
                                print(scaledSizeOnScreen, bestValue, closestScale, sep = '\n')
                        else:
                                break
                        
                totalTimeTook = time.time() - startTime
                
                print("===== RESULTS: ", "\nClosest Matching Value: ", closestValue, "\nClosest Matching Position: ", closestPosition, "\nClosest Matching Scale: ", closestScale, "\nClosest Matching Size: ", closestScaledSizeOnScreen, "\nTotal Time: ", totalTimeTook, sep = '')

        
        def _FindMinMaxLoc(self, scalePercentage: float, screenImg: cv.typing.MatLike) -> tuple[float, cv.typing.Point]:
                
                print(screenImg.shape)
                scalePercentage = round(scalePercentage, 3)
                scaledSizeOnScreen = tuple([int(x * scalePercentage) for x in self._tempImgSize])
                
                screenImg = cv.resize(screenImg, tuple([int(x * self._downsizeScale) for x in screenImg.shape[:2]]), interpolation = self._downsizeInterpolation)
                                                                                
                scaledTempImg = cv.resize(self._tempImg.copy(), scaledSizeOnScreen, interpolation = self._downsizeInterpolation)
                scaledMaskImg = cv.resize(self._maskImg.copy(), scaledSizeOnScreen, interpolation = self._downsizeInterpolation)
                                
                print(scaledTempImg.shape)

                _1, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                
                print(_1, bestValue, sep = ' ')
                                
                return tuple[bestValue, bestLocation]
        
        def _DownsizeImgs(self):
                
                if(round(self._downsizedScale, 3) == round(self._downsizeScale, 3)) and (self._downsizedScale != None): return
                
                self._screenImgDownsized = cv.resize(self._screenImgUntouched, tuple([int(x * self._downsizeScale) for x in self._screenImgUntouched.shape[:2]]), interpolation = self._downsizeInterpolation)
                self._tempImgDownsized = cv.resize(self._tempImgUntouched, tuple([int(x * self._downsizeScale) for x in self._tempImgUntouched.shape[:2]]), interpolation = self._downsizeInterpolation)
                self._maskImgDownsized = cv.resize(self._maskImgUntouched, tuple([int(x * self._downsizeScale) for x in self._maskImgUntouched.shape[:2]]), interpolation = self._downsizeInterpolation)
        
        def _TakeScreenshot(self):
                
                return cv.cvtColor(np.array(IG.grab().convert("RGB"))[:, :, ::-1], cv.COLOR_BGR2GRAY)
                


sh = ScreenHandler()

aio.run(sh.FindChessboardPosition())

# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://stackoverflow.com/questions/35642497/python-opencv-cv2-matchtemplate-with-transparency
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://post.bytes.com/forum/topic/python/22175-multiply-a-tuple-by-a-constant?t=28276
# https://roboflow.com/use-opencv/convert-pil-image-to-cv2-image#:~:text=You%20can%20convert%20a%20PIL,BGR%20(the%20cv2%20format).
# some parts of these sources are used together to come up with the algorithm above