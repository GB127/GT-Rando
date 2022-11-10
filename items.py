from generic import room_to_index, RandomizerError
from random import shuffle
import networkx as net # version 2.5

class Items:
    def __init__(self, data, world_i, screens_ids):
        self.data = data
        self.world_i = world_i
        self.screens = screens_ids

    def __getitem__(self, screen_item_id):
        if isinstance(screen_item_id, tuple):
            screen_id = screen_item_id[0]
            item_id = screen_item_id[1]
        else:
            screen_id = screen_item_id
            item_id = None
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

        while True:
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

            if bool(self):
                break

    def nodes(self, sorties):
        items_names = {0x8 : "Hookshot", 0xA : "Grey Key",0xB : "Gold Key", 0xE : "Bridge"}
        items_screens = {7:("7 (W)",),  # W0 : plank 
                        9:("9 (S)",),  # W0 : Shovel
                        29:("13 (N)",),  # W1 : Item north of double hookshot.
                        40:("8 (S)", "8 (S)", "8 (S)", "8 (S)", "8 (↗)", "8 (↗)"),  # W2 : Corridor with fruits and gem
                        49:("17 (N)",),  # W3 : Screen with gray key in middle, item on the right behind hookshot
                        53:("21 (W)", "21 (W)", "21 (↗)")  # W3 : movable platform and hookshot
                        }#, 53, 55, 62, 65, 69, 77, 78, 90, 94, 95, 96, 97, 99, 100, 101, 102, 103, 104, 105, 106, 108, 109, 111
        g = net.DiGraph()
        for B7, screen in enumerate(self.screens):
            if not self[screen]: continue
            if screen in items_screens:
                for spawn, item, id in zip(items_screens[screen], self[screen], range(len(self[screen]))):
                    if item in items_names:
                        g.add_edge(spawn, (B7, items_names[item], id))
            else:
                stringed = f'{B7} ({sorties[screen][0].direction})'
                for id, item in enumerate(self[screen]):
                    if item in items_names:
                        g.add_edge(stringed, (B7, items_names[item], id))
        return g






    def __bool__(self):
        """Some preliminary checks that we can do before even checking compatibility with
            exits by assuming all exits are always reachable and have infinite items
            Returns True if, , all items are accessible.
            Returns False if there is some inaccessible items"""
        GrayK = 0xA
        GoldK = 0xB
        Bridge = 0xE

        # World 0
        if any([x in [0xA, 0xB, 0xE] for x in self[10]]):
            # Check if (0,10) has a needed object for W1.
            # It's the screen with a banana and blue gem out of reach.
            # Needs a hookshot to get them, thus can't get an
            # usable item.
            return False
        if len([x for x in self[12] if x in range(0x8, 0xF)]) > 1:
            # Check if (0,12) has at most 1 usable item. If there are
            # More than 1 item, there is the risk that you can get softlocked
            # By using items stupidly.
            return False

        # World 1
        if len([x for x in self[room_to_index(tup=(1,13))] if x in range(0x8, 0xF)]) > 1:
            return False
        if self[room_to_index(tup=(1,7)), 2] in [GrayK, GoldK, Bridge]:
            # Check if the Blue gem location in (1,7) has a key or bridge.
            # I did not check the hookshot, because there are 2 extra hookshot in the second world.
            # And this location is the only item that requires the hookshot.
            return False
        if Bridge in self[room_to_index(tup=(1,7))] and any([x in self[room_to_index(tup=(1,7))] for x in [GrayK, GoldK]]):
            # If plank is not accessible, need to check if Key is locked.
            raise BaseException(self)

        # World 2:
        if self[room_to_index(tup=(2,6)), 2] in range(0x8, 0xF):
            # Check if item in the center is a fruit. It must be a fruit
            # to avoid a softlock if someone misuses or grab some useless items.
            return False

        # World 4:
        if any([x in self[room_to_index(tup=(4,12))] for x in [GrayK, GoldK]]):
            return False
        return True