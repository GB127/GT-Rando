from generic import world_indexes, room_to_index, RandomizerError
from random import shuffle
from copy import deepcopy

class Items:
    def __init__(self, data, world_i, screens_ids):
        self.data = data
        self.world_i = world_i
        self.screens = screens_ids

        self.items = {}
        self.fruits = {}
        for B7, screen_id in enumerate(screens_ids):
            num_objets = self.data.screens[screen_id].num_class_2_sprites
            for objet_id in range(num_objets):
                objet_type = self.data.screens[screen_id].class_2_sprites[objet_id].type
                if objet_type in range(0x8, 0xF):
                    self.items[B7] = self.items.get(B7, []) + [objet_type]
                elif objet_type in range(0x40, 0x47,2):
                    self.fruits[B7] = self.fruits.get(B7, []) + [objet_type]

    def __str__(self):
        items_names = {0x8 : "Hookshot", 0x9 : "Candle  ", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel  ", 0xD : "Bell    ", 0xE : "Bridge  "}
        fruits_names = {0x40 : "Cherry  ", 0x42: "Banana  ", 0x44 : "Red Gem ", 0x46 : "Blue Gem"}
        counts_items = {}
        counts_fruits = {}


        table_str = ""
        for B7, screen in enumerate(self.screens):
            tempo_items = ""
            tempo_fruits = ""
            
            if self.items.get(screen, False):
                tempo_items = ", ".join([items_names[x] for x in self.items[screen]])
                for item in self.items[screen]:
                    counts_items[items_names[item]] = counts_items.get(items_names[item], 0) + 1

            if self.fruits.get(screen, False):
                tempo_fruits = ", ".join([fruits_names[x] for x in self.fruits[screen]])
                for fruit in self.fruits[screen]:
                    counts_fruits[fruits_names[fruit]] = counts_items.get(fruits_names[fruit], 0) + 1

            if any([tempo_fruits, tempo_items]):
                table_str += f'{str(room_to_index(id=self.screens[B7])):8}{tempo_items:<48}| {tempo_fruits:<48}\n'

        line = "-" * 100
        return f'{table_str}{line}\nItems totals : {counts_items}\nFruits totals: {counts_fruits}'

    def __call__(self, randomize_items=False, randomize_fruits=False, combine=False, completely_random=False):
        def get_list_items():
            liste = []
            for liste_items in self.items.values():
                liste += liste_items
            return liste

        def get_list_fruits():
            liste = []
            for liste_items in self.fruits.values():
                liste += liste_items
            return liste

        def distribute(liste, combine):
            liste_all = liste
            if not combine:
                for screen in self.items.keys():
                    self.items[screen] = liste_all[:len(self.items[screen])]
                    liste_all = liste_all[len(self.items[screen]):]
                for screen in self.fruits.keys():
                    self.fruits[screen] = liste_all[:len(self.fruits[screen])]
                    liste_all = liste_all[len(self.fruits[screen]):]
            elif combine:
                self.copy_fruits = deepcopy(self.fruits)
                self.copy_items = deepcopy(self.items)
                self.fruits = {}
                self.items = {}
                for screen_id in self.screens:
                    total = len(self.copy_fruits.get(screen_id, [])) + len(self.copy_items.get(screen_id, []))
                    for item in range(total):
                        if liste_all[0] in range(0x8, 0xF):
                            self.items[screen_id] = self.items.get(screen_id, []) + [liste_all[0]]
                        else:
                            self.fruits[screen_id] = self.fruits.get(screen_id, []) + [liste_all[0]]
                        liste_all.pop(0)

        if not any([randomize_fruits, combine, completely_random, randomize_items]): return
        if combine and any([randomize_fruits, randomize_items]):
            explication = f"You cannot use the combine flag with randomize fruits or/and randomize items. This is to ensure the randomization stays the same even if it doesn't matter for the player"
            options_selected = "\n".join([
                    f'   Combine : {combine}',
                    f'   randomize fruits: {randomize_fruits}',
                    f'   randomize items: {randomize_items}',
                    ])
            raise RandomizerError(f'{explication}\n\nOptions selected:\n{options_selected}')


            raise RandomizerError()
        if completely_random: raise RandomizerError("The option completely random isn't supported yet.")


        liste_items = get_list_items()
        liste_fruits = get_list_fruits()


        if randomize_items: shuffle(liste_items)
        if randomize_fruits: shuffle(liste_fruits)
        liste_all = liste_items + liste_fruits
        if combine: shuffle(liste_all)
        
        distribute(liste_all, combine)
