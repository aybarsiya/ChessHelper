from threading import Thread
from time import sleep
from tkinter import Menu

class _Row():
        string = ""
        isCallable = False
        func: object

        def __init__(self, string: str = "", func: object = None):

                if(len(string) < 1):
                        print("Row string is not defined")
                        return

                self.string = string

                if(func != None):
                        self.func = func
                        self.isCallable = True

class _MainMenu():

        rows = [_Row()]
        def __init__(self):
                self.rows.pop(0)
                self.rows.append(_Row("Welcome to ChessHelper!\n---------------"))
                self.rows.append(_Row("Press enter to continue", self.test))

        def test(self):
                print("WHOOOOOOO")
        pass

class MenuHandler():

        cursorPos = 0
        mainMenu = _MainMenu()

        def loop(self):
                from InputHandler import IH

                for i in range(len(self.mainMenu.rows)):
                        print(self.mainMenu.rows[i].string)

                while(True):
                        sleep(0.16)

                        if(IH.update):
                                print("ohaaaa")
                                Thread(target = self.mainMenu.rows[1].func).start()




        pass

MH = MenuHandler()