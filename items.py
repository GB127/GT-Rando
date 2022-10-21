from generic import room_to_index, RandomizerError
from random import shuffle

class Items:
    def __init__(self, data, world_i, screens_ids):
        self.data = data
        self.world_i = world_i
        self.screens = screens_ids

    def __getitem__(self, screen_id, item_id=None):
        items = []
        num_objets = self.data.screens[screen_id].num_class_2_sprites
        for objet_id in range(num_objets):
            objet_type = self.data.screens[screen_id].class_2_sprites[objet_id].type
            if objet_type in range(0x8, 0xF) or objet_type in range(0x40, 0x47, 2):
                items += [objet_type]
        if item_id:
            return items[item_id]
        else:
            return items


    def __setitem__(self, tupl, new_item):
        screen_id, item_id = tupl

        num_objets = self.data.screens[screen_id].num_class_2_sprites
        for objet_id in range(num_objets):
            objet_type = self.data.screens[screen_id].class_2_sprites[objet_id].type
            if objet_type in range(0x8, 0xF) or objet_type in range(0x40, 0x47, 2):
                if item_id == 0:
                    self.data.screens[screen_id].class_2_sprites[objet_id].type = new_item
                    break
                item_id -= 1



    def __str__(self):
        items_names = {0x8 : "Hookshot", 0x9 : "Candle  ", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel  ", 0xD : "Bell    ", 0xE : "Bridge  "}
        fruits_names = {0x40 : "Cherry  ", 0x42: "Banana  ", 0x44 : "Red Gem ", 0x46 : "Blue Gem"}
        table_str = ""
        for B7, screen in enumerate(self.screens):
            tempo_items = ""
            tempo_fruits = ""
            if self[screen]:
                items = self[screen]
                tempo_fruits = ", ".join([fruits_names[x] for x in items if x in fruits_names])
                tempo_items =  ", ".join([items_names[x] for x in items if x in items_names])
                table_str += f'{str(room_to_index(id=self.screens[B7])):8}{tempo_items:<48}| {tempo_fruits:<48}\n'

        line = "-" * 100
        return f'{table_str}{line}'

    def __call__(self, randomize_items=False, randomize_fruits=False, combine=False):
        def randomized_items():
            def item_pool():
                items = []
                for screen in self.screens:
                    for item in self[screen]:
                        if item in range(0x8, 0xF):
                            items.append(item)
                return items

            def fruits_pool():
                fruits = []
                for screen in self.screens:
                    for item in self[screen]:
                        if item in range(0x40, 0x47, 2):
                            fruits.append(item)
                return fruits

            items = item_pool()
            fruits = fruits_pool()

            if randomize_items:
                shuffle(items)
            if randomize_fruits:
                shuffle(fruits)
            all_items = items + fruits
            if combine:
                shuffle(all_items)
            return all_items

        if not any([randomize_fruits, randomize_items]): return
        if combine and not all([randomize_fruits, randomize_items]):
            raise RandomizerError("The flag combine must be used with both randomize fruits and randomize items")
        all_items = randomized_items()
        for screen in self.screens:
            if self[screen]:
                for item_id, current_item in enumerate(self[screen]):
                    if combine:
                        new_item = all_items[0]
                    else:
                        if current_item in range(0x8, 0xF):
                            new_item = next(x for x in all_items if x in range(0x8, 0xF))
                        elif current_item in range(0x40, 0x47, 2):
                            new_item = next(x for x in all_items if x in range(0x40, 0x47, 2))
                    self[screen, item_id] = new_item
                    all_items.remove(new_item)
        raise BaseException(f'\n{self}')