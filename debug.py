from gameclass import GT
from generic import world_indexes, room_to_index
from world import World
from exits import Exits
from items import Items
from random import shuffle

class debug(GT):
    def __init__(self, data):
        super().__init__(data)
        del self.Worlds
        self.Worlds = [World_debug(self.data, x) for x in range(5)]

    def save(self):
        super().save("debug.smc")

class World_debug(World):
    def __init__(self, data, world_i):
        super().__init__(data, world_i)
        del self.Exits
        del self.Items
        
        self.Exits = Exits_debug(self.data, self.world_i, world_indexes(self.world_i))
        self.Items = Items_debug(self.data, self.world_i, world_indexes(self.world_i))

    def screen(self, B7):
        def transform_byt_co(big_value):
            assert big_value <= 0x6bc and big_value >=0, "Byte value must be 0 to 0x6BC"
            assert big_value % 2 == 0, "Byte value must be pair, else it will appear gliched."

            y = ( big_value // 0x40) / 2
            x = (big_value % 0x40) / 2
            return x/2, y

        def get_interactives(screen_id):
            screen_data = self.data.screens[screen_id]
            interactives = []
            for id in range(screen_data.num_itiles):
                objet = screen_data.itiles[id]
                interactives.append((objet.type, transform_byt_co(objet.tile_index)))
            return interactives


        screen_id = room_to_index(tup=(self.world_i, B7))


        interactives_string = {
            0x0 : "W",
            0x2 : "A",
            0x4 : "E",
            0x6 : "S",
            0x8 : "P",
            0xA : "B",
            0xC : "L",
            0xE : "2",
            0x10 : "I",
            0x12 : "C",
            0x14 : "T",
            0x16 : "R",
            0x18 : "r",
            0x1A : "X",
            0x1C : "G",
            0x1E : "O",
            0x20 : "R"
            }

        boundary_top = "_" * 34
        boundary_bottom = "¯" * 34


        string_list = []
        for y in range(28):
            tempo = [" " for _ in range(32)]
            # ...
            for interactive in get_interactives(screen_id):
                typ = interactive[0]
                inter_x = interactive[1][0]
                inter_y = interactive[1][1] 
                if 2* inter_y == y or (2 * inter_y +1) == y:
                    tempo[int(2 * inter_x)] = interactives_string[typ]
                    tempo[int(2* inter_x) + 1] = interactives_string[typ]


            new_str = "|" + "".join(tempo) + "|"
            string_list.append(new_str)

        print(boundary_top)
        print("\n".join(string_list))
        print(boundary_bottom)


class Exits_debug(Exits):
    def set_exit(self, B7, exit_id, destination):
        # Destination : tuple (new_B7, exit_id)

        def fetch_new_coordinates(destination, exit_id):
            count = 0
            for B7, screen_id in enumerate(self.screens_ids):
                for exi in range(self.data.screens[screen_id].num_exits):
                    current_exit = self.data.screens[screen_id].exits[exi]
                    if current_exit.dst_screen == destination:
                        count += 1
                        if count == exit_id + 1:
                            return current_exit.dst_x, current_exit.dst_y

        assert isinstance(destination, tuple), f"Destination must be a tuple : (New B7, Entrance ID)\n Data received: {destination}"
        assert destination[0] in range(len(self.screens_ids)) and B7 in range(len(self.screens_ids)) , f"B7 and New exit must be a value in {list(range(len(self.screens_ids)))}\nB7 : {B7} , New exit : {destination[0]}"
        assert exit_id in range(self.data.screens[self.screens_ids[B7]].num_exits), f"B7 exit id must be in {list(range(self.data.screens[self.screens_ids[B7]].num_exits))}\nCurrent exit id : {exit_id}"
        assert destination[1] in range(self.data.screens[self.screens_ids[destination[1]]].num_exits), f"Destination exit id must be in {list(range(self.data.screens[self.screens_ids[destination[0]]].num_exits))}"

        self.data.screens[self.screens_ids[B7]].exits[exit_id].dst_screen = destination[0]
        self.data.screens[self.screens_ids[B7]].exits[exit_id].dst_x, self.data.screens[self.screens_ids[B7]].exits[exit_id].dst_y = fetch_new_coordinates(destination[0], destination[1])
        self.generate_data()


class Items_debug(Items):
    def set_item(self, B7, item_id, new_item):
        def compatible_ids():
            liste = []
            for item_id in range(32):
                check_item = self.data.screens[self.screens[B7]].class_2_sprites[item_id].type
                if check_item in items_names.keys():
                    liste.append(item_id)
            return liste

        items_names = {0x8 : "Hookshot", 0x9 : "Candle  ", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel  ", 0xD : "Bell    ", 0xE : "Bridge  ", 0x40 : "Cherry  ", 0x42: "Banana  ", 0x44 : "Red Gem ", 0x46 : "Blue Gem"}
        assert new_item in items_names.keys(), f"New item need to be a value in {list(items_names)}\n New item : {new_item}"

        self.data.screens[self.screens[B7]].class_2_sprites[compatible_ids()[item_id]].type = new_item
        self.generate_data()


if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())
        # shuffle(tempo)
        string1 = str(test.Worlds[0].Exits)
        test.Worlds[0].Exits(randomize=True)
        string2 = str(test.Worlds[0].Exits)
        print(string1 == string2)
        print(string2)