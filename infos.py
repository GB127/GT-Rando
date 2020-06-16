from tools import gethex

# https://www.vgmaps.com/Atlas/SuperNES/index.htm#GoofTroop

"""
    Start at Stage 2	Banana - Red Diamond - Cherry - Banana - Cherry
    Start at Stage 3	Cherry - Red Diamond - Blue Diamond - Cherry - Banana
    Start at Stage 4	Red Diamond - Cherry - Blue Diamond - Blue Diamond - Red Diamond
    Start at Stage 5	Banana - Cherry - Blue Diamond - Red Diamond - Banana
"""




"""
i = world
j = niveau
base = Read_Byte(0x83F303 + i)
addr = Read_Word(0x83F303 + base + 2*j)
tu vas toruver toutes les infos sur le prochain niveau à loader dans les adresses suivantes:
Read_Byte(addr + 0)
Read_Byte(addr + 1)
Read_Byte(addr + 3)
Read_Byte(addr + 4)
Read_Byte(addr + 5)





[3:19 PM] PsychoManiac: The routine at $80:B631 loads the collision tiles
[3:20 PM] PsychoManiac: There are two layers, the lower layers is saved for when something is removed from the upper layer
[3:20 PM] PsychoManiac: This routine also calls $82:C235, which loads the exits for the screen you are

[6:54 AM] PsychoManiac: It specifies how the exit's collision tiles are laid down
[6:54 AM] PsychoManiac: If bit 6 is set (0x20) then it is a vertical line, otherwise it is horizontal or 2x2
[6:55 AM] PsychoManiac: If bit 6 is not set and bits 1-4 are 0x0F, then the exit is 2x2 (x,y) (x+1,y) (x,y+1) and (x+1,y+1)
[6:55 AM] PsychoManiac: For horizontal or vertical lines, bits 1-4 specify the length and bit 5 says if it is 1 or 2 tiles thick.


"""






class InfosError(BaseException):
    pass
