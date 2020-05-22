hookshot = 2
candle = 4
greyK = 6
goldK = 8
shovel = 10
bell = 12
bridge = 14
listitems = [hookshot, candle, greyK, goldK, shovel, bell, bridge]

def itemtable():
    for i in listitems : print(i)

class infos:
    """
        This class is more of a tool for me. I will store my findings of infos here.
        And if I need to get an info during my coding, I'll simply call this class and then ask it to
        Retrieve the things I need.
    """




    def __init__(self):
        self.adresses = {
            hex(0x143) : "Inventory 2 ID",
            hex(0x142) : "Inventory 1 ID"
                    }
        self.infos = {
            "items" 


        }
    def getadresses(self,*strings):
        liste = []