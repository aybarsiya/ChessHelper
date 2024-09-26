import cv2 as cv
import numpy as np
from PIL import ImageGrab

# 744

class ScreenHandler:        
        screenImg = cv.imread("screenshot.png", cv.IMREAD_COLOR)
        
        tempImg = cv.imread("greenboard.png", cv.IMREAD_COLOR)

        alphaChannel = np.array(cv.split(tempImg)[3])
        maskImg = cv.merge([alphaChannel, alphaChannel, alphaChannel])
        
        sizeOnScreen = tempImg.shape[:2]

        minScale = float(40)
        maxScale = float(90)
        initialScaleStepPercentage = float(5)
        
        def FindBestPosition(self):
                closestValue = float
                closestPosition = cv.typing.Point()
                closestScale = float
                
                scaleStepPercentage = self.initialScaleStepPercentage
                
                totalScaleSteps = self.updateTotalScaleSteps(self.initialScaleStepPercentage)
                
                while (totalScaleSteps <= 1):
                        if(scaleStepPercentage == self.initialScaleStepPercentage):
                                for scale in np.fliplr(np.linspace(self.minScale, self.maxScale, totalScaleSteps)):        
                                        scaledTempImg = cv.resize(self.tempImg, self.sizeOnScreen * scale, interpolation = cv.INTER_LINEAR)
                                        scaledMaskImg = cv.resize(self.maskImg, self.sizeOnScreen * scale, interpolation = cv.INTER_LINEAR)
                                
                                        _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(self.screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                                
                                        if(bestValue > closest):
                                                closestValue = bestValue
                                        else:
                                                scaleStepPercentage -= 1
                                                break
                        else:
                                for scale in np.fliplr(np.linspace(self.minScale, self.maxScale, totalScaleSteps)):        
                                        scaledTempImg = cv.resize(self.tempImg, self.sizeOnScreen * scale, interpolation = cv.INTER_LINEAR)
                                        scaledMaskImg = cv.resize(self.maskImg, self.sizeOnScreen * scale, interpolation = cv.INTER_LINEAR)
                                
                                        _, bestValue, _, bestLocation = cv.minMaxLoc(cv.matchTemplate(self.screenImg, scaledTempImg, cv.TM_CCORR_NORMED, None, scaledMaskImg))
                                
                                        if(bestValue > closest):
                                                closest = bestValue
                                        else:
                                                scaleStepPercentage -= 1
                                                break
                                
        
        def _getTotalScaleSteps(self, scaleStepPercentage: float):
                return (self.maxScale - self.minScale) / scaleStepPercentage
                




