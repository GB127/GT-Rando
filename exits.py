from lib2to3.pytree import Base
from generic import world_indexes, room_to_index, world_indexes
from copy import deepcopy
from random import shuffle, choice
import matplotlib.pyplot as plt
from random import shuffle

class one_exit:
    exits_type = { "N":[4, 18, 20, 132, 146, 148],
                    "S":[68, 82, 84, 196, 210, 212],
                    "W":[98, 100, 226, 228],
                    "E":[34, 35, 36, 50, 162, 163, 164, 178],
                    "↗":[15, 143]}
    opposite = {"N": "S",
                "S": "N",
                "W": "E",
                "E": "W",
                "↗": "↗"
                }

    def __init__(self, exit_data):
        self.destination = exit_data.dst_screen
        self.xy = exit_data.dst_x, exit_data.dst_y

        for direction in self.exits_type:
            if exit_data.type in self.exits_type[direction]:
                self.direction = direction
        if self.xy in [(200,66), (200,194), (120, 130), (152, 194), (24, 194), (88, 50), (104,50)]:
            self.spawn = '↗'
        elif self.xy[0] < 40:
            self.spawn = 'W'
        elif self.xy[0] > 180:
            self.spawn = 'E'
        elif self.xy[1] > 122:
            self.spawn = 'S'
        else:
            self.spawn = 'N'

    def __str__(self):
        return f'{self.destination} ({self.spawn})'




