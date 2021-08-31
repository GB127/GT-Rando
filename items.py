from generic import world_indexes, room_to_index

class Items2:
    def __init__(self, data, world_i, screens_ids):
        self.data = data
        self.world_i = world_i
        self.screens = screens_ids

        self.screens_items = {}
        self.screens_fruits = {}
        for B7, screen_id in enumerate(screens_ids):
            self.screens_items[B7] = []
            self.screens_fruits[B7] = []

            num_objets = self.data.screens[screen_id].num_class_2_sprites
            for objet_id in range(num_objets):
                objet_type = self.data.screens[screen_id].class_2_sprites[objet_id].type
                if objet_type in range(0x8, 0xF):
                    self.screens_items[B7].append(objet_type)
                elif objet_type in range(0x40, 0x47,2):
                    self.screens_fruits[B7].append(objet_type)

    def __str__(self):
        items_names = {0x8 : "Hookshot", 0x9 : "Candle  ", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel  ", 0xD : "Bell    ", 0xE : "Bridge  "}
        fruits_names = {0x40 : "Cherry  ", 0x42: "Banana  ", 0x44 : "Red Gem ", 0x46 : "Blue Gem"}
        counts_items = {}
        counts_fruits = {}


        table_str = ""
        for B7, screen in enumerate(self.screens_items):
            tempo_items = ""
            tempo_fruits = ""

            if self.screens_items[screen]:
                tempo_items = ", ".join([items_names[x] for x in self.screens_items[screen]])
                for item in self.screens_items[screen]:
                    counts_items[items_names[item]] = counts_items.get(items_names[item], 0) + 1

            if self.screens_fruits[screen]:
                tempo_fruits = ", ".join([fruits_names[x] for x in self.screens_fruits[screen]])
                for fruit in self.screens_fruits[screen]:
                    counts_fruits[fruits_names[fruit]] = counts_items.get(fruits_names[fruit], 0) + 1

            if any([tempo_fruits, tempo_items]):
                table_str += f'{str(room_to_index(id=self.screens[B7])):8}{tempo_items:<48}| {tempo_fruits:<48}\n'

        line = "-" * 100
        return f'{table_str}\n{line}\nItems totals : {counts_items}\nFruits totals: {counts_fruits}'

