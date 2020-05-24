from tools import gethex

# https://www.vgmaps.com/Atlas/SuperNES/index.htm#GoofTroop

"""
    Start at Stage 2	Banana - Red Diamond - Cherry - Banana - Cherry
    Start at Stage 3	Cherry - Red Diamond - Blue Diamond - Cherry - Banana
    Start at Stage 4	Red Diamond - Cherry - Blue Diamond - Blue Diamond - Red Diamond
    Start at Stage 5	Banana - Cherry - Blue Diamond - Red Diamond - Banana
"""
class InfosError(BaseException):
    pass
class infos:
    """
        This class is more of a tool for me. I will store my findings of infos here.
        And if I need to get an info during my coding, I'll simply call this class and then ask it to
        Retrieve the things I need.
    """
    def itemids(self, id=None, adjust=2):
        # The adjust is because the items displayed on the levels are
        # always -2. For example, in inventory, the bell is 12. On the
        # level, it will be 10.
        items = {"Hookshot" : 2,
        "Candle" : 4,
        "Grey Key" : 6,
        "Gold Key" : 8,
        "Shovel" : 10,
        "Bell" : 12,
        "Bridge" : 14}
        if id is None:
            print("-" * 20)
            for i in items.keys() :
                print(i)
                gethex(items[i] -adjust)
            print("-" * 20)
        else:
            for i in items.keys():
                if id == items[i] -adjust:
                    print(i)
                    return

    def level_items(self,type=None):
        print("Nothing : 0")
        print("Hookshot : 8")
        print("Candle : 9")
        print("Grey Key : A")
        print("Gold Key : B")
        print("Shovel : C")
        print("Bell : D")
        print("Bridge : E")
        # The idea is that some levels will take the first "letter", some will take the second letters.
        # For example, if the byte read is 0xAC:
            # One level that read this specific byte will read A and thus will fetch a Grey Key.
            # The other level that read the same byte will read C and will fetch the Shovel.
    def world_ranges(self):
        # These are the vanilla ranges of bytes the world read from.
        print("World 1 : 0x88160 - 0x1164")
        print("World 2 : 0x88160 - 0x1165")
        print("World 3 : 0x88160 - 0x116A")
        print("World 4 : 0x88160 - 0x1163")
        print("World 5 : 0x88160 - 0x1168")

    def __init__(self):
        self.infos = {
            hex(0x143) : "item1 ID : infos.itemids(2)",
            hex(0x15A) : "item1 display",
            hex(0x15B) : "item1 display",
            hex(0x15D) : "item2 display",
            hex(0x15C) : "item2 display",
            hex(0x142) : "item2 ID : infos.itemids(2)",
            hex(0x110) : "Xpos P1 (2b)",
            hex(0x113) : "Ypos P1 (2b)",
            hex(0xB6) : "world (1b)",
            hex(0xB7) : "lvl (1b)",
            hex(0x140B) : "Level's Item : infos.itemds(), infos.items140B",
                # Note : the items are always -2. 
                # For example : the bell will be 10 (or A).
            hex(0x11D) : "P1 Hearts",
            hex(0x157) : "P1 lives",
            hex(0x1144) : "Doors locking related",
            hex(0xBD) : "P # playing : 1 if 1P, 3 if 2P",
            hex(0x140) : "Item P1 check : 2 if has 2 items, else 0",
            hex(0x142) : "Item p1 selected : left = 0, right = 2"
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