class Exits:
    def generate_data(self):
        self.exits = {}
        for B7, screen_id in enumerate(self.screens_ids):
            tempo = {}
            for exi in range(self.data.screens[screen_id].num_exits):
                data = self.data.screens[screen_id].exits[exi]
                tempo_exit = one_exit(data)
                tempo[tempo_exit.direction] = tempo_exit
            self.exits[B7] = tempo
        return self.exits

    def __init__(self, data, world_i, screens_ids):
        self.data = data
        self.world_i = world_i
        self.screens_ids = screens_ids
        self.boss_screen = self.data.levels[self.world_i].boss_screen_index
        self.generate_data()

    def __str__(self):
        def str_screen(dictio):
            liste = []
            for direction, sortie in dictio.items():
                liste.append(f'{direction}: {str(sortie)}')
            return "   ".join(liste)
        # Contruisons le tableau.
        table = ""
        count = 0  # Pour des sauts de lignes.
        for B7, data in self.generate_data().items():
            count += 1
            table += f'{str(B7):>3} : {str_screen(data):45}'
            if count % 2 == 0:  # Si le tableau est trop large, réduire ce chiffre.
                table += "\n"

        return f'{table}'


    def __call__(self,  randomize:bool, 
                        keep_direction=False,
                        move_boss=False,
                        pair_exits=False):
        """Randomize the exits.

        Args:
            randomize (bool):  Activate the randomizer or not.
            keep_direction (bool, optional)
            move_boss (bool, optional): NOTIMPLEMENTED
            pair_exits (bool, optional)
            NEW ARGUMENT FOR checking if RANDOMIZING LOCKED DOORS because some exits will need to stay
        """
        def exits_list():
            """Retrieve all exits. And Returns a list of the exits."""
            # Fetch the data for easy shuffling.
            randomized_exits = []
            for screen in self.exits.keys():
                for direction in self.exits[screen]:
                        if self.exits[screen][direction] == self.boss_screen: continue
                        randomized_exits += [self.exits[screen][direction]]
            return randomized_exits

        def clear_exits():
            """Sets all destinations and landing coordinates to 255. Used for an "if...". Logically, it means that it's cleared."""
            for screen_id in self.screens_ids:
                for exi in range(self.data.screens[screen_id].num_exits):
                    self.data.screens[screen_id].exits[exi].dst_screen = 255
                    self.data.screens[screen_id].exits[exi].dst_x, self.data.screens[screen_id].exits[exi].dst_y = 255,255

        def set_boss_exit():
            """Manually set the vanilla boss exit."""
            boss_exit = next(x for x in all_exits if x.destination == self.boss_screen > 3)
            van_screen_to_boss= [   room_to_index(tup=(0,12)),
                                    room_to_index(tup=(1,14)),
                                    room_to_index(tup=(2,24)),
                                    room_to_index(tup=(3,24)),
                                    room_to_index(tup=(4,24))][self.world_i]
            self.data.screens[van_screen_to_boss].exits[0].dst_screen = boss_exit.destination
            self.data.screens[van_screen_to_boss].exits[0].dst_x, self.data.screens[van_screen_to_boss].exits[0].dst_y = boss_exit.xy 
            all_exits.remove(boss_exit)
        
        def next_exit(exit_type):
            """Returns the correct exit to be set. it only checks if keep direction is True."""
            exits_type = {  "N":[4, 18, 20, 132, 146, 148],
                    "S":[68, 82, 84, 196, 210, 212],
                    "W":[98, 100, 226, 228],
                    "E":[34, 35, 36, 50, 162, 163, 164, 178],
                    "↗":[15, 143]}
            if keep_direction:
                for direction in exits_type:
                    if exit_type in exits_type[direction]:
                        desired_direction = direction
                return next(x for x in all_exits if x.direction == desired_direction)             
            return all_exits[0]

        def back_exit(screen_id, exit_type):
            exits_type = {"N":[4, 18, 20, 132, 146, 148],
                    "S":[68, 82, 84, 196, 210, 212],
                    "W":[98, 100, 226, 228],
                    "E":[34, 35, 36, 50, 162, 163, 164, 178],
                    "↗":[15, 143]}
            for direction in exits_type:
                if exit_type in exits_type[direction]:
                    desired_direction = direction
            return next(x for x in all_exits if ((x.destination == room_to_index(id=screen_id)[1]) and (x.spawn == desired_direction)))

        def pairer(current_screen_id, exit_type, initial_exit):
            exits_type = { "N":[4, 18, 20, 132, 146, 148],
                            "S":[68, 82, 84, 196, 210, 212],
                            "W":[98, 100, 226, 228],
                            "E":[34, 35, 36, 50, 162, 163, 164, 178],
                            "↗":[15, 143]}
            return_exit = back_exit(current_screen_id, exit_type)

            dest_screen_id = room_to_index(tup=(self.world_i, initial_exit.destination))
            for exi_id in range(self.data.screens[dest_screen_id].num_exits):
                for cle, valeurs in exits_type.items():
                    if self.data.screens[room_to_index(tup=(self.world_i, initial_exit.destination))].exits[exi_id].type in valeurs:
                        current_dir = cle
                        break
                if initial_exit.spawn == current_dir:
                    self.data.screens[dest_screen_id].exits[exi_id].dst_screen = return_exit.destination
                    self.data.screens[dest_screen_id].exits[exi_id].dst_x, self.data.screens[dest_screen_id].exits[exi_id].dst_y = return_exit.xy
                    break
            all_exits.remove(return_exit)




        if not randomize: return
        assert not move_boss, "Moving boss is not supported yet" # Comment this line when working on the move_boss.

        all_exits = exits_list()
        clear_exits()
        set_boss_exit()

        # shuffle(all_exits)  # need to fix world 1 and 3 with their unused exit, mthen it should be ready.
        
        for screen_id in self.screens_ids:
            for exi in range(self.data.screens[screen_id].num_exits):
                # Check if exit already set before.
                if self.data.screens[screen_id].exits[exi].dst_screen != 255:
                    continue

                new_exit = next_exit(self.data.screens[screen_id].exits[exi].type)
                self.data.screens[screen_id].exits[exi].dst_screen = new_exit.destination
                self.data.screens[screen_id].exits[exi].dst_x, self.data.screens[screen_id].exits[exi].dst_y = new_exit.xy
                all_exits.remove(new_exit)

 
                if pair_exits:
                    pairer(screen_id, self.data.screens[screen_id].exits[exi].type, new_exit)
