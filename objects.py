import random
from generic import world_indexes, room_to_index, RandomizerError

def transform_byt_co(self, big_value):
    assert big_value <= 0x6bc and big_value >=0, "Byte value must be 0 to 0x6BC"
    assert big_value % 2 == 0, "Byte value must be pair, else it will appear gliched."

    y = ( big_value // 0x40) / 2
    x = (big_value % 0x40) / 2
    return x/2, y

# https://github.com/Zarby89/GoofTroop/blob/master/Bank81.asm#L8296

class Grabbables:
    def __init__(self, data):
        self.data = data

    def bosses(self):
                # Thrown item table.
                #Thrown item table.
                #    00 barel
                #    02 pot 
                #    04 egg 
                #    06 sign
                #    08 plant
                #    0A bomb
                #    0C log
                #    0E fence 
                #    10 ice 
                #    12 shell 
                #    14 plates
                #    16 rock
                #    18 nut
                #    1A spike
                #    FF = nothing

        pass

    def __call__(self, game_by_game=False, world_by_world=False, screen_by_screen=False, object_by_object=False):
        def generate_newItems():
            new_distribution = {}
            Barrel, Pot, Egg, Sign, Plant, Bomb, Log, Something, RedBox, Shell, Something2, Rock, Coconut, Star_Block, Green_Block, Orange_Block, Red_Block = [x for x in range(0, 0x21, 2)]
            changeables_items = [Barrel, Pot, Egg, Sign, Plant, Bomb,
                                Log, Something, RedBox, Shell, Something2,
                                Rock, Coconut]
            for grabbable in changeables_items:
                new_distribution[grabbable] = random.choice(changeables_items)
            return new_distribution


        if not any([world_by_world, screen_by_screen, game_by_game, object_by_object]):
            return
        elif [world_by_world, screen_by_screen, game_by_game, object_by_object].count(True) > 1: 
            explication = f"You cannot use more than one options among the {self.__class__.__name__} options"
            options_selected = "\n".join([
                    f'   world by world : {world_by_world}',
                    f'   Screen by Screen : {screen_by_screen}',
                    f'   game by game : {game_by_game}',
                    f'   object by object : {object_by_object}'
                    ])
            raise RandomizerError(f'{explication}\n\nOptions selected:\n{options_selected}')


        if game_by_game: new_items = generate_newItems()
        for world_id in range(5):
            if world_by_world: new_items = generate_newItems()
            for id_screen in world_indexes():
                if screen_by_screen: new_items = generate_newItems()
                for id_item in range(self.data.screens[id_screen].num_itiles):
                    if object_by_object: new_items = generate_newItems()
                    current_item = self.data.screens[id_screen].itiles[id_item].type
                    if current_item >= 0x1A: continue
                    self.data.screens[id_screen].itiles[id_item].type = new_items[current_item]


    def __str__(self):
        totaux = {}
        count = 0
        item_names = ["Barrel", "Pot", "Egg", "Sign", "Plant", "Bomb", "Log", "Something", "RedBox", "Shell", "Something2", "Rock", "Coconut", "Star Block", "Green Block", "Orange Block", "Red Block"]
        for id_screen in world_indexes():
            for id_item in range(self.data.screens[id_screen].num_itiles):
                current_item = self.data.screens[id_screen].itiles[id_item].type
                if current_item >= 0x1A: continue
                count += 1
                totaux[item_names[int(current_item/2)]] = totaux.get(item_names[int(current_item/2)], 0) + 1
        return f'{count} items\n{totaux}'


class Versions:
    def __init__(self, data):
        self.versions = [0 for _ in world_indexes()]
        self.data = data

    def __call__(self, world_by_world=False, room_by_room=False, game_by_game=False):
        if not any([world_by_world, room_by_room, game_by_game]):
            return
        elif [world_by_world, room_by_room, game_by_game].count(True) > 1: 
            explication = f"You cannot use more than one options among the {self.__class__.__name__} options"
            options_selected = "\n".join([
                    f'   world by world : {world_by_world}',
                    f'   room by room : {room_by_room}',
                    f'   game by game : {game_by_game}',
                    ])
            raise RandomizerError(f'{explication}\n\nOptions selected:\n{options_selected}')

        print(f"Randomizing {self.__class__.__name__}...")
        if game_by_game: new_version = random.randint(0,3)
        for world in range(5):
            if world_by_world: new_version = random.randint(0,3)
            for id in world_indexes(world):
                if room_by_room: new_version = random.randint(0,3)
                self.versions[id] = new_version
        self.save()
        print(f"Finished Randomizing {self.__class__.__name__}.")


    def __str__(self):
        versions_names = ["US", "J1", "J2", "J3"]

        # Faisons la liste des versions avec des lettres au lieu de juste 0-1-2-3
        liste_versions_changes = ([f'{str(room_to_index(id=no)):7} : {versions_names[x]} | ' for no, x in enumerate(self.versions)])

        # Contruisons le tableau.
        table = ""
        count = 0  # Pour des sauts de lignes.
        for screen in liste_versions_changes:
            count += 1
            table += f'{screen}'
            if count % 10 == 0:  # Si le tableau est trop large, réduire ce chiffre.
                table += "\n"

        # Faisons le total.
        totals = [f'{versions_names[x]} : {self.versions.count(x)}' for x in range(4)]
        totals_str = "Totals      " + "      ".join(totals)

        return f'Versions:\n{table}\n\n{totals_str}'


    def save(self):  # Because of the huge datas and how I approached, the save function is separate from the call.
        def transform_co_byt(coordinates):
            x, y = coordinates
            assert x <= 15 and x >= 0, "X must be in 0 and 15"
            assert y <= 13 and y >= 0, "Y must b in 0 and 13"
            assert x % 0.5 == 0 and y % 0.5 == 0, "X or Y must be a multiple of 0.5"
            transfo_y = y * 2 * 0x40
            big_value = transfo_y + x * 2 *2
            return int(big_value)

        Barrel, Pot, Egg, Sign, Plant, Bomb, Log, Something, RedBox, Shell, Something2, Rock, Coconut, Star_Block, Green_Block, Orange_Block, Red_Block = [x for x in range(0, 0x21, 2)]

        J1 = [
            [],
            [],
            [(Coconut, (2, 3)), (Coconut, (2, 7)), (Coconut, (13, 7)), (Star_Block, (6, 10)), (Star_Block, (9, 10))],
            [(Star_Block, (3, 5)), (Star_Block, (11, 7)), (Star_Block, (12, 8)), (Star_Block, (13, 8)), (Star_Block, (13, 9))],
            [(Barrel, (1.5, 5)), (Barrel, (2.5, 5)), (Barrel, (2.5, 4)), (Pot, (13, 11)), (Pot, (14, 10)), (Plant, (6.5, 5)), (Plant, (7.5, 5)), (Plant, (6.5, 9)), (Plant, (7.5, 9))],
            [(Plant, (3, 3)), (Plant, (4, 3)), (Plant, (5, 3)), (Plant, (6, 3)), (Plant, (7, 3)), (Plant, (10, 4)), (Plant, (12, 4)), (Plant, (6, 10)), (Plant, (6, 11)), (Plant, (6, 12)), (Plant, (9, 9)), (Plant, (9, 10)), (Plant, (9, 11)), (Star_Block, (6, 9)), (Coconut, (1, 9))],
            [(Plant, (9, 7)), (Plant, (7, 10)), (Plant, (8, 10)), (Star_Block, (3, 8)), (Star_Block, (8, 4)), (Star_Block, (12, 8))],
            [(Egg, (14, 2))],
            [(Coconut, (1.5, 12)), (Coconut, (6.5, 5)), (Coconut, (13.5, 2)), (Coconut, (14, 11)), (Coconut, (14, 12))],
            [(Barrel, (1, 12)), (Barrel, (4, 12)), (Barrel, (8, 9)), (Plant, (11, 10)), (Plant, (12, 10)), (Plant, (14, 8)), (Plant, (14, 9)), (Plant, (14, 10)), (Plant, (14, 11)), (Plant, (14, 12))],
            [(Plant, (1, 3)), (Plant, (2, 11)), (Plant, (2, 12)), (Plant, (5, 6)), (Plant, (5, 7)), (Plant, (5, 8)), (Plant, (5, 9)), (Plant, (10, 3)), (Plant, (10, 4)), (Plant, (12, 11))],
            [(Star_Block, (6, 7)), (Star_Block, (5, 8)), (Star_Block, (10, 8)), (Star_Block, (13, 6))],
            [(Star_Block, (6, 9)), (Star_Block, (12.5, 4))],
            [(Star_Block, (4, 9)), (Star_Block, (4, 10)), (Star_Block, (6, 7)), (Star_Block, (8, 7)), (Star_Block, (10, 9)), (Star_Block, (11, 6))],
            [(Barrel, (1, 8)), (Barrel, (14, 8)), (Barrel, (1.5, 12)), (Barrel, (13.5, 12))],
            [(Barrel, (1, 4)), (Barrel, (1, 12)), (Barrel, (2, 12)), (Plant, (12, 6)), (Plant, (12, 7)), (Plant, (12, 8)), (Plant, (12, 9)), (Plant, (12, 10)), (Plant, (3, 12)), (Plant, (4, 12)), (Plant, (5, 12)), (Star_Block, (14, 9))],
            [(Star_Block, (6, 6)), (Star_Block, (9, 6)), (Barrel, (7, 5)), (Barrel, (8, 5)), (Barrel, (5, 7)), (Barrel, (5, 8)), (Barrel, (4, 8)), (Barrel, (10, 7)), (Barrel, (10, 8)), (Barrel, (11, 8))],
            [],
            [(Star_Block, (3, 8)), (Star_Block, (8, 8)), (Star_Block, (9, 8)), (Star_Block, (10, 9))],
            [(Plant, (6, 11)), (Plant, (8, 11)), (Plant, (5, 4)), (Plant, (5, 5)), (Plant, (5, 6)), (Plant, (10, 11)), (Plant, (7, 8))],
            [(Barrel, (1, 2)), (Barrel, (8, 11)), (Barrel, (8, 12)), (Barrel, (12, 9)), (Barrel, (7, 4)), (Barrel, (9, 4)), (Star_Block, (8, 7)), (Star_Block, (8, 8))],
            [(Plant, (6, 6)), (Plant, (8, 8))],
            [(Plant, (1, 8)), (Plant, (5, 10)), (Plant, (10, 12)), (Plant, (11, 12)), (Green_Block, (2, 6)), (Green_Block, (5, 8)), (Green_Block, (5, 11)), (Green_Block, (4, 11)), (Green_Block, (10, 4)), (Green_Block, (11, 4))],
            [(Plant, (11, 3)), (Plant, (12, 4)), (Plant, (12, 12))],
            [(Plant, (2, 2)), (Plant, (3, 2)), (Plant, (5, 12)), (Plant, (6, 12)), (Plant, (11, 4)), (Plant, (12, 3)), (Plant, (12, 2))],
            [(Star_Block, (7, 4)), (Star_Block, (11, 4)), (Green_Block, (2, 5)), (Green_Block, (4, 7)), (Green_Block, (10, 8)), (Green_Block, (12, 10))],
            [],
            [(Barrel, (1, 2)), (Barrel, (2, 2)), (Barrel, (3, 2)), (Barrel, (4, 2)), (Barrel, (4, 3)), (Barrel, (6, 6)), (Barrel, (6, 8)), (Barrel, (7, 8))],
            [(Barrel, (1, 12)), (Barrel, (2, 12)), (Barrel, (4, 12)), (Barrel, (5, 12)), (Barrel, (13, 10))],
            [(Barrel, (1, 12))],
            [],
            [(Barrel, (2.5, 11)), (Barrel, (2.5, 12)), (Barrel, (12.5, 11)), (Barrel, (12.5, 12))],
            [(Plant, (0.5, 11)), (Plant, (1.5, 11)), (Plant, (1.5, 12))],
            [],
            [(Plant, (2, 2)), (Plant, (1, 3)), (Plant, (13, 2)), (Plant, (14, 3)), (Plant, (13, 12)), (Plant, (14, 11))],
            [],
            [],
            [(Plant, (1, 2)), (Plant, (14, 2)), (Plant, (6.5, 7)), (Plant, (8.5, 7)), (Plant, (1, 12)), (Plant, (14, 12))],
            [(Pot, (1, 11)), (Pot, (1, 12)), (Pot, (2, 12)), (Pot, (13, 12)), (Pot, (14, 12)), (Pot, (14, 11))],
            [],
            [(Pot, (1, 2)), (Pot, (1, 12)), (Pot, (5, 2)), (Pot, (11, 12)), (Pot, (14, 12))],
            [],
            [(Pot, (1, 2)), (Pot, (1, 12)), (Pot, (14, 6)), (Star_Block, (2, 6)), (Star_Block, (8, 5)), (Star_Block, (8, 7)), (Star_Block, (10, 6))],
            [],
            [(Pot, (3, 3.5)), (Pot, (7, 3.5)), (Pot, (11, 3.5)), (Pot, (4.5, 8.5)), (Pot, (5.5, 8.5)), (Pot, (8.5, 8.5)), (Pot, (9.5, 8.5))],
            [],
            [(Pot, (1, 6)), (Pot, (1, 7)), (Pot, (1, 8)), (Pot, (1, 12)), (Pot, (10, 2)), (Pot, (9, 5)), (Pot, (10, 5)), (Pot, (14, 12))],
            [],
            [(Pot, (1, 2)), (Pot, (6, 6)), (Pot, (9, 6)), (Pot, (14, 2))],
            [(Barrel, (1, 2)), (Barrel, (1, 3)), (Barrel, (2, 3)), (Barrel, (1, 12)), (Barrel, (6, 7.5)), (Barrel, (6, 8.5)), (Barrel, (10, 8.5)), (Barrel, (14, 2))],
            [(Pot, (1, 2)), (Pot, (2, 2)), (Pot, (13, 2)), (Pot, (14, 2))],
            [(Pot, (11, 5)), (Pot, (4, 7.5)), (Pot, (5, 7.5)), (Pot, (4, 10)), (Pot, (5, 10)), (Pot, (13, 9)), (Red_Block, (12, 9)), (Red_Block, (12, 12))],
            [(Pot, (2, 5)), (Pot, (1, 12)), (Pot, (14, 12))],
            [(Pot, (2, 7)), (Pot, (2, 8)), (Pot, (2, 9)), (Pot, (5, 9)), (Pot, (6, 9)), (Pot, (14, 11))],
            [],
            [(Star_Block, (12, 2)), (Star_Block, (12, 3)), (Pot, (2, 2)), (Pot, (2, 3)), (Pot, (4, 5.5)), (Pot, (4, 7.5)), (Pot, (9, 11))],
            [],
            [],
            [(Barrel, (1, 5)), (Barrel, (2, 5)), (Barrel, (3, 5)), (Barrel, (12, 5)), (Barrel, (13, 5)), (Barrel, (14, 5))],
            [(Star_Block, (6, 8)), (Star_Block, (7, 8)), (Star_Block, (8, 8)), (Star_Block, (10, 6)), (Barrel, (7, 7)), (Barrel, (8, 7))],
            [(Barrel, (12, 2)), (Barrel, (12, 3)), (Barrel, (13, 3)), (Barrel, (14, 3)), (Barrel, (14, 2)), (Barrel, (10, 7)), (Barrel, (11, 7)), (Barrel, (12, 7)), (Barrel, (13, 7)), (Barrel, (12, 11)), (Barrel, (12, 12)), (Barrel, (13, 11)), (Barrel, (14, 11)), (Barrel, (14, 12))],
            [(Barrel, (1, 6)), (Barrel, (2, 6)), (Barrel, (3, 6)), (Barrel, (4, 6)), (Barrel, (5, 6)), (Barrel, (6, 6)), (Barrel, (7, 2)), (Barrel, (7, 3)), (Barrel, (8, 2)), (Barrel, (8, 3)), (Barrel, (9, 5)), (Barrel, (10, 5)), (Barrel, (13, 5)), (Barrel, (14, 5))],
            [(Red_Block, (8.5, 7)), (Orange_Block, (4, 4)), (Orange_Block, (5, 10))],
            [],
            [(Barrel, (3, 8)), (Barrel, (6.5, 5.5)), (Barrel, (6.5, 7)), (Barrel, (8.5, 5.5)), (Barrel, (8.5, 7)), (Barrel, (12, 6))],
            [],
            [(Barrel, (7, 3)), (Barrel, (7, 4)), (Barrel, (7, 5)), (Barrel, (7, 6)), (Barrel, (8, 3)), (Barrel, (8, 4)), (Barrel, (8, 5)), (Barrel, (8, 6)), (Barrel, (7, 8)), (Barrel, (7, 9)), (Barrel, (7, 10)), (Barrel, (7, 11)), (Barrel, (8, 8)), (Barrel, (8, 9)), (Barrel, (8, 10)), (Barrel, (8, 11))],
            [(Orange_Block, (1, 6)), (Orange_Block, (1, 8)), (Orange_Block, (1, 10)), (Red_Block, (3, 5))],
            [(Star_Block, (2, 10)), (Star_Block, (4, 4)), (Star_Block, (7, 5)), (Star_Block, (6, 10)), (Star_Block, (10, 9)), (Star_Block, (12, 12)), (Star_Block, (13, 4))],
            [(Star_Block, (5, 10)), (Star_Block, (10, 10))],
            [],
            [(Barrel, (1, 2)), (Barrel, (1, 3)), (Barrel, (2, 3)), (Barrel, (4, 3)), (Barrel, (4, 2)), (Barrel, (1, 12)), (Barrel, (2, 12)), (Barrel, (9, 8)), (Barrel, (10, 8)), (Barrel, (14, 2)), (Barrel, (14, 3)), (Barrel, (9, 8)), (Barrel, (10, 8))],
            [(Barrel, (7, 8)), (Star_Block, (4, 3)), (Star_Block, (5, 4)), (Star_Block, (10, 8)), (Orange_Block, (11, 5)), (Orange_Block, (1, 8)), (Green_Block, (6, 9)), (Green_Block, (7, 4))],
            [],
            [(Barrel, (5, 9)), (Barrel, (6, 9)), (Barrel, (7, 8)), (Barrel, (8, 8)), (Barrel, (9, 9)), (Barrel, (10, 9)), (Barrel, (2, 5)), (Barrel, (12, 5)), (Barrel, (13, 5)), (Star_Block, (3, 7)), (Star_Block, (13, 6)), (Green_Block, (3, 8)), (Green_Block, (5, 10)), (Green_Block, (8, 10)), (Green_Block, (10, 8))],
            [(Barrel, (1, 7)), (Barrel, (2, 9)), (Barrel, (1, 11)), (Barrel, (2, 12)), (Barrel, (8, 12)), (Barrel, (14, 9)), (Barrel, (14, 10)), (Barrel, (14, 11)), (Barrel, (14, 12)), (Green_Block, (9.5, 5)), (Red_Block, (8, 11))],
            [],
            [],
            [(Star_Block, (2, 9)), (Star_Block, (2, 5)), (Star_Block, (4, 5)), (Star_Block, (10, 5)), (Star_Block, (12, 8))],
            [(Star_Block, (7, 7)), (Star_Block, (8, 7)), (Green_Block, (4, 4)), (Green_Block, (2, 5)), (Green_Block, (11, 4)), (Green_Block, (12, 5)), (Green_Block, (6, 10)), (Green_Block, (9, 10))],
            [],
            [(Star_Block, (6, 6)), (Green_Block, (7, 6)), (Green_Block, (3, 5))],
            [(Barrel, (1, 11)), (Barrel, (2, 11)), (Barrel, (1, 12)), (Barrel, (2, 12)), (Barrel, (3, 12)), (Barrel, (4, 12)), (Barrel, (13, 11)), (Barrel, (14, 11)), (Barrel, (11, 12)), (Barrel, (12, 12)), (Barrel, (13, 12)), (Barrel, (14, 12))],
            [],
            [(Barrel, (12, 2)), (Barrel, (12, 3)), (Barrel, (13, 3)), (Barrel, (14, 3)), (Barrel, (14, 2)), (Barrel, (10, 7)), (Barrel, (11, 7)), (Barrel, (12, 7)), (Barrel, (13, 7)), (Barrel, (12, 11)), (Barrel, (12, 12)), (Barrel, (13, 11)), (Barrel, (14, 11)), (Barrel, (14, 12))],
            [(Barrel, (1, 6)), (Barrel, (2, 6)), (Barrel, (3, 6)), (Barrel, (4, 6)), (Barrel, (5, 6)), (Barrel, (6, 6)), (Barrel, (7, 2)), (Barrel, (7, 3)), (Barrel, (8, 2)), (Barrel, (8, 3)), (Barrel, (9, 5)), (Barrel, (10, 5)), (Barrel, (13, 5)), (Barrel, (14, 5))],
            [(Barrel, (7, 3)), (Barrel, (7, 4)), (Barrel, (7, 5)), (Barrel, (7, 6)), (Barrel, (8, 3)), (Barrel, (8, 4)), (Barrel, (8, 5)), (Barrel, (8, 6)), (Barrel, (7, 8)), (Barrel, (7, 9)), (Barrel, (7, 10)), (Barrel, (7, 11)), (Barrel, (8, 8)), (Barrel, (8, 9)), (Barrel, (8, 10)), (Barrel, (8, 11))],
            [(Barrel, (7, 3)), (Barrel, (7, 4)), (Barrel, (7, 5)), (Barrel, (7, 6)), (Barrel, (8, 3)), (Barrel, (8, 4)), (Barrel, (8, 5)), (Barrel, (8, 6)), (Barrel, (7, 8)), (Barrel, (7, 9)), (Barrel, (7, 10)), (Barrel, (7, 11)), (Barrel, (8, 8)), (Barrel, (8, 9)), (Barrel, (8, 10)), (Barrel, (8, 11))],
            [(Barrel, (11, 11)), (Barrel, (12, 11)), (Barrel, (13, 11)), (Barrel, (11, 12)), (Barrel, (12, 12)), (Barrel, (13, 12))],
            [(Barrel, (3, 10)), (Barrel, (1, 8)), (Barrel, (1, 5)), (Barrel, (5, 2)), (Barrel, (4, 8)), (Barrel, (7, 10)), (Barrel, (8, 12)), (Barrel, (11, 2)), (Barrel, (11, 3)), (Barrel, (13, 2)), (Barrel, (14, 2))],
            [(Barrel, (1, 6)), (Barrel, (1, 7)), (Barrel, (6, 12)), (Barrel, (7, 12)), (Barrel, (13, 10)), (Barrel, (14, 10)), (Barrel, (11, 11)), (Barrel, (11, 12)), (Star_Block, (3, 10)), (Star_Block, (2, 11)), (Star_Block, (1, 12))],
            [(Star_Block, (8, 4)), (Star_Block, (5, 7)), (Star_Block, (6, 7)), (Star_Block, (8, 7)), (Star_Block, (3, 12)), (Star_Block, (7, 12)), (Star_Block, (14, 5))],
            [],
            [(Green_Block, (7, 11))],
            [],
            [(Pot, (1, 2)), (Pot, (4, 2)), (Pot, (11, 2)), (Pot, (14, 2)), (Pot, (1, 12)), (Pot, (4, 12)), (Pot, (11, 12)), (Pot, (14, 12))],
            [(Barrel, (1, 2)), (Barrel, (1, 3)), (Barrel, (1, 4)), (Barrel, (1, 5)), (Barrel, (1, 9)), (Barrel, (1, 10)), (Barrel, (1, 11)), (Barrel, (1, 12)), (Barrel, (11, 2)), (Barrel, (11, 3)), (Barrel, (7, 11)), (Barrel, (7, 12)), (Star_Block, (6, 11)), (Star_Block, (6, 12))],
            [(Barrel, (12, 2)), (Barrel, (13, 2)), (Barrel, (14, 2)), (Barrel, (12, 3)), (Barrel, (13, 3)), (Barrel, (14, 3))],
            [(Star_Block, (5, 7)), (Star_Block, (7, 5))],
            [(Barrel, (1, 11)), (Barrel, (2, 11)), (Barrel, (13, 11)), (Barrel, (14, 11))],
            [(Star_Block, (7, 4)), (Star_Block, (10, 4)), (Star_Block, (8, 7)), (Star_Block, (4, 10)), (Star_Block, (7, 10))],
            [],
            [(Red_Block, (4, 6)), (Red_Block, (5, 6)), (Red_Block, (10, 6)), (Red_Block, (11, 6)), (Orange_Block, (7, 10)), (Orange_Block, (8, 10)), (Green_Block, (13, 8)), (Green_Block, (2, 8))],
            [(Barrel, (9, 12)), (Barrel, (5, 6)), (Barrel, (7, 6)), (Barrel, (2, 3)), (Barrel, (1, 4)), (Barrel, (2, 11)), (Barrel, (8, 9)), (Barrel, (11, 12)), (Barrel, (13, 10)), (Barrel, (8, 4)), (Barrel, (13, 3)), (Barrel, (12, 3)), (Barrel, (11, 3))],
            [(Barrel, (6, 9)), (Barrel, (7, 9)), (Barrel, (8, 9))],
            [(Barrel, (10, 12)), (Barrel, (11, 12)), (Barrel, (14, 9)), (Barrel, (13, 9)), (Barrel, (5, 9)), (Star_Block, (8, 8)), (Star_Block, (11, 5))],
            [],
            [],
            [(Barrel, (1, 3)), (Barrel, (1, 2)), (Barrel, (6, 6)), (Barrel, (6, 7))],
            [],
            [(Star_Block, (5, 7)), (Star_Block, (7, 8)), (Star_Block, (7, 8)), (Star_Block, (10, 7))],
            [(Star_Block, (3, 7)), (Barrel, (4, 5)), (Barrel, (5, 5)), (Barrel, (6, 5)), (Barrel, (7, 5)), (Barrel, (4, 6)), (Barrel, (5, 6)), (Barrel, (6, 6)), (Barrel, (7, 6)), (Barrel, (8, 6)), (Barrel, (4, 7)), (Barrel, (5, 7)), (Barrel, (7, 7)), (Barrel, (8, 7)), (Barrel, (4, 8)), (Barrel, (5, 8)), (Barrel, (6, 8)), (Barrel, (7, 8)), (Barrel, (8, 8)), (Barrel, (4, 9)), (Barrel, (5, 9)), (Barrel, (6, 9)), (Barrel, (7, 9))],
            [],
            [],
            ]

        US = [
                [],
                [],
                [(Coconut, (2, 3)), (Coconut, (2, 7)), (Coconut, (13, 7)), (Star_Block, (6, 10)), (Star_Block, (9, 10))],
                [(Star_Block, (3, 5)), (Star_Block, (12, 5)), (Star_Block, (13, 5)), (Star_Block, (12, 6)), (Star_Block, (12, 7))],
                [(Barrel, (1.5, 5)), (Barrel, (2.5, 5)), (Barrel, (2.5, 4)), (Pot, (13, 11)), (Pot, (14, 10)), (Plant, (6.5, 5)), (Plant, (7.5, 5)), (Plant, (6.5, 9)), (Plant, (7.5, 9))],
                [(Plant, (3, 3)), (Plant, (4, 3)), (Plant, (5, 3)), (Plant, (6, 3)), (Plant, (7, 3)), (Plant, (10, 4)), (Plant, (12, 4)), (Plant, (6, 10)), (Plant, (6, 11)), (Plant, (6, 12)), (Plant, (9, 9)), (Plant, (9, 10)), (Plant, (9, 11)), (Star_Block, (10, 10)), (Star_Block, (11, 4)), (Coconut, (1, 9))],
                [(Plant, (9, 7)), (Plant, (7, 10)), (Plant, (8, 10)), (Star_Block, (3, 7)), (Star_Block, (8, 4)), (Star_Block, (12, 7))],
                [(Egg, (14, 2))],
                [(Coconut, (1.5, 12)), (Coconut, (6.5, 5)), (Coconut, (13.5, 2)), (Coconut, (14, 11)), (Coconut, (14, 12))],
                [(Barrel, (1, 12)), (Barrel, (4, 12)), (Barrel, (8, 9)), (Plant, (11, 10)), (Plant, (12, 10)), (Plant, (14, 8)), (Plant, (14, 9)), (Plant, (14, 10)), (Plant, (14, 11)), (Plant, (14, 12))],
                [(Plant, (1, 3)), (Plant, (2, 11)), (Plant, (2, 12)), (Plant, (5, 6)), (Plant, (5, 7)), (Plant, (5, 8)), (Plant, (5, 9)), (Plant, (10, 3)), (Plant, (10, 4)), (Plant, (12, 11))],
                [(Star_Block, (6, 7)), (Star_Block, (9, 7)), (Star_Block, (12, 10)), (Star_Block, (13, 6))],
                [(Star_Block, (6, 9)), (Star_Block, (12.5, 4))],
                [(Star_Block, (4, 9)), (Star_Block, (4, 10)), (Star_Block, (6, 7)), (Star_Block, (8, 7)), (Star_Block, (10, 8)), (Star_Block, (11, 6))],
                [(Barrel, (1, 8)), (Barrel, (14, 8)), (Barrel, (1.5, 12)), (Barrel, (13.5, 12))],
                [(Barrel, (1, 4)), (Barrel, (1, 12)), (Barrel, (2, 12)), (Plant, (3, 12)), (Plant, (4, 12)), (Plant, (5, 12)), (Star_Block, (2, 4)), (Star_Block, (4, 4)), (Star_Block, (6, 4)), (Star_Block, (9, 11)), (Star_Block, (12, 10))],
                [(Barrel, (7, 5)), (Barrel, (8, 5)), (Barrel, (5, 7)), (Barrel, (5, 8)), (Barrel, (4, 8)), (Barrel, (10, 7)), (Barrel, (10, 8)), (Barrel, (11, 8))],
                [],
                [(Star_Block, (2, 9)), (Star_Block, (5, 9)), (Star_Block, (6, 8)), (Star_Block, (10, 10))],
                [(Plant, (6, 11)), (Plant, (8, 11)), (Plant, (5, 4)), (Plant, (5, 5)), (Plant, (5, 6)), (Plant, (10, 11)), (Plant, (7, 8))],
                [(Barrel, (1, 2)), (Barrel, (8, 11)), (Barrel, (8, 12)), (Barrel, (12, 9)), (Barrel, (7, 4)), (Barrel, (9, 4)), (Star_Block, (8, 7)), (Star_Block, (8, 8))],
                [(Plant, (6, 6)), (Plant, (8, 8))],
                [(Plant, (1, 8)), (Plant, (5, 10)), (Plant, (10, 12)), (Plant, (11, 12)), (Green_Block, (2, 6)), (Green_Block, (2, 8)), (Green_Block, (5, 6)), (Green_Block, (4, 11)), (Green_Block, (6, 11)), (Green_Block, (10, 4)), (Green_Block, (11, 4))],
                [(Plant, (11, 3)), (Plant, (12, 4)), (Plant, (12, 12)), (Star_Block, (2, 3)), (Star_Block, (1, 4)), (Star_Block, (3, 4)), (Star_Block, (2, 5)), (Star_Block, (2, 9))],
                [(Plant, (2, 2)), (Plant, (3, 2)), (Plant, (5, 12)), (Plant, (6, 12)), (Plant, (11, 4)), (Plant, (12, 3)), (Plant, (12, 2))],
                [(Star_Block, (7, 4)), (Star_Block, (8, 4)), (Star_Block, (4, 5)), (Star_Block, (11, 10))],
                [],
                [(Barrel, (1, 2)), (Barrel, (2, 2)), (Barrel, (3, 2)), (Barrel, (4, 2)), (Barrel, (4, 3)), (Barrel, (6, 6)), (Barrel, (6, 8)), (Barrel, (7, 8))],
                [(Barrel, (1, 12)), (Barrel, (2, 12)), (Barrel, (4, 12)), (Barrel, (5, 12)), (Barrel, (13, 10))],
                [(Barrel, (1, 12)), (Star_Block, (2, 9)), (Star_Block, (3, 10)), (Star_Block, (4, 11)), (Star_Block, (5, 12)), (Star_Block, (11, 5)), (Star_Block, (13, 5)), (Star_Block, (10, 6)), (Star_Block, (11, 6)), (Star_Block, (12, 6)), (Star_Block, (13, 6)), (Star_Block, (12, 7)), (Star_Block, (11, 8))],
                [],
                [(Barrel, (2.5, 11)), (Barrel, (2.5, 12)), (Barrel, (12.5, 11)), (Barrel, (12.5, 12))],
                [(Plant, (0.5, 11)), (Plant, (1.5, 11)), (Plant, (1.5, 12))],
                [],
                [(Plant, (2, 2)), (Plant, (1, 3)), (Plant, (13, 2)), (Plant, (14, 3)), (Plant, (13, 12)), (Plant, (14, 11))],
                [],
                [],
                [(Plant, (1, 2)), (Plant, (14, 2)), (Plant, (6.5, 7)), (Plant, (8.5, 7)), (Plant, (1, 12)), (Plant, (14, 12))],
                [(Pot, (1, 11)), (Pot, (1, 12)), (Pot, (2, 12)), (Pot, (13, 12)), (Pot, (14, 12)), (Pot, (14, 11))],
                [],
                [(Pot, (1, 2)), (Pot, (1, 12)), (Pot, (5, 2)), (Pot, (11, 12)), (Pot, (14, 12))],
                [],
                [(Pot, (1, 2)), (Pot, (1, 12)), (Pot, (14, 6)), (Star_Block, (2, 6)), (Star_Block, (8, 5)), (Star_Block, (8, 7)), (Star_Block, (10, 6))],
                [],
                [(Pot, (3, 3.5)), (Pot, (7, 3.5)), (Pot, (11, 3.5)), (Pot, (4.5, 8.5)), (Pot, (5.5, 8.5)), (Pot, (8.5, 8.5)), (Pot, (9.5, 8.5))],
                [],
                [(Pot, (1, 6)), (Pot, (1, 7)), (Pot, (1, 8)), (Pot, (1, 12)), (Pot, (10, 2)), (Pot, (9, 5)), (Pot, (10, 5)), (Pot, (14, 12))],
                [],
                [(Pot, (1, 2)), (Pot, (6, 6)), (Pot, (9, 6)), (Pot, (14, 2))],
                [(Barrel, (1, 2)), (Barrel, (1, 3)), (Barrel, (2, 3)), (Barrel, (1, 12)), (Barrel, (6, 7.5)), (Barrel, (6, 8.5)), (Barrel, (10, 8.5)), (Barrel, (14, 2))],
                [(Pot, (1, 2)), (Pot, (2, 2)), (Pot, (13, 2)), (Pot, (14, 2))],
                [(Pot, (11, 5)), (Pot, (4, 7.5)), (Pot, (5, 7.5)), (Pot, (4, 10)), (Pot, (5, 10)), (Pot, (13, 9))],
                [(Pot, (2, 5)), (Pot, (1, 12)), (Pot, (14, 12))],
                [(Pot, (2, 7)), (Pot, (2, 8)), (Pot, (2, 9)), (Pot, (5, 9)), (Pot, (6, 9)), (Pot, (14, 11))],
                [],
                [(Red_Block, (12, 2)), (Red_Block, (12, 3)), (Pot, (2, 2)), (Pot, (2, 3)), (Pot, (4, 5.5)), (Pot, (4, 7.5)), (Pot, (9, 11))],
                [],
                [],
                [(Barrel, (1, 5)), (Barrel, (2, 5)), (Barrel, (3, 5)), (Barrel, (12, 5)), (Barrel, (13, 5)), (Barrel, (14, 5))],
                [(Star_Block, (6, 8)), (Star_Block, (7, 8)), (Star_Block, (8, 8)), (Star_Block, (9, 8)), (Barrel, (7, 7)), (Barrel, (8, 7))],
                [(Barrel, (12, 2)), (Barrel, (12, 3)), (Barrel, (13, 3)), (Barrel, (14, 3)), (Barrel, (14, 2)), (Barrel, (10, 7)), (Barrel, (11, 7)), (Barrel, (12, 7)), (Barrel, (13, 7)), (Barrel, (12, 11)), (Barrel, (12, 12)), (Barrel, (13, 11)), (Barrel, (14, 11)), (Barrel, (14, 12))],
                [(Barrel, (1, 6)), (Barrel, (2, 6)), (Barrel, (3, 6)), (Barrel, (4, 6)), (Barrel, (5, 6)), (Barrel, (6, 6)), (Barrel, (7, 2)), (Barrel, (7, 3)), (Barrel, (8, 2)), (Barrel, (8, 3)), (Barrel, (9, 5)), (Barrel, (10, 5)), (Barrel, (13, 5)), (Barrel, (14, 5))],
                [(Star_Block, (8.5, 7)), (Orange_Block, (3, 4)), (Orange_Block, (4, 8)), (Green_Block, (12, 8))],
                [],
                [(Barrel, (3, 8)), (Barrel, (6.5, 5.5)), (Barrel, (6.5, 7)), (Barrel, (8.5, 5.5)), (Barrel, (8.5, 7)), (Barrel, (12, 6))],
                [],
                [(Barrel, (7, 3)), (Barrel, (7, 4)), (Barrel, (7, 5)), (Barrel, (7, 6)), (Barrel, (8, 3)), (Barrel, (8, 4)), (Barrel, (8, 5)), (Barrel, (8, 6)), (Barrel, (7, 8)), (Barrel, (7, 9)), (Barrel, (7, 10)), (Barrel, (7, 11)), (Barrel, (8, 8)), (Barrel, (8, 9)), (Barrel, (8, 10)), (Barrel, (8, 11))],
                [(Green_Block, (2, 12)), (Orange_Block, (3, 11)), (Orange_Block, (1, 4))],
                [(Star_Block, (2, 10)), (Star_Block, (2, 4)), (Star_Block, (6, 10)), (Star_Block, (7, 5)), (Star_Block, (10, 9)), (Star_Block, (13, 4)), (Star_Block, (12, 12))],
                [(Star_Block, (5, 11)), (Star_Block, (12, 11))],
                [],
                [(Barrel, (1, 2)), (Barrel, (1, 3)), (Barrel, (2, 3)), (Barrel, (4, 3)), (Barrel, (4, 2)), (Barrel, (1, 12)), (Barrel, (2, 12)), (Barrel, (9, 8)), (Barrel, (10, 8)), (Barrel, (14, 2)), (Barrel, (14, 3)), (Barrel, (1, 13)), (Barrel, (2, 13))],
                [(Star_Block, (13, 9)), (Star_Block, (3, 10)), (Star_Block, (5, 5)), (Barrel, (7, 8)), (Green_Block, (1, 8)), (Green_Block, (11, 5)), (Green_Block, (6, 4)), (Something, (2, 9)), (Orange_Block, (6, 8))],
                [],
                [(Barrel, (5, 9)), (Barrel, (6, 9)), (Barrel, (7, 8)), (Barrel, (8, 8)), (Barrel, (9, 9)), (Barrel, (10, 9)), (Barrel, (2, 5)), (Barrel, (12, 5)), (Barrel, (13, 5)), (Star_Block, (2, 7)), (Star_Block, (2, 9)), (Star_Block, (13, 6)), (Green_Block, (2, 10)), (Green_Block, (8, 10)), (Green_Block, (12, 7))],
                [(Barrel, (1, 7)), (Barrel, (2, 9)), (Barrel, (1, 11)), (Barrel, (2, 12)), (Barrel, (8, 12)), (Barrel, (14, 9)), (Barrel, (14, 10)), (Barrel, (14, 11)), (Barrel, (14, 12)), (Barrel, (9.5, 5)), (Green_Block, (8, 11))],
                [],
                [],
                [(Star_Block, (4, 10)), (Star_Block, (5, 7)), (Star_Block, (2, 5)), (Star_Block, (8, 7)), (Star_Block, (9, 10))],
                [(Star_Block, (7, 7)), (Star_Block, (8, 7)), (Green_Block, (4, 4)), (Green_Block, (11, 4))],
                [],
                [(Star_Block, (3, 9)), (Star_Block, (6, 9)), (Orange_Block, (6, 4))],
                [(Barrel, (1, 11)), (Barrel, (2, 11)), (Barrel, (1, 12)), (Barrel, (2, 12)), (Barrel, (3, 12)), (Barrel, (4, 12)), (Barrel, (13, 11)), (Barrel, (14, 11)), (Barrel, (11, 12)), (Barrel, (12, 12)), (Barrel, (13, 12)), (Barrel, (14, 12))],
                [],
                [(Barrel, (12, 2)), (Barrel, (12, 3)), (Barrel, (13, 3)), (Barrel, (14, 3)), (Barrel, (14, 2)), (Barrel, (10, 7)), (Barrel, (11, 7)), (Barrel, (12, 7)), (Barrel, (13, 7)), (Barrel, (12, 11)), (Barrel, (12, 12)), (Barrel, (13, 11)), (Barrel, (14, 11)), (Barrel, (14, 12))],
                [(Barrel, (1, 6)), (Barrel, (2, 6)), (Barrel, (3, 6)), (Barrel, (4, 6)), (Barrel, (5, 6)), (Barrel, (6, 6)), (Barrel, (7, 2)), (Barrel, (7, 3)), (Barrel, (8, 2)), (Barrel, (8, 3)), (Barrel, (9, 5)), (Barrel, (10, 5)), (Barrel, (13, 5)), (Barrel, (14, 5))],
                [(Barrel, (7, 3)), (Barrel, (7, 4)), (Barrel, (7, 5)), (Barrel, (7, 6)), (Barrel, (8, 3)), (Barrel, (8, 4)), (Barrel, (8, 5)), (Barrel, (8, 6)), (Barrel, (7, 8)), (Barrel, (7, 9)), (Barrel, (7, 10)), (Barrel, (7, 11)), (Barrel, (8, 8)), (Barrel, (8, 9)), (Barrel, (8, 10)), (Barrel, (8, 11))],
                [(Barrel, (7, 3)), (Barrel, (7, 4)), (Barrel, (7, 5)), (Barrel, (7, 6)), (Barrel, (8, 3)), (Barrel, (8, 4)), (Barrel, (8, 5)), (Barrel, (8, 6)), (Barrel, (7, 8)), (Barrel, (7, 9)), (Barrel, (7, 10)), (Barrel, (7, 11)), (Barrel, (8, 8)), (Barrel, (8, 9)), (Barrel, (8, 10)), (Barrel, (8, 11))],
                [(Barrel, (11, 11)), (Barrel, (12, 11)), (Barrel, (13, 11)), (Barrel, (11, 12)), (Barrel, (12, 12)), (Barrel, (13, 12))],
                [(Barrel, (3, 10)), (Barrel, (1, 8)), (Barrel, (1, 5)), (Barrel, (5, 2)), (Barrel, (4, 8)), (Barrel, (7, 10)), (Barrel, (8, 12)), (Barrel, (11, 2)), (Barrel, (11, 3)), (Barrel, (13, 2)), (Barrel, (14, 2))],
                [(Barrel, (1, 6)), (Barrel, (1, 7)), (Barrel, (6, 12)), (Barrel, (7, 12)), (Barrel, (13, 10)), (Barrel, (14, 10)), (Barrel, (11, 11)), (Barrel, (11, 12)), (Star_Block, (3, 10)), (Star_Block, (2, 12)), (Star_Block, (4, 12)), (Star_Block, (2, 7))],
                [(Star_Block, (2, 2)), (Star_Block, (3, 7)), (Star_Block, (3, 8)), (Star_Block, (5, 4)), (Star_Block, (5, 7)), (Star_Block, (7, 7)), (Star_Block, (8, 7)), (Star_Block, (7, 12)), (Star_Block, (8, 4)), (Star_Block, (11, 4)), (Star_Block, (11, 7)), (Star_Block, (14, 5))],
                [],
                [(Green_Block, (7, 11))],
                [],
                [(Pot, (1, 2)), (Pot, (4, 2)), (Pot, (11, 2)), (Pot, (14, 2)), (Pot, (1, 12)), (Pot, (4, 12)), (Pot, (11, 12)), (Pot, (14, 12))],
                [(Barrel, (1, 2)), (Barrel, (1, 3)), (Barrel, (1, 4)), (Barrel, (1, 5)), (Barrel, (1, 9)), (Barrel, (1, 10)), (Barrel, (1, 11)), (Barrel, (1, 12)), (Barrel, (11, 2)), (Barrel, (11, 3)), (Barrel, (7, 11)), (Barrel, (7, 12)), (Star_Block, (6, 11)), (Star_Block, (6, 12))],
                [(Barrel, (12, 2)), (Barrel, (13, 2)), (Barrel, (14, 2)), (Barrel, (12, 3)), (Barrel, (13, 3)), (Barrel, (14, 3))],
                [(Star_Block, (4, 4)), (Star_Block, (4, 10))],
                [(Barrel, (1, 11)), (Barrel, (2, 11)), (Barrel, (13, 11)), (Barrel, (14, 11))],
                [(Star_Block, (7, 4)), (Star_Block, (10, 4)), (Star_Block, (4, 7)), (Star_Block, (6, 10)), (Star_Block, (10, 7)), (Star_Block, (12, 12))],
                [],
                [(Green_Block, (3, 11)), (Green_Block, (2, 11)), (Green_Block, (8, 11)), (Green_Block, (13, 11))],
                [(Barrel, (9, 12)), (Barrel, (5, 6)), (Barrel, (7, 6)), (Barrel, (2, 3)), (Barrel, (1, 4)), (Barrel, (2, 11)), (Barrel, (8, 9)), (Barrel, (11, 12)), (Barrel, (13, 10)), (Barrel, (8, 4)), (Barrel, (13, 3)), (Barrel, (12, 3)), (Barrel, (11, 3))],
                [(Barrel, (6, 9)), (Barrel, (7, 9)), (Barrel, (8, 9))],
                [(Barrel, (10, 12)), (Barrel, (11, 12)), (Barrel, (14, 9)), (Barrel, (13, 9)), (Barrel, (5, 9)), (Star_Block, (8, 8)), (Star_Block, (11, 5))],
                [],
                [],
                [(Barrel, (1, 3)), (Barrel, (1, 2)), (Barrel, (6, 6)), (Barrel, (6, 7))],
                [],
                [(Star_Block, (9, 4)), (Star_Block, (6, 8)), (Star_Block, (6, 9)), (Star_Block, (9, 7)), (Star_Block, (6, 6))],
                [(Star_Block, (3, 7)), (Barrel, (4, 5)), (Barrel, (5, 5)), (Barrel, (6, 5)), (Barrel, (7, 5)), (Barrel, (4, 6)), (Barrel, (5, 6)), (Barrel, (6, 6)), (Barrel, (7, 6)), (Barrel, (8, 6)), (Barrel, (4, 7)), (Barrel, (5, 7)), (Barrel, (7, 7)), (Barrel, (8, 7)), (Barrel, (4, 8)), (Barrel, (5, 8)), (Barrel, (6, 8)), (Barrel, (7, 8)), (Barrel, (8, 8)), (Barrel, (4, 9)), (Barrel, (5, 9)), (Barrel, (6, 9)), (Barrel, (7, 9))],
                [],
                [],
            ]

        all_versions = [US, J1, J1, J1]

        data = self.data.screens
        for id_screen, version in enumerate(self.versions):
            data[id_screen].num_itiles = len(all_versions[version][id_screen])
            for id_item, item_co in enumerate(all_versions[version][id_screen]):
                data[id_screen].itiles[id_item].type = item_co[0]
                data[id_screen].itiles[id_item].tile_index = transform_co_byt(item_co[1])