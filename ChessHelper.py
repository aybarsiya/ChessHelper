"""
    This is the main class of the whole program. Main loops are initialized and handled here.
"""
import asyncio as aio

class ChessHelper:
        """
                This is the main controller object of the whole program.
                It keeps the necessary classes' references, in order to make the necessary actions and calculations.
        """
        from MenuHandler import MenuHandler
        from Getch import Getch
        
        MH = MenuHandler()
        
        
        async def Controller(self):
                
                
                pass
        
        
        async def PlayMode(self):
                """
                        This async function handles the operations while playing a chess game.
                        
                """
                import Chessboard
                
                
                pass

"""
        We run the ChessHelper program here.
"""
CH = ChessHelper()
with aio.Runner() as runner:
    runner.run(CH.Controller())