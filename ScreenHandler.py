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
        
        _downsizeScale = 0.700
        
        _downsizeInterpolation = cv.INTER_AREA
        
        async def FindChessboardPosition(self):
                
                self._tempImgDownsized = self._screenImgUntouched
                
                print(self._FindMinMaxLoc(1, self._screenImgUntouched))
                cv.imshow("", self._screenImgUntouched)
                cv.waitKeyEx(0)
                
                
                closestValue = float()
                closestPosition = tuple[int(), int()]
                closestScale = float()
                
                screenshot = self._TakeScreenshot()
                self._DownsizeImgs()
                
                scale = 0.900
                
                print("|||||||||||||||||||||||||||||||||||||||||||||")
                
                while(scale >= 0):
                        
                        print(scale)
                        print(self._FindMinMaxLoc(scale, self._screenImgDownsized))
                        print("------")
                        scale = round((scale - 0.020), 3)
                        
                scale = 0.70
                
                print("---------------------------------------------")
                
                while(scale >= 0.670):
                        
                        print(scale)
                        print(self._FindMinMaxLoc(scale, self._screenImgDownsized))
                        print("------")
                        scale = round((scale - 0.002), 3)
                        
                
                print("===== RESULTS: ", "\nClosest Matching Value: ", closestValue, "\nClosest Matching Position: ", closestPosition, "\nClosest Matching Scale: ", closestScale, "\nClosest Matching Size: ", closestScaledSizeOnScreen, "\nTotal Time: ", totalTimeTook, sep = '')

        
        def _FindMinMaxLoc(self, scalePercentage: float, screenImg: cv.typing.MatLike) -> tuple[float, cv.typing.Point]:
                
                scalePercentage = round(scalePercentage, 3)
                
                if(scalePercentage != 1):
                        
                        if(scalePercentage > 1): return
                        
                        else:
                                scaledSizeOnScreen = tuple([int(x * scalePercentage) for x in self._tempImgDownsized.shape[:2]])
                
                                scaledTempImg = cv.resize(self._tempImgDownsized.copy(), scaledSizeOnScreen, interpolation = self._downsizeInterpolation)
                                scaledMaskImg = cv.resize(self._tempImgDownsized.copy(), scaledSizeOnScreen, interpolation = self._downsizeInterpolation)
                
                else:
                        scaledTempImg = self._tempImgDownsized.copy()
                        scaledMaskImg = self._tempImgDownsized.copy()
                

                                
                _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                                                
                return tuple[bestValue, bestLocation]
        
        def _CompareImgs(self, oldImg: cv.typing.MatLike, newImg: cv.typing.MatLike) -> bool:
                _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(oldImg, newImg, cv.TM_CCORR_NORMED, None))
                if(bestValue == 1): return True
                return False
        
        def _DownsizeImgs(self):
                
                if(self._downsizedScale != None) and (round(self._downsizedScale, 3) == round(self._downsizeScale, 3)): return
                
                # self._screenImgDownsized = cv.resize(self._screenImgUntouched, tuple([int(x * self._downsizeScale) for x in self._screenImgUntouched.shape[:2]]), interpolation = self._downsizeInterpolation)
                # self._tempImgDownsized = cv.resize(self._tempImgUntouched, tuple([int(x * self._downsizeScale) for x in self._tempImgUntouched.shape[:2]]), interpolation = self._downsizeInterpolation)
                # self._maskImgDownsized = cv.resize(self._maskImgUntouched, tuple([int(x * self._downsizeScale) for x in self._maskImgUntouched.shape[:2]]), interpolation = self._downsizeInterpolation)
                
                self._screenImgDownsized = self._screenImgUntouched
                self._tempImgDownsized = self._tempImgUntouched
                self._maskImgDownsized = self._maskImgUntouched
        
        def _TakeScreenshot(self):
                
                return cv.cvtColor(np.array(IG.grab().convert("RGB"))[:, :, ::-1], cv.COLOR_BGR2GRAY)
        

sh = ScreenHandler()
aio.run((sh.FindChessboardPosition()))

# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://stackoverflow.com/questions/35642497/python-opencv-cv2-matchtemplate-with-transparency
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://post.bytes.com/forum/topic/python/22175-multiply-a-tuple-by-a-constant?t=28276
# https://roboflow.com/use-opencv/convert-pil-image-to-cv2-image#:~:text=You%20can%20convert%20a%20PIL,BGR%20(the%20cv2%20format).
# some parts of these sources are used together to come up with the algorithm above