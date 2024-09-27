import cv2 as cv
import numpy as np
from PIL import ImageGrab

# 744

class ScreenHandler:        
        _screenImg = cv.imread("screenshot.png", cv.IMREAD_COLOR)
        
        _tempImg = cv.imread("greenboard.png", cv.IMREAD_COLOR)
        
        print(_tempImg.shape)

        _alphaChannel = np.array(cv.imread("greenboard_mask.png", cv.IMREAD_UNCHANGED)[:,:,3])
        _maskImg = cv.merge([_alphaChannel, _alphaChannel, _alphaChannel])
        
        _sizeOnScreen = _tempImg.shape[:2]
        
        print(_sizeOnScreen)

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
                
                print(np.linspace(self._minScale, self._maxScale, totalScaleSteps), np.linspace(self._minScale, self._maxScale, totalScaleSteps)[::-1], sep = "\n\n")
                
                scaledSizeOnScreen = (0, 0)
                
                for scale in np.linspace(self._minScale, self._maxScale, totalScaleSteps)[::-1]:        
                        
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
                        
                scaleStepPercentage = 0.01
                
                upScaledSizeOnScreen = (int(self._sizeOnScreen[0] * (closestScale + scaleStepPercentage)), int(self._sizeOnScreen[1] * (closestScale + scaleStepPercentage)))
                downScaledSizeOnScreen = (int(self._sizeOnScreen[0] * (closestScale - scaleStepPercentage)), int(self._sizeOnScreen[1] * (closestScale + scaleStepPercentage)))
                
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

                closestScale += scaleStepPercentage
                        
                while(True):
                        scaledSizeOnScreen = (int(self._sizeOnScreen[0] * (closestScale + scaleStepPercentage)), int(self._sizeOnScreen[1] * scale))
                        
                        scaledTempImg = cv.resize(self._tempImg, scaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                        scaledMaskImg = cv.resize(self._maskImg, scaledSizeOnScreen, interpolation = cv.INTER_LINEAR)
                        
                        _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(self._screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                
                        if(bestValue > closestValue):
                                closestValue = bestValue
                                closestPosition = bestLocation
                                closestScale += scaleStepPercentage
                                
                                print(scaledSizeOnScreen, bestValue, closestScale, sep = '\n')
                        else:
                                break
                
                print(closestValue, closestPosition, closestScale, sep = '\n')


                                
        
        def _getTotalScaleSteps(self, scaleStepPercentage: float):
                return int((self._maxScale - self._minScale) / scaleStepPercentage) + 1
                
sh = ScreenHandler()

sh.FindBestPosition()

