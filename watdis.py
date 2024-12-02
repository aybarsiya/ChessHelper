import cv2 as cv
import numpy as np
from ResourceHandler import PieceImgs

whiteKingImg = PieceImgs[0][5]._croppedSelf
tileImg = PieceImgs[2][0]._self[0:whiteKingImg.shape[0], 0:whiteKingImg.shape[1]]
alphaChannelNormed = PieceImgs[0][5]._croppedAlphaChannel[0:whiteKingImg.shape[0], 0:whiteKingImg.shape[1]] / 255.0

print(alphaChannelNormed)

cv.imshow("", whiteKingImg)
cv.waitKeyEx(0)
cv.imshow("", tileImg)
cv.waitKeyEx(0)

print(tileImg.shape, whiteKingImg.shape)

comp = tileImg * (1.0 - alphaChannelNormed) + whiteKingImg * alphaChannelNormed
cv.imwrite("comp.png", comp)
comp = cv.imread("comp.png", cv.IMREAD_GRAYSCALE)
cv.imshow("", comp)
cv.waitKeyEx(0)



background = cv.imread('field.jpg')
overlay = cv.imread('dice.png', cv.IMREAD_UNCHANGED)  # IMREAD_UNCHANGED => open image with the alpha channel

# separate the alpha channel from the color channels
alpha_channel = overlay[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
overlay_colors = overlay[:, :, :3]

# To take advantage of the speed of numpy and apply transformations to the entire image with a single operation
# the arrays need to be the same shape. However, the shapes currently looks like this:
#    - overlay_colors shape:(width, height, 3)  3 color values for each pixel, (red, green, blue)
#    - alpha_channel  shape:(width, height, 1)  1 single alpha value for each pixel
# We will construct an alpha_mask that has the same shape as the overlay_colors by duplicate the alpha channel
# for each color so there is a 1:1 alpha channel for each color channel
alpha_mask = alpha_channel[:, :, np.newaxis]

# The background image is larger than the overlay so we'll take a subsection of the background that matches the
# dimensions of the overlay.
# NOTE: For simplicity, the overlay is applied to the top-left corner of the background(0,0). An x and y offset
# could be used to place the overlay at any position on the background.
h, w = overlay.shape[:2]
background_subsection = background[0:h, 0:w]

# combine the background with the overlay image weighted by alpha
composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask

# overwrite the section of the background image that has been updated
background[0:h, 0:w] = composite

cv.imwrite('combined.png', background)