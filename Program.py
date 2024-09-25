"""
    This is the main class of the whole program. Main loops are initialized and handled here.
"""

import asyncio
from Singleton import Singleton

@Singleton
class Main:
    teststring = "test"
    
    def __init__(self):
        self.teststring = "test1"
            
        print(self.teststring)
            
    def testing(self):
        self.teststring = "test2"
        
        print(self.teststring)

m = Main()