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

        def DeterminePiece(self, scale: float, algoScale: float):

                # scale -= 0.5
                # scale = algoScale

                bestResult = 0.0
                bestColour = 0.0
                bestType = 0.0

                for i in range(2):
                        result = SH._GetBestValues(
                                                                                        # scale,
                                                                                        self.img,
                                                                                        PieceImgs[2][i]._croppedSelf,
                                                                                        )[0]

                        if(result > bestResult and result > 0.995):
                                bestResult = result
                                bestColour = 2
                                bestType = i

                if(bestResult != 0.0):
                        return

                for x in range(2):
                        for y in range(5):



                                result = SH._GetBestValues(
                                                                                                # scale,
                                                                                                self.img,
                                                                                                PieceImgs[x][y + 1]._croppedSelf,
                                                                                                PieceImgs[x][y + 1]._croppedMask,
                                                                                                )[0]

                                print(result, PieceColourEnum.Stringify(x), PieceTypeEnum.Stringify(y + 1))

                                if(result > bestResult and (bestResult + ((bestResult / 100) / 4)) < result):
                                        bestResult = result
                                        bestColour = x
                                        bestType = y + 1

                                        print("-----------------found piece", PieceColourEnum.Stringify(x), PieceTypeEnum.Stringify(y + 1))

                for x in range(2):
                        result = SH._GetBestValues(
                                                                                # scale,
                                                                                self.img,
                                                                                PieceImgs[x][0]._croppedSelf,
                                                                                PieceImgs[x][0]._croppedMask,
                                                                                )[0]

                        print(result)
                        if(result > 0.895 and result > bestResult):
                                #  and (bestResult + ((bestResult / 100) / 4)) > result
                                bestResult = result
                                bestColour = x
                                bestType = 0

                                print("-----------------found pawn", PieceColourEnum.Stringify(x), PieceTypeEnum.Stringify(0))

                print(bestResult)
                self.piece = _Piece(bestColour, bestType)


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
                for i in range(len(self.squares)):
                        for k in range(len(self.squares[i])):
                                self.squares[i][k].DeterminePiece(self.scale, self.algoScale)
                                print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,", self.squares[i][k].piece())