class infos:
    """
        This class is more of a tool for me. I will store my findings of infos here.
        And if I need to get an info during my coding, I'll simply call this class and then ask it to
        Retrieve the things I need.
    """
    def __init__(self):
        self.infos = {

                    }

class ROM:
    def __init__(self,data):
        """
        This constructor convert the game (that is only in bytes)
        into a byte array that is a mutable form.

        data should be in bytes
        """
        if len(data) % 1024 == 512:
            print("Your game has a header! It's removed")
        self.data = bytearray(data[512:])
    def __getitem__(self,offset):
        return hex(self.data[offset])
    def __setitem__(self,offset, value):
        self.data[offset] = value