"""
        Chessboard Module

        This module is responsible for initializing and keeping track of a Chessboard object.

        Aybars Ay
        2024
"""

from Enums import PieceTypeEnum, PieceColourEnum
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
        _squares = [[_Square]]


        def __init__(self):

                self._squares.pop(0)

                for i in range(8):
                        self._squares.append([])
                        for k in range(8):
                                self._squares[i].append(_Square())

                # self.PrintChessBoard()

        def PrintChessBoard(self):
                for i in range(len(self._squares)):
                        for k in range(len(self._squares[i])):
                                print(self._squares[i][k].piece())
                                print(i, k)