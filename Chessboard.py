from Enums import Piece, Colour

class Chessboard:
        _initialized = bool(0)
        
        
        def __init__(self):
                
                
                
                self._initialized = bool(1)

class Square:
        piece = Piece.EMPTY.value
        colour = Colour