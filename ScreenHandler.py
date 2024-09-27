import cv2 as cv
import numpy as np
# from PIL import ImageGrab as imgGrab

# 744

class ScreenHandler:        
        _screenImg = cv.imread("screenshot2.png", cv.IMREAD_COLOR)
        
        _tempImg = cv.imread("greenboard.png", cv.IMREAD_COLOR)

        _alphaChannel = np.array(cv.imread("greenboard_mask.png", cv.IMREAD_UNCHANGED)[:,:,3])
        _maskImg = cv.merge([_alphaChannel, _alphaChannel, _alphaChannel])
        
        _sizeOnScreen = _tempImg.shape[:2]

        _minScale = 0.4
        _maxScale = 0.9
        _initialScaleStepPercentage = 0.05
        
        def FindBestPosition(self):
                
                closestValue = float()
                closestPosition = (0, 0)
                closestScale = float()
                
                scaleStepPercentage = self._initialScaleStepPercentage
                
                totalScaleSteps = self._getTotalScaleSteps(self._initialScaleStepPercentage)
                
                print(totalScaleSteps)
                
                print(np.linspace(self._minScale, self._maxScale, totalScaleSteps), np.linspace(self._minScale, self._maxScale, totalScaleSteps)[:-1], sep = "\n\n")
                
                scaledSizeOnScreen = (0, 0)
                
                for scale in np.linspace(self._minScale, self._maxScale, totalScaleSteps)[::-1]:        
                        scaledSizeOnScreen = tuple[int]()
                        scaledSizeOnScreen = (int(self._sizeOnScreen[0] * scale), int(self._sizeOnScreen[1] * scale))
                        
                        scaledTempImg = cv.resize(self._tempImg, scaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                        scaledMaskImg = cv.resize(self._maskImg, scaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                
                        _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(self._screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                
                        if(bestValue > closestValue):
                                
                                closestValue = bestValue
                                closestScale = float(scale)
                                
                                print(scaledSizeOnScreen, bestValue, closestScale, sep = '\n')
                        else:
                                break
                        
                scaleStepPercentage = 0.002
                
                upScaledSizeOnScreen = (int(self._sizeOnScreen[0] * (closestScale + scaleStepPercentage)), int(self._sizeOnScreen[1] * (closestScale + scaleStepPercentage)))
                downScaledSizeOnScreen = (int(self._sizeOnScreen[0] * (closestScale - scaleStepPercentage)), int(self._sizeOnScreen[1] * (closestScale - scaleStepPercentage)))
                
                scaledTempImg = cv.resize(self._tempImg, upScaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                scaledMaskImg = cv.resize(self._maskImg, upScaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                _, upBestValue, _, upBestLocation = cv.minMaxLoc(cv.matchTemplate(self._screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                
                scaledTempImg = cv.resize(self._tempImg, downScaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                scaledMaskImg = cv.resize(self._maskImg, downScaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
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
                        scaledSizeOnScreen = (int(self._sizeOnScreen[0] * (closestScale + scaleStepPercentage)), int(self._sizeOnScreen[1] * (closestScale + scaleStepPercentage)))
                        
                        scaledTempImg = cv.resize(self._tempImg, scaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                        scaledMaskImg = cv.resize(self._maskImg, scaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                        
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
                
                print("===== RESULTS: ", "\nClosest Matching Value: ", closestValue, "\nClosest Matching Position: ", closestPosition, "\nClosest Matching Scale: ", closestScale, "\nClosest Matching Size: ", closestScaledSizeOnScreen, sep = '')


                                
        
        def _getTotalScaleSteps(self, scaleStepPercentage: float):
                return int((self._maxScale - self._minScale) / scaleStepPercentage) + 1
                
sh = ScreenHandler()

sh.FindBestPosition()

# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://stackoverflow.com/questions/35642497/python-opencv-cv2-matchtemplate-with-transparency
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://post.bytes.com/forum/topic/python/22175-multiply-a-tuple-by-a-constant?t=28276
# some parts of these sources are used together to come up with the algorithm above