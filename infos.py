from tools import gethex

# https://www.vgmaps.com/Atlas/SuperNES/index.htm#GoofTroop
class infos:
    """
        This class is more of a tool for me. I will store my findings of infos here.
        And if I need to get an info during my coding, I'll simply call this class and then ask it to
        Retrieve the things I need.
    """
    def itemids(self):
        nothing = 0
        hookshot = 2
        candle = 4
        greyK = 6
        goldK = 8
        shovel = 10
        bell = 12
        bridge = 14
        listitems = [hookshot, candle, greyK, goldK, shovel, bell, bridge, nothing]
        for i in listitems : gethex(i)

    def __init__(self):
        self.infos = {
            hex(0x143) : "item1 ID",
            hex(0x15A) : "item1 display",
            hex(0x15B) : "item1 display",
            hex(0x15D) : "item2 display",
            hex(0x15C) : "item2 display",
            hex(0x142) : "item2 ID",
            hex(0x110) : "Xpos P1 (2b)",
            hex(0x113) : "Ypos P1 (2b)",
            hex(0xB6) : "world (1b)",
            hex(0xB7) : "lvl (1b)",
            hex(0x140B) : "Level's Item.",
                # Note : This is always -2 from the "normal item ID".
                # For example : the bell will be 10.
            hex(0x11D) : "P1 Hearts",
            hex(0x157) : "P1 lives",
            hex(0x1144) : "Doors locking related"
                    }
            
    def check(self,adress):
        if isinstance(adress,str):
            return adress + " : " + self.infos[adress]
        else:
            return hex(adress) + " : " + self.infos[hex(adress)]

    def listadresses(self,*seeked):
        print("-----------LIST OF ADRESSES-------------------")
        for i in list(self.infos):
            if all(x in self.infos[i] for x in seeked):
                print(self.check(i))
        print("-----------END OF ADRESSES--------------------")
