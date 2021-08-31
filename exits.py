from generic import world_indexes, room_to_index, world_indexes
from copy import deepcopy
from random import shuffle, choice

class Exits:
    exits_type = {  "N":[4, 18, 20, 132, 146, 148],
                    "S":[68, 82, 84, 196, 210, 212],
                    "W":[98, 100, 226, 228],
                    "E":[34, 35, 36, 50, 162, 163, 164, 178],
                    "↗":[15, 143]}

    def __init__(self, data,world_i, screens_ids):
        self.data = data
        self.world_i = world_i
        self.screens_ids = screens_ids
        self.boss_screen = self.data.levels[self.world_i].boss_screen_index


        self.screens_exits = {}

        for B7, screen_id in enumerate(screens_ids):
            tempo = {}
            for exi in range(self.data.screens[screen_id].num_exits):
                for direction, values in self.exits_type.items():
                    if self.data.screens[screen_id].exits[exi].type in values:
                        tempo[direction] = self.data.screens[screen_id].exits[exi].dst_screen
                        break
            self.screens_exits[B7] = tempo


    def __str__(self):
        # Contruisons le tableau.
        table = ""
        count = 0  # Pour des sauts de lignes.
        for B7 in self.screens_exits:
            count += 1
            table += f'{str(B7):>3} : {str(self.screens_exits[B7]):40}'
            if count % 3 == 0:  # Si le tableau est trop large, réduire ce chiffre.
                table += "\n"
        Accessibility = "All rooms are accessible" if self.all_rooms_accessible() else "There is a closed loop"
        return f'{table}\n{Accessibility}'


    def all_rooms_accessible(self):
        """Return a bool.
            True : All room are accessible
            False : A room cannot be accessed (closed cloop somewhere)
        """
        def enter_room(ids, exits, new_location):
            entered_ids = ids
            if new_location not in entered_ids:
                entered_ids.append(new_location)
            if not exits[new_location]:  # All exits have been visited in this location
                return ids
            else:  # There are some exits not visited yet.
                copy_exits = deepcopy(exits)
                for direction, destination in exits[new_location].items():
                    del copy_exits[new_location][direction]
                for direction, destination in exits[new_location].items():
                    entered_ids = enter_room(entered_ids, copy_exits, destination)
                return ids
        
        for starting_screen in self.screens_exits:
            if starting_screen ==  self.boss_screen: # We do not want to check accessibility from boss screen.
                continue
            accessible_B7 = enter_room([], deepcopy(self.screens_exits), starting_screen)
            if list(self.screens_exits.keys()) == sorted(accessible_B7): continue
            return False
        return True

    def __call__(self,  randomize=False, 
                        keep_direction=False,
                        move_boss=False,
                        pair_exits=False):
        def assemble_exits(keep_direction):
            # Fetch the data for easy shuffling.
            randomized_exits = {} if keep_direction else []
            for screen in self.screens_exits.keys():
                for direction in self.screens_exits[screen]:
                        if self.screens_exits[screen][direction] == self.boss_screen: continue
                        elif keep_direction:
                            randomized_exits[direction] = randomized_exits.get(direction, []) + [self.screens_exits[screen][direction]]
                        elif not keep_direction:
                            randomized_exits += [self.screens_exits[screen][direction]]
            return randomized_exits

        def randomize_exits(exits, keep_direction):
            if keep_direction:
                for direction in exits.keys():
                    shuffle(exits[direction])
            elif not keep_direction:
                shuffle(exits)

        def create_empty_data():
            empty_data = {}
            for screen in self.screens_exits.keys():
                empty_data[screen] = {}
                for direction in self.screens_exits[screen]:
                    empty_data[screen][direction] = {}
                    try:
                        if self.screens_exits[screen]["N"] == self.boss_screen:
                            empty_data[screen]["N"] = self.boss_screen
                    except KeyError: pass
            return empty_data

        def distribute_exits(empty_list, randomized_exits, pair_exits, keep_direction):
            opposite = {    "N": "S",
                        "S": "N",
                        "W": "E",
                        "E": "W",
                        "↗": "↗"
                        }

            loop_exits = deepcopy(empty_list)
            for screen in loop_exits:
                for direction in loop_exits[screen]:
                    if not empty_list[screen][direction]:
                        if not keep_direction: access_destination = randomized_exits
                        elif keep_direction: access_destination = randomized_exits[direction]

                        new_destination = access_destination[0]
                        empty_list[screen][direction] = new_destination
                        del access_destination[0]

                        if pair_exits and keep_direction:
                            empty_list[new_destination][opposite[direction]] = screen # Works
                            randomized_exits[opposite[direction]].remove(screen)
            self.screens_exits = empty_list

        if not randomize: return
        assert not move_boss, "Moving boss is not supported yet" # Comment this line when working on the move_boss.

        empty_data = create_empty_data()
        all_exits = assemble_exits(keep_direction)
        
        randomize_exits(all_exits, keep_direction=keep_direction)
        distribute_exits(empty_data, all_exits, pair_exits, keep_direction)
