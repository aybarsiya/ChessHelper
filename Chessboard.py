"""
        Chessboard Module

        This module is responsible for initializing and keeping track of a Chessboard object.

        Aybars Ay
        2024
"""

from Enums import PieceTypeEnum, PieceColourEnum
from ResourceHandler import BoardImg
import cv2 as cv

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


class Chessboard():

        squares = [[_Square]]

        img: cv.typing.MatLike = None

        scale: float = 0.0
        boxCoords: tuple[int, int, int, int] = (int(0), int(0), int(0), int(0))

        def __init__(self):

                self.squares.pop(0)

                for i in range(8):
                        self.squares.append([])
                        for k in range(8):
                                self.squares[i].append(_Square())

                # self.PrintChessBoard()

        def PrintChessBoard(self):
                for i in range(len(self.squares)):
                        for k in range(len(self.squares[i])):
                                print(self.squares[i][k].piece())
                                print(i, k)

        def SetImg(self, img: cv.typing.MatLike):

                if((round(img.shape[:2][0] % 8) != 0) or (img.shape[:2][0] != img.shape[:2][1])):
                        raise Exception("Chessboard image is not correctly sized! (side % 8 > 0 OR side[0] != side[1])")

                self.img = img

                squareWidth = round(self.img.shape[:2][0] / 8)
                for i in range(8):
                        for k in range(8):
                                self.squares[i][k].img = self.img[(i * squareWidth):((i + 1) * squareWidth), (k * squareWidth):((k + 1) * squareWidth)]
