from tools import gethex

hookshot = 2
candle = 4
greyK = 6
goldK = 8
shovel = 10
bell = 12
bridge = 14
listitems = [hookshot, candle, greyK, goldK, shovel, bell, bridge]

def itemtable():
    for i in listitems : gethex(i)

class infos:
    """
        This class is more of a tool for me. I will store my findings of infos here.
        And if I need to get an info during my coding, I'll simply call this class and then ask it to
        Retrieve the things I need.
    """




    def __init__(self):
        self.adresses = {
            hex(0x143) : "Item 1",
            hex(0x15D) : "Item 2 related to palette?",
            hex(0x15C) : "Item 2 related to sprite ID?,",
            hex(0x142) : "Item 2",
            hex(0x110) : "Xpos p1 (2b)",
            hex(0x113) : "Ypos p1 (2b)",
            hex(0xB6) : "world (1b)",
            hex(0xB7) : "lvl (1b)"
                    }
    def getadresses(self,*strings):
        liste = []