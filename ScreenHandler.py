import cv2 as cv
import numpy as np

# 744

sizeOnScreen = (600, 600)

img = cv.imread("screenshot.png", cv.IMREAD_COLOR)
templ = cv.resize(cv.imread("greenboard.png", cv.IMREAD_COLOR), sizeOnScreen, interpolation= cv.INTER_LINEAR)

print(img.shape)
print(templ.shape)

alpha_channel = np.array(cv.split(cv.resize(cv.imread("greenboard_mask.png", cv.IMREAD_UNCHANGED), sizeOnScreen, interpolation= cv.INTER_LINEAR))[3]) 
mask = cv.merge([alpha_channel, alpha_channel, alpha_channel])

print(mask.shape)

result = cv.matchTemplate(img, templ, cv.TM_CCORR_NORMED, None, mask)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print('Highest correlation WITH mask', max_val)
print(f"{min_loc} {max_loc}")
print(result.max())
print(result.min())