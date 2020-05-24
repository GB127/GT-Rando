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

    def leveltypes_vs_items(self,type=None):
        if type is None:
            raise InfosError("You need to select a level type")
        if type is "A":
            print("Hookshot : 88\nCandle : 98\nGrey Key : A8\nGold Key : B8\nShovel : C8\nBell : D8\nBridge : E8")
        if type is "B":
            print("Hookshot : 8\nCandle : 9\nGrey Key : A\nGold Key : B\nShovel : C\nBell : D\nBridge : E")

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
            hex(0x140B) : "Level's Item.",
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
