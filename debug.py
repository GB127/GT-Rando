from gameclass import GT
from patch import *


class debug(GT):
    def list_freespace(self):
        self.freespace = [offset for offset in range(0x7374, 0x7FB0)]
        self.freespace += [offset for offset in range(0xFF33, 0x10000)]
        self.freespace += [offset for offset in range(0x1401, 0x15E00)]
        self.freespace += [offset for offset in range(0x1F9C1, 0x1FA42)]
        self.freespace += [offset for offset in range(0x1FADC, 0x20000)]
        self.freespace += [offset for offset in range(0x2A796, 0x2C000)]
        self.freespace += [offset for offset in range(0x47DFE, 0x48000)]
        self.freespace += [offset for offset in range(0x45055, 0x4F100)]
        self.freespace += [offset for offset in range(0x4FD48, 0x50000)]
        self.freespace += [offset for offset in range(0x53F70, 0x54000)]
        self.freespace += [offset for offset in range(0x55FC0, 0x56000)]
        self.freespace += [offset for offset in range(0x57E00, 0x58000)]
        self.freespace += [offset for offset in range(0x5E240, 0x5F000)]
        self.freespace += [offset for offset in range(0x5FBDC, 0x5FE00)]
        self.freespace += [offset for offset in range(0xFB5BE, 0xFD400)]
        self.freespace += [offset for offset in range(0x7FB20, 0x7FE00)]
        self.freespace += [offset for offset in range(0x7FE50, 0x7FEA0)]
        self.freespace += [offset for offset in range(0x7FED0, 0x7FF00)]
        self.freespace += [offset for offset in range(0x7FFB0, 0x7FFFF)]


        self.freespace += [offset for offset in range(0x72A9, 0x72D6)]
        self.used = []

    def save_file(self):
        result = s_result()
        rv = self.lib.conclude(pointer(result))
        with open("debug.smc", "wb") as debug_file:
            debug_file.write(self.rom_data[0:result.num_banks*32768])

if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())  # Open the debug class, which, as the time of writting, an exact copy of the class GT on gameclass.py
        test.save_file()
