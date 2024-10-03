"""
    This is the main class of the whole program. Main loops are initialized and handled here.
"""

import asyncio
from Singleton import *


class Main(Singleton):        
        teststring = "test"
        
        def testing(self):
                self.teststring = "test2"
        
                print(self.teststring)
                
        def testing2(self):
                print(self.teststring)
                
        def testing3(self):
                self.teststring = "test3"
                
                
        

m = Main()
n = Main()

m.testing()
n.testing2()
n.testing3()
m.testing2()

print(m)
print(n)
print(m == n)
print(type(m))

class ChessHelper:
        """
                This is the main controller object of the whole program.
                It keeps the necessary subclasses in order to make the necessary actions and calculations.
        """