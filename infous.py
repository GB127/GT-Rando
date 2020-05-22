
nothing = 0
hookshot = 2
candle = 4
greyK = 6
goldK = 8
shovel = 10
bell = 12
bridge = 14
listitems = [hookshot, candle, greyK, goldK, shovel, bell, bridge, nothing]

def itemtable():
    for i in listitems : gethex(i)

class infos:
    """
        This class is more of a tool for me. I will store my findings of infos here.
        And if I need to get an info during my coding, I'll simply call this class and then ask it to
        Retrieve the things I need.
    """




    def __init__(self):
        self.infos = {
            hex(0x143) : "Item1 ID",
            hex(0x15A) : "Item1 display",
            hex(0x15B) : "Item1 display",
            hex(0x15D) : "Item2 display",
            hex(0x15C) : "Item2 display",
            hex(0x142) : "Item2 ID",
            hex(0x110) : "Xpos p1 (2b)",
            hex(0x113) : "Ypos p1 (2b)",
            hex(0xB6) : "world (1b)",
            hex(0xB7) : "lvl (1b)"
                    }
    def check(self,adress):
        if isinstance(adress,str):
            return adress + " : " + self.infos[adress]
        else:
            return hex(adress) + " : " + self.infos[hex(adress)]

    def listadresses(self,*seeked):
        print("-----------LIST OF ADRESSES-------------------")
        for i in list(self.infos):
            for key in seeked:
                if self.infos[i].count(key) > 0:
                    print(self.check(i))
        print("-----------END OF ADRESSES--------------------")
