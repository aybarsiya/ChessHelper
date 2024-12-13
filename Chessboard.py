"""
        Chessboard Module

        This module is responsible for initializing and keeping track of a Chessboard object.

        Aybars Ay
        2024
"""

from operator import le
from Enums import PieceTypeEnum, PieceColourEnum
from ResourceHandler import BoardImg, PieceImgs
import cv2 as cv

from ScreenHandler import SH

class _Piece():

        colour: int
        type: int

        def __init__(self, pieceColour = PieceColourEnum.EMPTY, pieceType = PieceTypeEnum.EMPTY):
                self.colour = pieceColour
                self.type = pieceType

        def __call__(self): return (PieceColourEnum.Stringify(self.colour), PieceTypeEnum.Stringify(self.type))

class _Square():

        piece: _Piece
        img: cv.typing.MatLike

        def __init__(self, piece: _Piece = _Piece()):
                self.piece = piece
                pass

        def DeterminePiece(self, scale: float, algoScale: float, black: bool):

                bestResult = 0.0
                bestColour = 0.0
                bestType = 0.0

                i = 0
                if(black): i = 1

                result = SH._GetBestValues(
                                                                                self.img,
                                                                                PieceImgs[2][i]._croppedSelf,
                                                                                )[0]

                if(result > 0.989):
                        return

                imgToCompare: cv.typing.MatLike



                for y in range(5):
                        for x in range(2):


                                if(black): imgToCompare = PieceImgs[x][y + 1].processedImgBlack
                                else: imgToCompare = PieceImgs[x][y + 1].processedImgWhite


                                result = SH._GetBestValues(
                                                                                                self.img,
                                                                                                imgToCompare,
                                                                                                )[0]

                                print(result, PieceColourEnum.Stringify(x), PieceTypeEnum.Stringify(y + 1))

                                if(result > 0.9 and result > bestResult and (bestResult + ((bestResult / 100) / 2)) < result):
                                        bestResult = result
                                        bestColour = x
                                        bestType = y + 1

                                        print("-----------------found piece", PieceColourEnum.Stringify(x), PieceTypeEnum.Stringify(y + 1))

                for x in range(2):

                        if(black): imgToCompare = PieceImgs[x][0].processedImgBlack
                        else: imgToCompare = PieceImgs[x][0].processedImgWhite

                        result = SH._GetBestValues(
                                                                                # scale,
                                                                                self.img,
                                                                                imgToCompare,
                                                                                # PieceImgs[x][0]._croppedMask,
                                                                                )[0]

                        print(result)

                        if(x == 0):
                                if(result > 0.985 and result > bestResult):
                                        #  and (bestResult + ((bestResult / 100) / 4)) > result
                                        bestResult = result
                                        bestColour = x
                                        bestType = 0

                                        print("-----------------found pawn", PieceColourEnum.Stringify(x), PieceTypeEnum.Stringify(0))
                        else:
                                if(result > 0.965 and result > bestResult):
                                        #  and (bestResult + ((bestResult / 100) / 4)) > result
                                        bestResult = result
                                        bestColour = x
                                        bestType = 0

                                        print("-----------------found pawn", PieceColourEnum.Stringify(x), PieceTypeEnum.Stringify(0))

                print(bestResult)
                self.piece = _Piece(bestColour, bestType)

        def DetPieces():




                pass


class Chessboard():

        squares = [[_Square]]

        img: cv.typing.MatLike = None

        scale: float = 0.0
        algoScale: float = 0.0
        pos: tuple[int, int] = (int(0), int(0))

        def __init__(self, img: cv.typing.MatLike, scale: float, pos: tuple[int, int], algoScale: float):

                self.squares.pop(0)

                for i in range(8):
                        self.squares.append([])
                        for k in range(8):
                                self.squares[i].append(_Square())

                # self.PrintChessBoard()

                # img = cv.bilateralFilter(img, 3, 80, 80)
                img = SH._GetUpscaledImg(img, scale)

                self.SetImg(img)
                self.scale = scale
                self.algoScale = algoScale
                self.pos = pos

                self.SetPieceImgs()

        def PrintChessBoard(self):
                for i in range(len(self.squares)):
                        for k in range(len(self.squares[i])):
                                print(self.squares[i][k].piece())
                                print(i, k)

        def SetImg(self, img: cv.typing.MatLike):

                if((round(img.shape[:2][0] % 8) != 0) or (img.shape[:2][0] != img.shape[:2][1])):
                        print(img.shape[:2])
                        raise Exception("Chessboard image is not correctly sized! (side % 8 > 0 OR side[0] != side[1])")

                self.img = img

        def SetPieceImgs(self):
                squareWidth = round(self.img.shape[:2][0] / 8)
                for i in range(8):
                        for k in range(8):
                                self.squares[i][k].img = self.img[(i * squareWidth):((i + 1) * squareWidth), (k * squareWidth):((k + 1) * squareWidth)]

        def DeterminePieces(self):
                black = False
                for i in range(len(self.squares)):
                        for k in range(len(self.squares[i])):
                                self.squares[i][k].DeterminePiece(self.scale, self.algoScale, black)
                                print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,", self.squares[i][k].piece())
                                black = not black