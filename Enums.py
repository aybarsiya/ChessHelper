from enum import Enum

class _Piece(Enum):
        EMPTY = 0
        PAWN = 1
        KNIGHT = 2
        BISHOP = 3
        ROOK = 4
        QUEEN = 5
        KING = 6
        
        @classmethod
        def _missing_(cls, value):
                return cls.EMPTY

class _Colour(Enum):
        EMPTY = 0
        WHITE = 1
        BLACK = 2
        
        @classmethod
        def _missing_(cls, value):
                return cls.EMPTY

Piece = _Piece
Colour = _Colour

MS_PER_FRAME = 16.6