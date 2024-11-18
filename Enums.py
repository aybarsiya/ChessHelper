"""
        Enums Module

        This module is responsible for keeping enum values which are commonly used throughout the main program's modules.

        Aybars Ay
        2024
"""

class _Piece():
        EMPTYDARK = -2
        EMPTY = -1
        PAWN = 0
        KNIGHT = 1
        BISHOP = 2
        ROOK = 3
        QUEEN = 4
        KING = 5

        def Stringify(toStringify: int) -> str:
                match toStringify:
                        case 0: return "PAWN"
                        case 1: return "KNIGHT"
                        case 2: return "BISHOP"
                        case 3: return "ROOK"
                        case 4: return "QUEEN"
                        case 5: return "KING"
                        case _: return "EMPTY"


class _Colour():
        EMPTY = -1
        WHITE = 0
        BLACK = 1

        def Stringify(toStringify: int) -> str:
                match toStringify:
                        case 0: return "WHITE"
                        case 1: return "BLACK"
                        case _: return "EMPTY"


PieceTypeEnum = _Piece
PieceColourEnum = _Colour

MS_PER_FRAME = 16.6