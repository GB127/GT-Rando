from generic import world_indexes, room_to_index
from items import Items
from exits import Exits

class World2():
    def __init__(self, data, world_i):
        self.world_i = world_i
        self.data = data

        self.Exits = Exits(self.data,self.world_i, world_indexes(self.world_i))
        self.Items = Items(self.data, self.world_i, world_indexes(self.world_i))


    def print_screen(self, B7):
        def transform_byt_co(big_value):
            assert big_value <= 0x6bc and big_value >=0, "Byte value must be 0 to 0x6BC"
            assert big_value % 2 == 0, "Byte value must be pair, else it will appear gliched."

            y = ( big_value // 0x40) / 2
            x = (big_value % 0x40) / 2
            return x/2, y

        def get_interactives(screen_id):
            screen_data = self.data.screens[screen_id]
            interactives = []
            for id in range(screen_data.num_itiles):
                objet = screen_data.itiles[id]
                interactives.append((objet.type, transform_byt_co(objet.tile_index)))
            return interactives


        screen_id = room_to_index(tup=(self.world_i, B7))


        interactives_string = {
            0x0 : "W",
            0x2 : "A",
            0x4 : "E",
            0x6 : "S",
            0x8 : "P",
            0xA : "B",
            0xC : "L",
            0xE : "2",
            0x10 : "I",
            0x12 : "C",
            0x14 : "T",
            0x16 : "R",
            0x18 : "r",
            0x1A : "X",
            0x1C : "G",
            0x1E : "O",
            0x20 : "R"
            }

        boundary_top = "_" * 34
        boundary_bottom = "¯" * 34


        string_list = []
        for y in range(28):
            tempo = [" " for _ in range(32)]
            # ...
            for interactive in get_interactives(screen_id):
                typ = interactive[0]
                inter_x = interactive[1][0]
                inter_y = interactive[1][1] 
                if 2* inter_y == y or (2 * inter_y +1) == y:
                    tempo[int(2 * inter_x)] = interactives_string[typ]
                    tempo[int(2* inter_x) + 1] = interactives_string[typ]


            new_str = "|" + "".join(tempo) + "|"
            string_list.append(new_str)

        print(boundary_top)
        print("\n".join(string_list))
        print(boundary_bottom)


class World():
    def __init__(self, data, world_i, starting_exit=0):
        # Doors related
        self.doors = Doors(data, world_i, self.exits)

        self.frames = Frames(data, 
                            world_i, 
                            self.exits.source_frames,
                            self.items.frames
                            )

    def randomizeFirstFrame(self):
        all_nFrames = [16, 16, 26, 30, 26]  # Number of frames per world.
        boss_frame = [14, 15, 25, 25, 25][self.world_i]
        frames = list(range(all_nFrames[self.world_i]))
        boss_frame_index = frames.index(boss_frame)
        frames.remove(boss_frame_index)
        while True:
            try:
                self.starting_frame = random.choice(frames)

                all_exits = list(enumerate(self.exits.destination_frames))
                locked_exits = self.doors.locked_exits
                locked_exits.sort(reverse=True)
                for locked_exit in locked_exits:
                    all_exits.pop(locked_exit)
                valid_exits_i = []
                for exit in all_exits:
                    if exit[1] == self.starting_frame:
                        valid_exits_i.append(exit[0])

                starting_exit = random.choice(valid_exits_i)

                self.starting_frame = self.exits.source_frames[starting_exit]
                self.initial_frame_coordinates_offsets, self.initial_frame_coordinates = self.setStartingExit(starting_exit)
                return self.initial_frame_coordinates_offsets, self.initial_frame_coordinates
            except:
                pass


    def randomizeFirstExit(self):
        boss_exit = self.exits.boss_exit
        all_exits = list(range(self.nExits))
        all_exits.remove(boss_exit)
        for locked_exit in self.doors.locked_exits:
            if locked_exit in all_exits:
                all_exits.remove(locked_exit)
        starting_exit = random.choice(all_exits)

        self.starting_frame = self.exits.source_frames[starting_exit]
        self.initial_frame_coordinates_offsets, self.initial_frame_coordinates = self.setStartingExit(starting_exit)
        return self.initial_frame_coordinates_offsets, self.initial_frame_coordinates

    def setStartingExit(self, starting_exit):
        self.starting_exit = starting_exit
        [offset_x_goofy, offset_y_goofy, offset_x_max, offset_y_max] = self.initial_frame_coordinates_offsets
        if starting_exit == 0:
            self.initial_frame_coordinates_offsets, self.initial_frame_coordinates =self.initial_frame_coordinates_offsets_vanilla, self.initial_frame_coordinates_vanilla
        else:
            self.initial_frame_coordinates_offsets, self.initial_frame_coordinates =[offset_x_goofy, offset_y_goofy, offset_x_max, offset_y_max], [self.exits.source_Xpos[starting_exit], self.exits.source_Ypos[starting_exit], self.exits.source_Xpos[starting_exit], self.exits.source_Ypos[starting_exit]]
        return self.initial_frame_coordinates_offsets, self.initial_frame_coordinates

    
    def feasibleWorldVerification(self):
        early_boss_indicator = -0.1
        unlocked_exits = [0]*self.nExits
        unlocked_exits[self.starting_exit] = 1 #means that we have access to this exit at the start
        used_items = [0]*self.nItems
        items_filled_conditions = [0]*len(self.items.conditions_types) #means that we already put none of the the bridges and hooks to reach the items
        items_filled_conditions[0] = 1 # element 0 should always be set to 1 in this list
        frames_filled_conditions = [0]*len(self.frames.conditions_types) #means that we already put none of the the bridges and hooks to reach the exits
        frames_filled_conditions[0] = 1 # element 0 should always be set to 1 in this list
        for big_step in range(50): #max number or loops
            for small_step in range(100): #how much exploration before we unlock something

                #for faster verification
                last_unlocked_exits = deepcopy(unlocked_exits)

                #exits links
                unlocked_exits, boss_reached = self.exits.getUnlockedExits(unlocked_exits)
                if boss_reached and early_boss_indicator == -0.1:
                    unlocked_items = self.items.getUnlockedItems(unlocked_exits, items_filled_conditions)
                    early_boss_indicator = (sum(unlocked_items)+sum(unlocked_exits))/(len(unlocked_items)+len(unlocked_exits))
                    early_boss_indicator = self.bossKeyAlreadyUsed(used_items)*early_boss_indicator #Always too early if the boss key was not used
                #internal frame links
                unlocked_exits = self.frames.getUnlockedExits(unlocked_exits, frames_filled_conditions)

                #for faster verification
                if last_unlocked_exits == unlocked_exits:
                    break

            previous = deepcopy(used_items)
            #unlocked items
            unlocked_items = self.items.getUnlockedItems(unlocked_exits, items_filled_conditions)

            #We now have to unlock something in order to move further?
            #what can we unlock right now?
            frames_reachable_conditions, items_reachable_conditions = self.getReachableConditions(unlocked_exits, frames_filled_conditions, items_filled_conditions)
            frames_unlockable_conditions, items_unlockable_conditions = self.getUnlockableConditions(frames_reachable_conditions, items_reachable_conditions, unlocked_items, used_items)
            
            #Check for softlocks
            if self.softlockIsPossible(frames_reachable_conditions, items_reachable_conditions, unlocked_items):
                break
            
            #randomly chose which condition to unlock
            if len(frames_unlockable_conditions)+len(items_unlockable_conditions)>0:
                random_i = random.randint(0, len(frames_unlockable_conditions)+len(items_unlockable_conditions)-1)
                if random_i<len(frames_unlockable_conditions): #we unlock a frame condition
                    condition_i = frames_unlockable_conditions[random_i]
                    frames_filled_conditions, used_items = self.unlockAFrameCondition(condition_i, frames_filled_conditions, unlocked_items, used_items)
                else: #we unlock an item condition
                    random_i = random_i-len(frames_unlockable_conditions)
                    condition_i = items_unlockable_conditions[random_i]
                    items_filled_conditions, used_items = self.unlockAnItemCondition(condition_i, items_filled_conditions, unlocked_items, used_items)

            if previous == used_items: #for faster verification
                break
            #verify if the world is completed
            if all(unlocked_exits) and all(unlocked_items) and boss_reached:
                break

        return unlocked_exits, unlocked_items, boss_reached, early_boss_indicator


    def softlockIsPossible(self, frames_reachable_conditions, items_reachable_conditions, unlocked_items):
        
        available_items = [x for x, y in zip(self.items.values, unlocked_items) if y == 1]

        if 1 in frames_reachable_conditions+items_reachable_conditions: #1:hook+bridge 
            if (available_items.count(8)==1) and (not 14 in available_items) and (2 in frames_reachable_conditions+items_reachable_conditions):
                return True
        if 6 in frames_reachable_conditions+items_reachable_conditions: #6:double hook
            if (available_items.count(8)==1) and (2 in frames_reachable_conditions+items_reachable_conditions):
                return True
        if 8 in frames_reachable_conditions+items_reachable_conditions: #8:hook+key
            if (available_items.count(8)==1) and (not 10 in available_items) and (2 in frames_reachable_conditions+items_reachable_conditions):
                return True
        return False

    def feasibleWorldVerification_debug(self):
        print('----- NEW RUN -----')
        early_boss_indicator = -0.1
        unlocked_exits = [0]*self.nExits
        unlocked_exits[self.starting_exit] = 1 #means that we have access to this exit at the start
        used_items = [0]*self.nItems
        unlocked_items = [0]*self.nItems
        items_filled_conditions = [0]*len(self.items.conditions_types) #means that we already put none of the the bridges and hooks to reach the items
        items_filled_conditions[0] = 1 # element 0 should always be set to 1 in this list
        frames_filled_conditions = [0]*len(self.frames.conditions_types) #means that we already put none of the the bridges and hooks to reach the exits
        frames_filled_conditions[0] = 1 # element 0 should always be set to 1 in this list
        for big_step in range(50): #max number or loops
            for small_step in range(100): #how much exploration before we unlock something
                #exits links

                previous = deepcopy(unlocked_exits)
                unlocked_exits, boss_reached = self.exits.getUnlockedExits(unlocked_exits)
                new = deepcopy(unlocked_exits)
                for exit_i in range(self.nExits):
                    if new[exit_i] and not previous[exit_i]:
                        print('Unlocked exit:',exit_i)

                if boss_reached and early_boss_indicator == -0.1:
                    unlocked_items = self.items.getUnlockedItems(unlocked_exits, items_filled_conditions)
                    early_boss_indicator = (sum(unlocked_items)+sum(unlocked_exits))/(len(unlocked_items)+len(unlocked_exits))
                    early_boss_indicator = self.bossKeyAlreadyUsed(used_items)*early_boss_indicator #Always too early if the boss key was not used
                #internal frame links
                previous = deepcopy(unlocked_exits)
                unlocked_exits = self.frames.getUnlockedExits(unlocked_exits, frames_filled_conditions)
                new = deepcopy(unlocked_exits)
                for exit_i in range(self.nExits):
                    if new[exit_i] and not previous[exit_i]:
                        print('Unlocked exit:',exit_i)
            print('-------------')
            #unlocked items
            previous = deepcopy(unlocked_items)
            unlocked_items = self.items.getUnlockedItems(unlocked_exits, items_filled_conditions)
            new = deepcopy(unlocked_items)
            for item_i in range(self.nItems):
                if new[item_i] and not previous[item_i]:
                    print('Unlocked item:',item_i, ' (',self.items.names[item_i],')')


            #We now have to unlock something in order to move further?
            #what can we unlock right now?
            frames_reachable_conditions, items_reachable_conditions = self.getReachableConditions(unlocked_exits, frames_filled_conditions, items_filled_conditions)
            frames_unlockable_conditions, items_unlockable_conditions = self.getUnlockableConditions(frames_reachable_conditions, items_reachable_conditions, unlocked_items, used_items)
            
            #Check for softlocks
            if self.softlockIsPossible(frames_reachable_conditions, items_reachable_conditions, unlocked_items):
                break
            
            #randomly chose which condition to unlock
            previous = deepcopy(used_items)
            if len(frames_unlockable_conditions)+len(items_unlockable_conditions)>0:
                random_i = random.randint(0, len(frames_unlockable_conditions)+len(items_unlockable_conditions)-1)
                if random_i<len(frames_unlockable_conditions): #we unlock a frame condition
                    condition_i = frames_unlockable_conditions[random_i]
                    frames_filled_conditions, used_items = self.unlockAFrameCondition(condition_i, frames_filled_conditions, unlocked_items, used_items)
                else: #we unlock an item condition
                    random_i = random_i-len(frames_unlockable_conditions)
                    condition_i = items_unlockable_conditions[random_i]
                    items_filled_conditions, used_items = self.unlockAnItemCondition(condition_i, items_filled_conditions, unlocked_items, used_items)
            new = used_items
            for item_i in range(self.nItems):
                if new[item_i] and not previous[item_i]:
                    print('Used item:',item_i, ' (',self.items.names[item_i],')')

            #verify if the world is completed
            if all(unlocked_exits) and all(unlocked_items) and boss_reached:
                break

        return unlocked_exits, unlocked_items, boss_reached, early_boss_indicator

    def bossKeyAlreadyUsed(self, used_items):
        bossKeyItemValues = [0xB,0xB,0xB,0x8,0xB] #boss key in world 3 is a hook ... sort of
        if bossKeyItemValues[self.world_i] in self.items.values:
            bosskey_i = self.items.values.index(bossKeyItemValues[self.world_i])
            return used_items[bosskey_i]
        else:
            return False # no boss key in items

    def unlockAFrameCondition(self, condition_i, frames_filled_conditions, unlocked_items, used_items):
        condition_type = self.frames.conditions_types[condition_i]
        frames_filled_conditions[condition_i] = 1

        if (condition_type == 1): required_items = [0x8,0xE]
        elif (condition_type == 2): required_items = [0x8]
        elif (condition_type == 3): required_items = [0xE]
        elif (condition_type == 4): required_items = [0xA]
        elif (condition_type == 5): required_items = [0xB]
        elif (condition_type == 6): required_items = [0x8,0x8]
        elif (condition_type == 7): required_items = [0xA]
        elif (condition_type == 8): required_items = [0x8,0xA]
        for required_item in required_items:
            for item_i in range(self.nItems):
                if unlocked_items[item_i] and not used_items[item_i] and self.items.values[item_i]==required_item:
                    used_items[item_i] = 1 #we use that item
                    break

        return frames_filled_conditions, used_items
        

    def unlockAnItemCondition(self, condition_i, items_filled_conditions, unlocked_items, used_items):
        condition_type = self.items.conditions_types[condition_i]
        items_filled_conditions[condition_i] = 1

        if (condition_type == 1): required_items = [0x8,0xE]
        elif (condition_type == 2): required_items = [0x8]
        elif (condition_type == 3): required_items = [0xE]
        elif (condition_type == 4): required_items = [0xA]
        elif (condition_type == 5): required_items = [0xB]
        elif (condition_type == 6): required_items = [0x8,0x8]
        elif (condition_type == 7) and (0xA in available_items): frames_unlockable_conditions.append(condition_i)
        elif (condition_type == 8): required_items = [0x8,0xA]

        for required_item in required_items:
            for item_i in range(self.nItems):
                if unlocked_items[item_i] and not used_items[item_i] and self.items.values[item_i]==required_item:
                    used_items[item_i] = 1 #we use that item
                    break

        return items_filled_conditions, used_items
        
    
    def getUnlockableConditions(self, frames_reachable_conditions, items_reachable_conditions, unlocked_items, used_items):
        available_items = []
        for item_i in range(self.nItems):
            if unlocked_items[item_i] and not used_items[item_i]:
                available_items.append(self.items.values[item_i])

        frames_unlockable_conditions = []
        for i in range(len(frames_reachable_conditions)):
            condition_i = frames_reachable_conditions[i]
            condition_type = self.frames.conditions_types[condition_i]
            #type of condition: 0: no condition, 1: hook+bridge, 2: hook, 3:bridge, 4: door grey key external, 5: door boss key, 6:double hook, 7: door grey key with no going back!, 8: hook+key
            #{0x8 : "Hookshot", 0x9 : "Candle", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel", 0xD : "Bell", 0xE : "Bridge"}
            if (condition_type == 1) and (0x8 in available_items) and (0xE in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 2) and (0x8 in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 3) and (0xE in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 4) and (0xA in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 5) and (0xB in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 6) and (available_items.count(0x8)>=2): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 7) and (0xA in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 8) and (0x8 in available_items) and (0xA in available_items): frames_unlockable_conditions.append(condition_i)
        
        items_unlockable_conditions = []
        for i in range(len(items_reachable_conditions)):
            condition_i = items_reachable_conditions[i]
            condition_type = self.items.conditions_types[condition_i]
            #type of condition: 0: no condition, 1: hook+bridge, 2: hook, 3:bridge, 4: door grey key external, 5: door boss key, 6:double hook, 7: door grey key with no going back!, 8: hook+key
            #{0x8 : "Hookshot", 0x9 : "Candle", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel", 0xD : "Bell", 0xE : "Bridge"}
            if (condition_type == 1) and (0x8 in available_items) and (0xE in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 2) and (0x8 in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 3) and (0xE in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 4) and (0xA in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 5) and (0xB in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 6) and (available_items.count(0x8)>=2): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 7) and (0xA in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 8) and (0x8 in available_items) and (0xA in available_items): items_unlockable_conditions.append(condition_i)

        return frames_unlockable_conditions, items_unlockable_conditions


    def getReachableConditions(self, unlocked_exits, frames_filled_conditions, items_filled_conditions): 
        # A place where you can use a bridge or a hook is called a condition. 
        # There are conditions to unlocks items and conditions to unlock exits inside a given frame
        # This function checks which of these conditions are reachable
        frames_reachable_conditions = []
        items_reachable_conditions = []
        for exit_i in range(len(unlocked_exits)):
                if unlocked_exits[exit_i]:
                    for condition_i in self.frames.associated_conditions_i[exit_i]:
                        if condition_i not in frames_reachable_conditions:
                            frames_reachable_conditions.append(condition_i)
                    for item_i in range(self.nItems):
                        associated_exit_i = self.items.associated_exits[item_i]
                        if exit_i == associated_exit_i:
                            condition_i = self.items.associated_conditions[item_i]
                            if condition_i not in items_reachable_conditions:
                                items_reachable_conditions.append(condition_i)

        # remove conditions that are already met
        for condition_i in range(len(frames_filled_conditions)):
            if frames_filled_conditions[condition_i]:
                if condition_i in frames_reachable_conditions:
                    frames_reachable_conditions.remove(condition_i)
        for condition_i in range(len(items_filled_conditions)):
            if items_filled_conditions[condition_i]:
                if condition_i in items_reachable_conditions:
                    items_reachable_conditions.remove(condition_i)

        return frames_reachable_conditions, items_reachable_conditions 