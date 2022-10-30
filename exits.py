from generic import world_indexes, room_to_index, world_indexes
from random import shuffle
from random import shuffle
from copy import deepcopy
import networkx as net # version 2.5

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

    def nodes(self):
        # TODO : REPLACE THESE FUNCTION IN THE LOOPS TO REDUCE LOOPAGE
        def world_0_DE():
            """Dead-ends for plank and shovel"""
            if self.world_i == 0:
                for B7, screen in enumerate(self.screens_ids):
                    for sortie in self[screen]:
                        if B7 == sortie.destination : continue
                        if sortie.destination == 7 and sortie.spawn == "W":
                            g.remove_edge(B7, 7)
                            g.remove_edge(7, B7)
                            net.add_path(g, [B7, B7])
                        elif sortie.destination == 9 and sortie.spawn == "S":
                            g.remove_edge(B7, 9)
                            g.remove_edge(9, B7)
                            net.add_path(g, [B7, B7])

        def world_2_DE():
            """Dead ends for fruits / gem in B7 = 8"""
            if self.world_i == 2:
                for B7, screen in enumerate(self.screens_ids):
                    for sortie in self[screen]:
                        if B7 == sortie.destination : continue
                        if sortie.destination == 8 and sortie.spawn == "S":   # Works!
                            g.remove_edge(B7, 8)
                            g.remove_edge(8, B7)
                            net.add_path(g, [B7, B7])

                        if sortie.destination == 8 and sortie.spawn == "↗":
                            try:
                                g.remove_edge(B7, 8)
                                g.remove_edge(8, B7)
                                net.add_path(g, [B7, B7])
                            except:  # Si on lève cette erreur, c'est à coup sûr que c'est 14.
                                g.remove_edge(14, 8)
                                net.add_path(g, [14, 14])

        g = net.DiGraph()
        for B7, screen in enumerate(self.screens_ids):
            for sortie in self[screen]:

                # World 1: The infamous double hookshot screen. We do not want
                    # To land here without hookshot. So I must assume that someone
                    # Never grabs an item. To do so, I assume it's unidirect to the north.
                if self.world_i == 1:
                    if sortie.destination == 13 and sortie.spawn == "N":
                        continue

                # World 2 : Bypass for 14 to 13.
                    # Nomally it's 14 -> 13 -> Stair exit
                    # Adjust for logic : 14 -> Stair exit
                elif self.world_i == 2:
                    if B7 == 13: # Pièce de bille : For the bombable wall and the stair
                        if sortie.destination == 14:
                            continue  # No return because it's a wall and it must be uni
                        if sortie.direction == "↗":
                            continue # Don't set, because of the bypass
                    if B7 == 14:  # For the bombable wall and the bypass
                        if sortie.destination == 13:
                            B7_13 = room_to_index(tup=(2,13))
                            net.add_path(g, [B7, self[B7_13, 3].destination])  # Bypass for logic check
                            continue

                elif self.world_i == 3:  # Both puzzles that opens a door on North.
                    if sortie.destination == 16 and sortie.spawn == "N":
                        continue
                    if sortie.destination == 17 and sortie.spawn == "N":
                        continue


                elif self.world_i == 4: 
                    # Make the platform unidirect! When reimplemented, will use a bool.
                    if sortie.destination == 18 and sortie.spawn == "E":
                        continue
                net.add_path(g, [B7, sortie.destination])

        world_0_DE()
        world_2_DE()
        return g

    def __bool__(self):
        """Returns True if all screens can be reached from the start."""
        if self.world_i == 1:
            if self[7,2].destination == 7 and self[7,2].spawn == "W":
                raise BaseException("7 DEAD END : INACCESSIBLE ITEM, DID IT WORK?")
                return False
            if self[9, 1].destination == 9 and self[9, 1].spawn == "S":
                raise BaseException("9 SHOVEL DEAD END : INACCESSIBLE ITEM, DID IT WORK?")
                return False
        # TODO : SAME FOR CASTLE


        g = self.nodes()
        nodes = net.shortest_path(g,0).keys()  #TODO : Once we can change the first screen, the 0 will be that screen.
        if len(self.screens_ids) != len(nodes):
            return False

        
        if self.world_i == 3:  # Make sure Room #1 is accessible from the start.
            g.remove_edge(0, self[room_to_index(tup=(3,0)), 0].destination)
            if 1 not in net.shortest_path(g,0).keys():  # TODO : Once we can change the starting room, change the 0 here.
                return False

        if self.world_i == 4:  # Make sure the gold key is required.
            g.remove_node(20)
            try:
                net.shortest_path(g, 0, 25)
                return False
            except:
                pass

        if self.world_i == 4:  # Make sure we can come back, assuming we skip all items.
            # À modifier avec un futur bool quand la plateforme sera réimplementé
            try:
                net.shortest_path(g,self[room_to_index(tup=(4, 18)),0].destination, 18)
            except:  # Pas de chemin de retour.
                return False
        return True

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

    def exit_type(self, screen_id, exit_id):
        return self.data.screens[screen_id].exits[exit_id].type

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
