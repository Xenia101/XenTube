from typing import *
import os

class Checking:
    def __init__(self, URL, PATH):
        if len(URL) is 0 or len(PATH) is 0:
            raise ValueError("URL or PATH is none")
        
        self.URL :str = URL
        self.PATH:str = PATH
        
        super().__init__()
        
    def dircheck(self):
        return os.path.isdir(self.PATH)

    def dircreate(self):
        try:
            os.makedirs(self.PATH)
        except OSError:
            print("[Error] Creathing directory : {}".format(self.PATH))
            return 0
        
    def check(self):
        if self.dircheck() is True:
            return True
        else:
            return False