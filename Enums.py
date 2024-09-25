from enum import Enum

class Piece(Enum):
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
        
MS_PER_FRAME = 16.6