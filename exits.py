from generic import world_indexes, room_to_index, world_indexes
from copy import deepcopy
from random import shuffle, choice

class Exits2:
    exits_type = {  "N":[4, 18, 20, 132, 146, 148],
                    "S":[68, 82, 84, 196, 210, 212],
                    "W":[98, 100, 226, 228],
                    "E":[34, 35, 36, 50, 162, 163, 164, 178],
                    "↗":[15, 143]}

    def __init__(self, data,world_i, screens_ids):
        self.data = data
        self.world_i = world_i
        self.screens_ids = screens_ids

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
            if not exits[new_location]:
                return ids
            else:
                copy_exits = deepcopy(exits)
                for direction, destination in exits[new_location].items():
                    del copy_exits[new_location][direction]
                for direction, destination in exits[new_location].items():
                    entered_ids = enter_room(entered_ids, copy_exits, destination)
                return ids
        
        all_ids = list(self.screens_exits.keys())
        copy_exits = deepcopy(self.screens_exits)
        for starting_screen in self.screens_exits:
            if starting_screen == self.data.levels[self.world_i].boss_screen_index:
                continue
            test = enter_room([], copy_exits, starting_screen) 
            test.sort()
            if all_ids == test: continue
            else: return False
        return True

    def __call__(self, keep_direction=False, move_boss=False, pair_exits=False):
        assert not move_boss, "Moving boss is not supported yet" # Comment this line when working on the move_boss.
        opposite = {    "N": "S",
                        "S": "N",
                        "W": "E",
                        "E": "W",
                        "↗": "↗"
                        }

        # Create a backup for loopings.
        boss_screen = self.data.levels[self.world_i].boss_screen_index

        backup_screens_exitws = deepcopy(self.screens_exits)

        # Prepare the empty data. Keep the boss at the vanilla place if needed.
        for screen in deepcopy(self.screens_exits):
            self.screens_exits[screen] = {}
            try:  # FIXME : Improve the code so it doesn't always do the try
                if backup_screens_exitws[screen]["N"] == boss_screen and not move_boss:
                    self.screens_exits[screen]["N"] = boss_screen
                    del backup_screens_exitws[screen]["N"]
                else:
                    vanilla_screen_to_boss = screen
            except KeyError:
                pass

        # Fetch the data for easy shuffling.
        all_destinations = {} if keep_direction else []
        for screen in backup_screens_exitws:
            for direction in backup_screens_exitws[screen]:
                    if keep_direction: 
                        all_destinations[direction] = all_destinations.get(direction, []) + [backup_screens_exitws[screen][direction]]
                    elif not keep_direction:
                        all_destinations += [backup_screens_exitws[screen][direction]]


        if move_boss:  # Immediately place the boss at the new location if moved.
            if keep_direction: boss_direction = "N"
            else: boss_direction = choice(["N", "S", "W", "E"])  # No stairs here because we can't lock a stair!
            all_possibilities = []
            for screen in backup_screens_exitws.keys():
                if boss_direction in backup_screens_exitws[screen]:
                    all_possibilities.append(screen)
            new_screen_to_boss = choice(all_possibilities)
            self.screens_exits[new_screen_to_boss][boss_direction] = boss_screen
            print(self.screens_exits)

            # FIXME : Clean up


        # Randomization!
        if keep_direction:
            for direction in deepcopy(all_destinations):
                shuffle(all_destinations[direction])
        elif not keep_direction:
            shuffle(all_destinations)





        # Distribution des nouvelles destinations:
        for screen in backup_screens_exitws:
            for direction in backup_screens_exitws[screen]:
                try:
                    self.screens_exits[screen][direction]
                    # Paired if this doesn't trigger the keyerror.
                except KeyError:
                    # Not setted yet.
                    if not keep_direction: access_destination = all_destinations
                    elif keep_direction: access_destination = all_destinations[direction]
                    new_destination = access_destination[0]
                    self.screens_exits[screen][direction] = new_destination
                    del access_destination[0]

                    if pair_exits and keep_direction:
                        self.screens_exits[new_destination][opposite[direction]] = screen # Works
                        all_destinations[opposite[direction]].remove(screen)

"""class Exits:
    def getUnlockedExits(self, currently_unlocked):
        new_unlocks = [0]*self.nExits
        boss_reached = 0
        for source_i in range(self.nExits):
            if self.world_i == 3 and source_i == 0 and currently_unlocked[2]==0: #first puzzle of the cave world
                new_unlocks[source_i] = currently_unlocked[source_i]
            elif self.world_i == 3 and source_i == 45 and currently_unlocked[48]==0: #last puzzle of the cave world
                new_unlocks[source_i] = currently_unlocked[source_i]
            ### one ways temporary fix ###
            elif self.world_i == 1 and source_i == 15 and currently_unlocked[16]==0: 
                new_unlocks[source_i] = currently_unlocked[source_i]
            elif self.world_i == 1 and source_i == 25 and currently_unlocked[26]==0: 
                new_unlocks[source_i] = currently_unlocked[source_i]
            elif self.world_i == 2 and source_i == 7 and currently_unlocked[8]==0: 
                new_unlocks[source_i] = currently_unlocked[source_i]
            elif self.world_i == 2 and source_i == 27 and currently_unlocked[26]==0: 
                new_unlocks[source_i] = currently_unlocked[source_i]
            elif self.world_i == 2 and source_i == 30 and currently_unlocked[29]==0: 
                new_unlocks[source_i] = currently_unlocked[source_i]
            elif self.world_i == 2 and source_i == 43 and currently_unlocked[44]==0: 
                new_unlocks[source_i] = currently_unlocked[source_i]
            elif self.world_i == 2 and source_i == 47 and currently_unlocked[48]==0: 
                new_unlocks[source_i] = currently_unlocked[source_i]
            ### end of temporary fix ###
            elif currently_unlocked[source_i]:
                destination_i = self.destination_exits[source_i]
                if destination_i == None:
                    boss_reached = 1
                else:
                    new_unlocks[source_i] = 1
                    new_unlocks[destination_i] = 1
        return new_unlocks, boss_reached
"""