class infos:
    """
        This class is more of a tool for me. I will store my findings of infos here.
        And if I need to get an info during my coding, I'll simply call this class and then ask it to
        Retrieve the things I need.
    """
    def introtext_range(self):
        for i in range(0x1D450,0x1D4BD):
            print(hex(i))

    def boss0_text(self):
        for i in range(0x5F87B, 0x5F8B8):
            print(hex(i))

    def passwordrange(self):
        for i in range(0x1C67F, 0x1C692 +1) :
            print(f"game[{hex(i)}]")

    def dark_rooms_range(self):
        print("worlds - level")
        for i in range(0x186B5, 0x186BF+1):
            print(f'{hex(i)} - {hex(i+1)}')

    def itemids(self, id=None, adjust=0):
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

    def level_items(self):
        # These are the actual values that the game will need to select the items.
        # For placing them in the levels
        print("Hookshot : 8")
        print("Candle : 9")
        print("Grey Key : A")
        print("Gold Key : B")
        print("Shovel : C")
        print("Bell : D")
        print("Bridge : E")

    def range_World_Item(self, world=None):
        end = {0:0x1164,
               1:0x1165,
               2:0x116A,
               3:0x1163,
               4:0x1168}
        if world in range(5):
            print(f'World {world} range location : {hex(0x1160)} - {hex(end[world])}')
            return (0x1160, end[world])
        elif world is None:
            for i in end.keys():
                print(f'World {i} range location : {hex(0x1160)} - {hex(end[i])}')
            return
        else:
            raise InfosError("The world can only be a value of [0-1-2-3-4-None]")

    def __init__(self):
        self.infos = {
            # When searching for a keyword, always use a capital for the first letter.

            hex(0xB6) : "current World (1b)",
            hex(0xB7) : "current Level (1b)",
            hex(0xBD) : "P # playing : 1 if 1P, 3 if 2P",


            # Item
            hex(0x140) : "Item P1 check : 2 if has 2 items, else 0",
            hex(0x142) : "Item P1 selected : left = 0, right = 2",
            hex(0x143) : "Item1 ID : infos.itemids()",
            hex(0x142) : "Item2 ID : infos.itemids()",
            hex(0x15A) : "Item1 display",
            hex(0x15B) : "Item1 display",
            hex(0x15D) : "Item2 display",
            hex(0x15C) : "Item2 display",


            # P1
                # Related to P1
            hex(0x11D) : "P1 Hearts",
            hex(0x157) : "P1 Lives",
            hex(0x110) : "Xpos P1 (2b)",
            hex(0x113) : "Ypos P1 (2b)",

            hex(0x1144) : "Doors locking related",
            hex(0x140B) : "Level's Item : infos.items(2)",
                # Note : the items are always -2. 
                # For example : the bell will be 10 (or A).

            # Password box
            hex(0x230) : "Password box 1: Cherry = 00, Banana = 01, Red Gem = 02, Blue Gem = 03",
            hex(0x231) : "Password box 2: Cherry = 00, Banana = 01, Red Gem = 02, Blue Gem = 03",
            hex(0x232) : "Password box 3: Cherry = 00, Banana = 01, Red Gem = 02, Blue Gem = 03",
            hex(0x233) : "Password box 4: Cherry = 00, Banana = 01, Red Gem = 02, Blue Gem = 03",
            hex(0x234) : "Password box 5: Cherry = 00, Banana = 01, Red Gem = 02, Blue Gem = 03",


            # Stored items for the World
                # See world_ranges()
                    # The idea is that some levels will take the first "letter", some will take the second letters.
                    # For example, if the byte read is 0xAC:
                        # One level that read this specific byte will read A and thus will fetch a Grey Key.
                        # The other level that read the same byte will read C and will fetch the Shovel.
                hex(0x1160) : "World Item 1&2",
                hex(0x1161) : "World Item 3&4",
                hex(0x1162) : "World Item 5&6",
                hex(0x1163) : "World Item 7&8",
                hex(0x1164) : "World Item 9&10",
                hex(0x1165) : "World Item 11&12",
                hex(0x1166) : "World Item 13&14",
                hex(0x1167) : "World Item 15&16",
                hex(0x1168) : "World Item 17&18",
                hex(0x1169) : "World Item 19&20",
                hex(0x116A) : "World Item 21&22",

            # World 0's items.
                hex(0x6F69): "0-X : Item",
                hex(0x6F72): "0-X : Item",
                hex(0x6F77): "0-X : Item",
                hex(0x6F7C): "0-X : Item",
                hex(0x6F8D): "0-X : Item",
                hex(0x6F9F): "0-X : Item",
                hex(0x6FB1): "0-X : Item",
                hex(0x6FC3): "0-X : Item",
                hex(0x6FCC): "0-X : Item",
                hex(0x6FDD): "0-X : Item",

            # World 1:
                hex(0x7013): "1-X : Item",
                hex(0x7018): "1-X : Item",
                hex(0x701C): "1-X : Item",
                hex(0x7022): "1-X : Item",
                hex(0x7027): "1-X : Item",
                hex(0x702B): "1-X : Item",
                hex(0x7034): "1-X : Item",
                hex(0x7038): "1-X : Item",
                hex(0x7043): "1-X : Item",
                hex(0x7048): "1-X : Item",
                hex(0x7050): "1-X : Item",
                hex(0x7055): "1-X : Item",

            # World 2
                hex(0x7072): "2-X : Item",
                hex(0x7077): "2-X : Item",
                hex(0x707C): "2-X : Item",
                hex(0x7080): "2-X : Item",
                hex(0x7084): "2-X : Item",
                hex(0x708E): "2-X : Item",
                hex(0x7092): "2-X : Item",
                hex(0x70BA): "2-X : Item",
                hex(0x70BE): "2-X : Item",
                hex(0x70C2): "2-X : Item",
                hex(0x70CC): "2-X : Item",
                hex(0x70D6): "2-X : Item",
                hex(0x70DB): "2-X : Item",
                hex(0x70E0): "2-X : Item",
                hex(0x70E5): "2-X : Item",
                hex(0x70EB): "2-X : Item",
                hex(0x70EF): "2-X : Item",
                hex(0x70F5): "2-X : Item",
                hex(0x70FD): "2-X : Item",
                hex(0x7101): "2-X : Item",
                hex(0x7107): "2-X : Item",

            # World 3:
                hex(0x7122): "3-X : Item",
                hex(0x7126): "3-X : Item",
                hex(0x7171): "3-X : Item",
                hex(0x719D): "3-X : Item",
                hex(0x71A6): "3-X : Item",

            # World 4:
                hex(0x71D2) : "4-X : Item",
                hex(0x71E2) : "4-X : Item",
                hex(0x71EA) : "4-X : Item",
                hex(0x71F8) : "4-X : Item",
                hex(0x71FC) : "4-X : Item",
                hex(0x720B) : "4-X : Item",
                hex(0x720F) : "4-X : Item",
                hex(0x721D) : "4-X : Item",
                hex(0x7221) : "4-X : Item",
                hex(0x7225) : "4-X : Item",
                hex(0x723A) : "4-X : Item",
                hex(0x7260) : "4-X : Item",
                hex(0x7264) : "4-X : Item",
                hex(0x726D) : "4-X : Item",
                hex(0x7272) : "4-X : Item",
                hex(0x727C) : "4-X : Item",
                hex(0x7297) : "4-X : Item",
                hex(0x729B) : "4-X : Item"
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
