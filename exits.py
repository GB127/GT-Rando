from generic import room_to_index
from random import shuffle
from random import shuffle
from copy import deepcopy
import networkx as net # version 2.5

from itertools import permutations

def exit_type_str(chiffre):
    exits_type = { "N":[4, 18, 20, 132, 146, 148],
                    "S":[68, 82, 84, 196, 210, 212],
                    "W":[98, 100, 226, 228],
                    "E":[34, 35, 36, 50, 162, 163, 164, 178],
                    "↗":[15, 143]}
    for direction in exits_type:
        if chiffre in exits_type[direction]:
            return direction

class one_exit:
    opposite = {"N": "S",
                "S": "N",
                "W": "E",
                "E": "W",
                "↗": "↗"
                }

    def __bool__(self):
        return self.destination != 255

    def __init__(self, exit_data):
        self.destination = exit_data.dst_screen
        self.xy = exit_data.dst_x, exit_data.dst_y

        self.direction = exit_type_str(exit_data.type)
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



    def clear(self):
        self.destination = 255
        self.xy = 255, 255


class Exits:
    def __init__(self, data, world_i, screens_ids):
        self.data = data
        self.world_i = world_i
        self.screens_ids = screens_ids
        self.boss_screen = self.data.levels[self.world_i].boss_screen_index

        if self.world_i == 1:
            self.data.screens[room_to_index(tup=(1, 15))].num_exits = 0
            self.data.screens[room_to_index(tup=(1, 13))].num_exits = 2
            self.data.screens[room_to_index(tup=(1, 13))].exits[1] = self.data.screens[room_to_index(tup=(1, 13))].exits[2]
        elif self.world_i == 3:
            self.data.screens[room_to_index(tup=(3, 1))].num_exits = 1
            self.data.screens[room_to_index(tup=(3, 1))].exits[0] = self.data.screens[room_to_index(tup=(3, 1))].exits[1]

    def __str__(self):
        def generate_data():
            self.exits = {}
            for B7, screen_id in enumerate(self.screens_ids):
                tempo = {}
                for exi in range(self.data.screens[screen_id].num_exits):
                    data = self.data.screens[screen_id].exits[exi]
                    tempo_exit = one_exit(data)
                    tempo[tempo_exit.direction] = tempo_exit
                self.exits[B7] = tempo
            return self.exits

        def str_screen(dictio):
            liste = []
            for direction, sortie in dictio.items():
                liste.append(f'{direction}: {str(sortie)}')
            return "   ".join(liste)
        # Contruisons le tableau.
        table = ""
        count = 0  # Pour des sauts de lignes.
        for B7, data in generate_data().items():
            count += 1
            table += f'{str(B7):>3} : {str_screen(data):45}'
            if count % 2 == 0:  # Si le tableau est trop large, réduire ce chiffre.
                table += "\n"

        return f'{table}'

    def __len__(self):
        total = 0
        for screen in self.screens_ids:
            total += self.data.screens[screen].num_exits
        return total

    def __iter__(self):
        toreturn = []
        for screen in self.screens_ids:
            for exi in range(self.data.screens[screen].num_exits):
                sortie = one_exit(self.data.screens[screen].exits[exi])
                toreturn.append(sortie)
        return iter(toreturn)

    def __getitem__(self, screen_exit_id):
        # TODO : Use room_to_index here
        if isinstance(screen_exit_id, tuple):
            screen_id = screen_exit_id[0]
            exit_id = screen_exit_id[1]
        else:
            screen_id = screen_exit_id
            exit_id = None
        exits = []
        for exi in range(self.data.screens[screen_id].num_exits):
            exits.append(one_exit(self.data.screens[screen_id].exits[exi]))
        if isinstance(exit_id,int):
            return exits[exit_id]
        return exits

    def __setitem__(self, screen_exit_id, new_exit):
        screen_id = screen_exit_id[0]
        exit_id = screen_exit_id[1]

        for exi in range(self.data.screens[screen_id].num_exits):
            if exit_id == 0:
                self.data.screens[screen_id].exits[exi].dst_screen = new_exit.destination
                self.data.screens[screen_id].exits[exi].dst_x, self.data.screens[screen_id].exits[exi].dst_y = new_exit.xy
                break
            exit_id -= 1

    def __call__(self,  randomize:bool, 
                        keep_direction:bool=True,
                        move_boss:bool=False,
                        pair_exits:bool=True):
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
            for screen in self.screens_ids:
                randomized_exits += self[screen]
            return randomized_exits
        def clear_exits():
            for screen in self.screens_ids:
                for current_id, current_exit in enumerate(self[screen]):
                    current_exit.clear()
                    self[screen, current_id] = current_exit
        

        def back_exit(screen_id, exit_type):
            desired_direction = exit_type_str(exit_type)
            tempo = next(x for x in all_exits if ((x.destination == room_to_index(id=screen_id)[1]) and (x.spawn == desired_direction)))
            return tempo

        def pairer(current_screen_id, exit_type, initial_exit):
            dest_screen_id = room_to_index(tup=(self.world_i, initial_exit.destination))

            for exi_id, exit in enumerate(self[dest_screen_id]):
                current_dir = exit_type_str(self.data.screens[room_to_index(tup=(self.world_i, initial_exit.destination))].exits[exi_id].type)

                if initial_exit.spawn == current_dir:
                    try:
                        return_exit = back_exit(current_screen_id, exit_type)
                        self[dest_screen_id, exi_id] = return_exit
                        all_exits.remove(return_exit)
                    except StopIteration:
                        break
                    break


        def next_exit(exit_type):
            """Returns the correct exit to be set. it only checks if keep direction is True."""
            if keep_direction:
                desired_direction = exit_type_str(exit_type)
                return next(x for x in all_exits if x.direction == desired_direction)
            return all_exits[0]

        def set_boss_exit():
            """Manually set the vanilla boss exit."""
            boss_exit = next(x for x in all_exits if x.destination == self.boss_screen)
            van_screen_to_boss= [   room_to_index(tup=(0,12)),
                                    room_to_index(tup=(1,14)),
                                    room_to_index(tup=(2,24)),
                                    room_to_index(tup=(3,24)),
                                    room_to_index(tup=(4,24))][self.world_i]
            self[van_screen_to_boss, 0] = boss_exit
            all_exits.remove(boss_exit)

        def set_fixed_exits():
            """Manually set the breakable wall exit to avoid a softlock"""
            if self.world_i == 2:
                wall_exit = next(x for x in all_exits if (x.destination == 13 and x.spawn == "E"))
                self[room_to_index(tup=(2,14)), 1] = wall_exit
                all_exits.remove(wall_exit)

                wall_exit = next(x for x in all_exits if (x.destination == 14 and x.spawn == "W"))
                self[room_to_index(tup=(2,13)), 0] = wall_exit
                all_exits.remove(wall_exit)

            # For the castle : 0 Always lead to south of 1. And vice versa.
            if self.world_i == 2:
                wall_exit = next(x for x in all_exits if (x.destination == 1 and x.spawn == "S"))
                self[room_to_index(tup=(2,0)), 0] = wall_exit
                all_exits.remove(wall_exit)

                wall_exit = next(x for x in all_exits if (x.destination == 0 and x.spawn == "N"))
                self[room_to_index(tup=(2,1)), 2] = wall_exit
                all_exits.remove(wall_exit)

            """Manually set the waterfall to always lead to "that" room."""
            if self.world_i == 3:  # The waterfall always lead to the boss.
                fall_exit = next(x for x in all_exits if (x.destination == 24 and x.spawn == "S"))
                self[room_to_index(tup=(3,22)), 0] = fall_exit
                all_exits.remove(fall_exit)

                fall_exit = next(x for x in all_exits if (x.destination == 22 and x.spawn == "N"))
                self[room_to_index(tup=(3,24)), 1] = fall_exit
                all_exits.remove(fall_exit)



        def set_locked_doors():
            """Temporary function that will fix some exits that are locked on both sides. Once we can move locked doors,
                this will disappear."""
            if self.world_i == 0:
                wall_exit = next(x for x in all_exits if (x.destination == 5 and x.spawn == "N"))
                self[room_to_index(tup=(0,8)), 1] = wall_exit
                all_exits.remove(wall_exit)

                wall_exit = next(x for x in all_exits if (x.destination == 8 and x.spawn == "S"))
                self[room_to_index(tup=(0,5)), 0] = wall_exit
                all_exits.remove(wall_exit)
            if self.world_i == 1:  # Fix the vanilla door that works on both side to the vanilla one.
                wall_exit = next(x for x in all_exits if (x.destination == 12 and x.spawn == "S"))
                self[room_to_index(tup=(1,10)), 0] = wall_exit
                all_exits.remove(wall_exit)

                wall_exit = next(x for x in all_exits if (x.destination == 10 and x.spawn == "N"))
                self[room_to_index(tup=(1,12)), 1] = wall_exit
                all_exits.remove(wall_exit)


        if not randomize: return
        assert not move_boss, "Moving boss is not supported yet" # Comment this line when working on the move_boss.

        exits_pools = exits_list()
        while True:
            all_exits = deepcopy(exits_pools)
            clear_exits()
            set_boss_exit()
            set_fixed_exits()
            set_locked_doors()
            shuffle(all_exits)
            for screen_id in self.screens_ids:
                for exit_id in range(len(self[screen_id])):
                    current_exit = self[screen_id, exit_id]
                    if current_exit:
                        continue
                    new_exit = next_exit(self.exit_type(screen_id, exit_id))
                    self[screen_id, exit_id] = new_exit
                    all_exits.remove(new_exit)
                    if pair_exits:
                        pairer(screen_id, self.data.screens[screen_id].exits[exit_id].type, new_exit)
            if self:
                break

    def __bool__(self):
        """Bool that checks if all exits are reachable."""
        def B7s_tocouple():
            """Check for the Cave puzzle (because it's the only B7s that are progression)."""
            data = {58:(59, (str(self[58,0]),"0 (N)"), ("0 (N)", "1 (E)")), # World 3 : 0 locked door : see if puzzle reachable without going to north!
                    80:(81, ("22 (S)", "22 (N)"), ('22 (S)', "23 (W)"))  # World 3 : Waterfall and the puzzle room!
                        }
            # data Format : {Screen : (Screen2, (Spawn1, Spawn2), (Exit1, Exit2))} 
                # Screen1 : Screen where we need to start the check.
                # Screen2 : Destination screen we need to have on same world.
                # Spawn1 & Spawn2 : Spawns on Screen1 we need to remove the link
                # Exit1 & Exit2 : Exits to use to see if we can reach Exit2 from Exit1
                    # NOTE : Exit1 is on Screen1
            for screen_to_check, infos in data.items():
                if screen_to_check in self.screens_ids:
                    # Check if screen to pair is in the same world. (Currently, will always work).
                        # If implemented, this will be moved elsewhere!
                    B7_to_couple = infos[0]
                    assert B7_to_couple in self.screens_ids, "Looks like we can randomize screens now? This is a failsafe check"
                    copy_g = deepcopy(g)
                    
                    # Remove the link we need to remove.
                    link_to_remove = infos[1]
                    for exit1, exit2 in permutations(link_to_remove, 2):
                        try:
                            copy_g.remove_edge(exit1, exit2)
                        except net.NetworkXError:  
                        # This happens when we don't pair exits. With this, we simply only remove the
                        # out.
                            continue

                    # See if we can reach the goal. Raises an error if unreachable.
                    path_to_find = infos[2]
                    net.shortest_path(copy_g, path_to_find[0], path_to_find[1])

        g = self.nodes()
        try:
            B7s_tocouple()
        # Check if all exits are accessible from the start.
            return all([str(x) in net.shortest_path(g, str("0 (N)")) for x in self])
        except net.NetworkXNoPath:
            return False

    def nodes(self):
        def apply_internal_links(screen:int, exits_str):
            screens_data = {
                            7 :[(0, 1), (1,0)],  # 7 : W0 Plank Screen 
                            9 :[(0, 2), (2, 0)],  # 9 : W0 Shovel Screen
                            40:[(0,2), (2,0)],  # W2 : Corridor screen with fruits on south and gems on top
                            45:[(1, 2), (2, 1), (0, 3), (3, 0)],  # W2 : Boulder screen with breakable wall on top right and stair
                            74:[(1,0)],  # W3 : puzzle with 1 Enemy in center
                            75:[(1,0)],  # W3 : Puzzle with a zig zag section
                            80:[(2,0), (0,2), (1,2), (2,1)],  # W3 : Waterfall, to ease logic
                            93:[(1, 0)],  # W4 : Puzzle that opens a door to the right
                            97:[(0,1), (1,0), (1,2), (2,1)],  # W4 : Room with two hookshot spots. Not the cannon one
                            99: [(0,1), (1, 0), (0, 2), (2,0)],  # W4 : Room with 2 buttons. This is to make logic easier.
                            100:[(0, 2), (2,0), (2, 1), (1,2), (0, 1)],  #W4 : Room with the fire blower.
                            106:[(1, 0)], #W4 : Arrow platform room
                            110:[(0,1), (1,0), (1,2), (2,1)]  # W4 : Wheel puzzle room
                            }
            screens_c = [23,  #W1 Hookshot + plank screen 
                        29, # W1 double hookshot
                        42, # Castle double plank
                        109 # Pirate double hookshot & canons 
                        ]
            if screen in screens_data:
                for sortie_1_id, sortie_2_id in screens_data[screen]:
                    net.add_path(g, [exits_str[sortie_1_id], exits_str[sortie_2_id]])
            elif screen in screens_c:
                center_spawn = f'{int(exits_str[0][:2])} (C)'
                for spawn in exits_str:
                    net.add_path(g, [spawn, center_spawn])
                    net.add_path(g, [center_spawn, spawn])
            else:
                for sortie_1, sortie_2 in permutations(exits_str, 2):
                    net.add_path(g, [sortie_1, sortie_2])

        g = net.DiGraph()
        for B7, screen in enumerate(self.screens_ids):
            this_screen_exit = []
            for sortie in self[screen]:
                starting = f'{B7} ({sortie.direction})'
                net.add_path(g, [starting, str(sortie)])
                this_screen_exit.append(starting)
            apply_internal_links(screen, this_screen_exit)
        return g

    def exit_type(self, screen_id, exit_id):
        return self.data.screens[screen_id].exits[exit_id].type

    def find(self, spawn):
        for B7, screen in enumerate(self.screens_ids):
            for exi in range(self.data.screens[screen].num_exits):
                sortie = one_exit(self.data.screens[screen].exits[exi])
                if str(sortie) == spawn:
                    return f"{B7} ({sortie.direction})"
