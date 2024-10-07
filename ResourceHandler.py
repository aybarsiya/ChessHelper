import cv2 as cv
from Enums import PieceTypeEnum, PieceColourEnum

class _TempImg():

        _self: cv.typing.MatLike
        _mask: cv.typing.MatLike

        def __init__(self, resourceFullPath: str = ' ', separateMaskFullPath: str = ' '):

                if(resourceFullPath == ' '):
                        raise Exception("Resource location is not defined")

                try:
                        self._self = cv.imread(resourceFullPath, cv.IMREAD_GRAYSCALE)

                        if(separateMaskFullPath != ' '): resourceFullPath = separateMaskFullPath
                        self._mask = cv.merge([cv.imread(resourceFullPath, cv.IMREAD_UNCHANGED)[:,:,3]])
                except:
                        raise Exception("Could not read resource from given directory")

class _PieceImg(_TempImg):

        colour: int = PieceColourEnum.EMPTY
        type: int = PieceTypeEnum.EMPTY

        def __init__(self, colour: int = PieceColourEnum.EMPTY, pieceType: int = PieceTypeEnum.EMPTY):

                if(not(colour > PieceColourEnum.EMPTY and colour <= PieceColourEnum.BLACK) or not(pieceType > PieceTypeEnum.EMPTY and pieceType <= PieceTypeEnum.KING)):
                        raise Exception("Colour or type of piece is not defined properly")

                self.colour

                super().__init__(self._GetResourceFullPath(colour, pieceType))

        @staticmethod
        def _GetResourceFullPath(colour: int, pieceType: int):

                fullPath = r"resources\pieces"

                match colour:
                        case 1: fullPath += r"\white"
                        case 2: fullPath += r"\black"

                match pieceType:
                        case 1: fullPath += r"\p.png"
                        case 2: fullPath += r"\n.png"
                        case 3: fullPath += r"\b.png"
                        case 4: fullPath += r"\r.png"
                        case 5: fullPath += r"\q.png"
                        case 6: fullPath += r"\k.png"

                return fullPath

class _BoardImg(_TempImg):

        def __init__(self, resourceFullPath: str = ' ', separateMaskFullPath: str = ' '):
                super().__init__(resourceFullPath, separateMaskFullPath)

def _SetupPieceImgs():

        pieceImgs = [[_PieceImg]]
        pieceImgs.pop(0)

        for x in range(2):
                pieceImgs.append([])
                for y in range(6):
                        pieceImgs[x].append(_PieceImg((x + 1), (y + 1)))

        return pieceImgs

PieceImgs = _SetupPieceImgs()
BoardImg = _BoardImg(r"resources\board\greenboard.png", r"resources\board\greenboard_mask.png")