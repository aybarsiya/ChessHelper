from Enums import PieceTypeEnum, PieceColourEnum
import cv2 as cv

class Piece():
        
        type: int
        colour: int
        
        def __init__(self, pieceType = PieceTypeEnum.EMPTY, pieceColour = PieceColourEnum.EMPTY):
                self.type = pieceType
                self.colour = pieceColour
        
        def __call__(self): return (PieceTypeEnum.Stringify(self.type), PieceColourEnum.Stringify(self.colour))

class Square():
        
        piece: Piece
        img: cv.typing.MatLike
        
        def __init__(self, piece: Piece = Piece()):
                self.piece = piece
                pass
        

class Chessboard():
        _squares = [[Square]]
        
        
        def __init__(self):
                
                for i in range(8):
                        self._squares.append([])
                        for k in range(8):
                                self._squares[i].append(Square())
                                print(i, k)
                
                for i in range(len(self._squares)):
                        for k in range(len(self._squares[i])):
                                print(self._squares[i][k])
                                print(i, k)
                
                self._squares.pop(0)


CB = Chessboard()
CB._squares[0][0].piece = Piece(PieceTypeEnum.BISHOP, PieceColourEnum.BLACK)
print(CB._squares[0][0].piece())