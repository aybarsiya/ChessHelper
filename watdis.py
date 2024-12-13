import cv2 as cv
import numpy as np
from ResourceHandler import PieceImgs

whiteKingImg = PieceImgs[0][5]._croppedSelf
tileImg = PieceImgs[2][0]._self[0:whiteKingImg.shape[0], 0:whiteKingImg.shape[1]]
alphaChannelNormed = PieceImgs[0][5]._croppedAlphaChannel / 255.0

cv.imshow("", whiteKingImg)
cv.waitKeyEx(0)
cv.imshow("", tileImg)
cv.waitKeyEx(0)

print(tileImg.shape, whiteKingImg.shape)

comp = tileImg * (1.0 - alphaChannelNormed) + whiteKingImg * alphaChannelNormed
cv.imshow("", comp.astype(np.int8))
cv.imwrite("comp.png", comp)
comp = cv.imread("comp.png", cv.IMREAD_GRAYSCALE)
cv.imshow("", comp)
cv.waitKeyEx(0)