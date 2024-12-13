"""
        ResourceHandler Module

        This module is responsible for initializing and keeping fast access resources organized.

        Features;
        - Locating and loading images of chess pieces
                - To be used for;
                        - Recognising chessboard on the screen
                        - Recognising chess pieces on the board
        - Keeping opencv's Matlike type image objects in the memory
        - PieceImgs object keeps all the chess pieces and retrival is done using piece enums in the Enums module
        - BoardImg object keep the board image

        Aybars Ay
        2024
"""

import cv2 as cv
import numpy as np
from Enums import PieceTypeEnum, PieceColourEnum

class _TempImg():
        """
                This base class is designed to load both grayscale and transparency mask images from a given resource path.
        """

        _self: cv.typing.MatLike
        _mask: cv.typing.MatLike
        _croppedSelf: cv.typing.MatLike
        _croppedMask: cv.typing.MatLike

        _alphaChannel: cv.typing.MatLike
        _croppedAlphaChannel: cv.typing.MatLike
        _croppedAlphaChannelNormed: cv.typing.MatLike

        def __init__(self, resourceFullPath: str = ' ', separateMaskFullPath: str = ' '):

                if(resourceFullPath == ' '):
                        raise Exception("Resource location is not defined")

                try:
                        self._self = cv.imread(resourceFullPath, cv.IMREAD_GRAYSCALE)

                        if(separateMaskFullPath != ' '): resourceFullPath = separateMaskFullPath

                        self._alphaChannel = cv.imread(resourceFullPath, cv.IMREAD_UNCHANGED)[:,:,3]
                        self._mask = cv.merge([self._alphaChannel])
                except:
                        raise Exception("Could not read resource from given directory")

                # blurred = cv.bilateralFilter(self._self, 3, 500, 500)
                # blurred = self._self
                x, y, w, h = cv.boundingRect(self._self)
                self._croppedSelf = self._self[y:y + h, x:x + w]
                self._croppedMask = self._mask[y:y + h, x:x + w]
                self._croppedAlphaChannel = self._alphaChannel[y:y + h, x:x + w]
                self._croppedAlphaChannelNormed = self._croppedAlphaChannel / 255.0

                # cv.imshow("", self._croppedSelf)
                # cv.waitKeyEx(0)

class _PieceImg(_TempImg):
        """
                This class keeps a single chess piece information.
                _TempImg is used as the base class to also keep the image data in one place.
                Colour and type is also declared upon creation.
        """

        colour: int = PieceColourEnum.EMPTY
        type: int = PieceTypeEnum.EMPTY

        processedImgWhite: cv.typing.MatLike
        processedImgBlack: cv.typing.MatLike

        def __init__(self, colour: int = PieceColourEnum.EMPTY, pieceType: int = PieceTypeEnum.EMPTY):

                self.colour = colour
                self.type = pieceType

                super().__init__(self._GetResourceFullPath(colour, pieceType))

        def __call__(self): return (PieceColourEnum.Stringify(self.colour), PieceTypeEnum.Stringify(self.type))

        @staticmethod
        def _GetResourceFullPath(colour: int, pieceType: int):

                fullPath = r"resources\pieces"

                match colour:
                        case PieceColourEnum.WHITE: fullPath += r"\white"
                        case PieceColourEnum.BLACK: fullPath += r"\black"
                        case PieceColourEnum.EMPTY: fullPath += r"\empty"

                match pieceType:
                        case PieceTypeEnum.PAWN: fullPath += r"\p.png"
                        case PieceTypeEnum.KNIGHT: fullPath += r"\n.png"
                        case PieceTypeEnum.BISHOP: fullPath += r"\b.png"
                        case PieceTypeEnum.ROOK: fullPath += r"\r.png"
                        case PieceTypeEnum.QUEEN: fullPath += r"\q.png"
                        case PieceTypeEnum.KING: fullPath += r"\k.png"
                        case PieceTypeEnum.EMPTY: fullPath += r"\e.png"
                        case PieceTypeEnum.EMPTYDARK: fullPath += r"\ed.png"

                return fullPath

        def _SetupFinalImage(self, whiteTileImg: cv.typing.MatLike, blackTileImg: cv.typing.MatLike):
                """
                        This method setups images needed for square image comparisons.
                        These images also have square images as backgrounds for better results.
                """
                _whiteTileImg = whiteTileImg[0:self._croppedSelf.shape[0], 0:self._croppedSelf.shape[1]]
                _blackTileImg = blackTileImg[0:self._croppedSelf.shape[0], 0:self._croppedSelf.shape[1]]

                self.processedImgWhite = ((_whiteTileImg * (1.0 - self._croppedAlphaChannelNormed) + self._croppedSelf * self._croppedAlphaChannelNormed)).astype(np.uint8)
                self.processedImgBlack = ((_blackTileImg * (1.0 - self._croppedAlphaChannelNormed) + self._croppedSelf * self._croppedAlphaChannelNormed)).astype(np.uint8)
                # cv.imshow("", self.processedImgWhite)
                # cv.waitKeyEx(0)
                # cv.imshow("", self.processedImgBlack)
                # cv.waitKeyEx(0)


                pass

class _BoardImg(_TempImg):
        """
                This class loads the chessboard image using the given variable during creation.
                _TempImg is used as base class to simplify resource loading.
        """
        def __init__(self, resourceFullPath: str = ' ', separateMaskFullPath: str = ' '):
                super().__init__(resourceFullPath, separateMaskFullPath)

def _SetupPieceImgs():
        """
                This function initializes all pieces with their corresponding colours, types,
                and returns a 2D array (white, black) of all chess pieces also with their image resources.
        """
        pieceImgs = [[_PieceImg]]
        pieceImgs.pop(0)

        for x in range(2):
                pieceImgs.append([])
                for y in range(6):
                        pieceImgs[x].append(_PieceImg((x), (y)))

        pieceImgs.append([])
        pieceImgs[2].append(_PieceImg(PieceColourEnum.EMPTY, PieceTypeEnum.EMPTY))
        pieceImgs[2].append(_PieceImg(PieceColourEnum.EMPTY, PieceTypeEnum.EMPTYDARK))

        for x in range(2):
                for y in range(6):
                        pieceImgs[x][y]._SetupFinalImage(pieceImgs[2][0]._self, pieceImgs[2][1]._self)

        for x in range(len(pieceImgs)):
                for y in range(len(pieceImgs[x])):
                        print(PieceColourEnum.Stringify(pieceImgs[x][y].colour), PieceTypeEnum.Stringify(pieceImgs[x][y].type))

        # cv.imshow("", pieceImgs[2][0]._self)
        # cv.waitKeyEx(0)

        return pieceImgs

PieceImgs = _SetupPieceImgs()
BoardImg = _BoardImg(r"resources\board\greenboard.png", r"resources\board\greenboard_mask.png")


