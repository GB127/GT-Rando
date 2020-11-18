"""
    [3:19 PM] PsychoManiac: The routine at $80:B631 loads the collision tiles
    [3:20 PM] PsychoManiac: There are two layers, the lower layers is saved for when something is removed from the upper layer
    [3:20 PM] PsychoManiac: This routine also calls $82:C235, which loads the exits for the screen you are
"""

class InfosError(BaseException):
    pass
class infos:
    """
        This class is more of a tool for me. I will store my findings of infos here.
        And if I need to get an info during my coding, I'll simply call this class and then ask it to
        Retrieve the things I need.
    """

    def __init__(self):
        self.infos = {
            # When searching for a keyword, always use a capital for the first letter.
            # general
                hex(0xB6) : "current World (1b)",
                hex(0xB7) : "current Level (1b)",
                hex(0xBD) : "Player count : 1 if 1P, 3 if 2P",
                hex(0xF0) : "Current world 'milliseconds'",
                hex(0xF1) : "Current world seconds",
                hex(0xF2) : "Current world minutes",
                hex(0xF3) : "Current world hours (Max value is 9!)",
                hex(0xF5) : "Total Seconds played",
                hex(0xF6) : "Total Minutes played",
                hex(0xF7) : "Total Hours played",

                hex(0x21C) : "Current(?) boss HP",
                hex(0x21D) : "Current(?) boss HP",

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

            hex(0x1144) : "Doors unlocked",
            hex(0x1145) : "Doors unlocked",  # Perhaps 1146? Will have to test further
            hex(0x140B) : "Level's Item : infos.items(2)",
                # Note : the items are always -2. 
                # For example : the bell will be 10 (or A).

            # Credits
                hex(0x1414F) : "Credits : Speed of the THE END Credits",
                hex(0x14137) : "Credits : Where the THE END should stop if password used",




            hex(0x10C) : "Player on correct level?"
        }


    def maps(self):
        print("https://www.vgmaps.com/Atlas/SuperNES/index.htm#GoofTroop")

    def range_dynamic_passwords(self):
        return [x for x in range(0x230, 0x235)]

    def range_credits(self):
        print(f' Vanilla credits : {hex(0x5F99E)} - {hex(0x5FBFF)}')

    def format_credits_line(self, verbose=False):
        print("[Vspac][Hspac][#][Col][...letters...]")
        if verbose:
            print("Byte 1   : Vspac : Vertical spacing")
            print("Byte 2   : Hspac : Horizontal spacing")
            print("Byte 3   : #     : How many letters to fetch for the line")
            print("Byte 4   : Col   : Color / Properties (see add_credits for more infos)")
            print("Bytes 5+ : The following bytes are the letters")

    def range_World_dynamic_Items(self, world=None):
        """Returns a string showing the range of addresses that stores the items of a said world.
            If no world is selected, it will print all worlds.

            Args:
                world ([int], optional): World selected. Defaults to None.

            Raises:
                InfosError: Make sure the world is only 0-1-2-3-4 or None.
            """
        end = {0:0x1164,
               1:0x1165,
               2:0x116A,
               3:0x1163,
               4:0x1168}
        if world in range(5):
            print(f'World {world} range location : {hex(0x1160)} - {hex(end[world])}')
        elif world is None:
            for i in end.keys():
                print(f'World {i} range location : {hex(0x1160)} - {hex(end[i])}')
        else:
            raise InfosError("The world can only be a value of [0-1-2-3-4-None]")
