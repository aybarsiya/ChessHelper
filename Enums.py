"""
        Enums Module

        This module is responsible for keeping enum values which are commonly used throughout the main program's modules.

        Aybars Ay
        2024
"""

class _Piece():
        EMPTY = 0
        PAWN = 1
        KNIGHT = 2
        BISHOP = 3
        ROOK = 4
        QUEEN = 5
        KING = 6

        def Stringify(toStringify: int) -> str:
                match toStringify:
                        case 1: return "PAWN"
                        case 2: return "KNIGHT"
                        case 3: return "BISHOP"
                        case 4: return "ROOK"
                        case 5: return "QUEEN"
                        case 6: return "KING"
                        case _: return "EMPTY"


class _Colour():
        EMPTY = 0
        WHITE = 1
        BLACK = 2

        def Stringify(toStringify: int) -> str:
                match toStringify:
                        case 1: return "WHITE"
                        case 2: return "BLACK"
                        case _: return "EMPTY"


PieceTypeEnum = _Piece
PieceColourEnum = _Colour

MS_PER_FRAME = 16.6