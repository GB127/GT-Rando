"""
    def print_world(self, world_i, frame_i):

        ID_string = {
            0x0 : "WW",
            0x2 : "AA",
            0x4 : "EE",
            0x6 : "SS",
            0x8 : "PP",
            0xA : "BB",
            0xC : "LL",
            0xE : "22",
            0x10 : "II",
            0x12 : "CC",
            0x14 : "TT",
            0x16 : "RR",
            0x18 : "rr",
            0x1A : "XX",
            0x1C : "GG",
            0x1E : "OO",
            0x20 : "RR"
            }

        boundary_top = "_" * 34
        boundary_bottom = "¯" * 34
        string_list = []
        for _ in range(28):
            string_list.append("|" + " " * 32 + "|")

        for one in self.get_world_frame(world_i, frame_i):
            x = int(2*one[1][0])
            y = int(2*one[1][1])
            string_list[y] = string_list[y][:x+1] + ID_string[one[0]] + string_list[y][x+3:]
            string_list[y+1] = string_list[y+1][:x+1] + ID_string[one[0]] + string_list[y+1][x+3:]


        string = "\n".join(string_list)


        print(boundary_top)
        print(string)
        print(boundary_bottom)

"""
