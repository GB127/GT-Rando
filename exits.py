from generic import world_indexes, room_to_index, world_indexes
from copy import deepcopy
from random import shuffle

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
        test = enter_room([], copy_exits, 0) 
        test.sort()

        return all_ids == test


    def __call__(self, keep_direction=False, move_boss=False, pair_exits=False):  #FIXME : Do pair_exits
        opposite = {    "N": "S",
                        "S": "N",
                        "W": "E",
                        "E": "W",
                        "↗": "↗"
                        }
        # FIXME: Uniformize the if/elif of keep_direction

        # Create a backup for loopings.
        new_screens_exits = deepcopy(self.screens_exits)  #FIXME : Change names

        boss_screen = self.data.levels[self.world_i].boss_screen_index
        for screen in deepcopy(self.screens_exits):
            try:
                if new_screens_exits[screen]["N"] == boss_screen and not move_boss:
                    self.screens_exits[screen] = {}
                    self.screens_exits[screen]["N"] = boss_screen
                    del new_screens_exits[screen]["N"]
                else:
                    self.screens_exits[screen] = {}
            except KeyError:
                self.screens_exits[screen] = {}

        # Fetch the data
        all_destinations = {} if keep_direction else []
        for screen in new_screens_exits:
            for direction in new_screens_exits[screen]:
                    if not keep_direction:                         
                        all_destinations += [new_screens_exits[screen][direction]]
                    elif keep_direction: 
                        all_destinations[direction] = all_destinations.get(direction, []) + [new_screens_exits[screen][direction]]


        # Randomization!
        if keep_direction:
            for direction in deepcopy(all_destinations):
                shuffle(all_destinations[direction])
        elif not keep_direction:
            shuffle(all_destinations)

        # Distribution des nouvelles destinations:
        for screen in new_screens_exits:
            for direction in new_screens_exits[screen]:
                if not keep_direction: access_destination = all_destinations
                elif keep_direction: access_destination = all_destinations[direction]
                new_destination = access_destination[0]
                
                self.screens_exits[screen][direction] = new_destination
                del access_destination[0]



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