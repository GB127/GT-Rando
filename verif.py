internal_exit_to_exit = [[1],[0],[3],[2],[5],[4],[7,8],[6,8],[6,7],[10], # 0 to 9
                        [9],[12],[11],[14,15,16],[13,15,16],[13,14,16],[13,14,15],[18],[17],[], # 10 to 19
                        [21,22],[20,22],[20,21],[25],[],[23],[27],[26],[],[30], # 20 to 29
                        [29],[],[]] # 30 to 32

internal_exit_to_item = [[2,'Hookshot'],[5,'Bell'],[6,'Hookshot'],[9,'Hookshot'],[11,'Hookshot'],[19,'Bridge'],[24,'Shovel'],[30,'Bell'],[31,'Gold Key']] #linked exit, available item. PS: ONLY PUT THE FREE ITEMS HERE

external_exit_to_exit = [32,2,1,5,7,3,14,4,10,18,8,21,13,12,6,24,19,26,9,16,30,11,25,31,15,22,17,28,27,'BOSS',20,23,0]

locks = [[[17, 18],'Bridge',[17,18],'internal'], # requirement, cost, reward(s), lock type
         [[11, 21],'Grey Key',[11,21],'external'],
         [[29],'Gold Key',['BOSS'],'external'],
         [[28],'Hookshot',['Grey Key'],'item']] # fake link, for testing only

available_exits = [0]
available_items = []

def softlocksVerification(internal_exit_to_exit, internal_exit_to_item, external_exit_to_exit, locks, available_exits, available_items, current_layer):

    last_num_of_available_exits = 0
    while len(available_exits)>last_num_of_available_exits:
        # update available exits
        last_num_of_available_exits = len(available_exits)

        # external links
        for exit in available_exits:
            if exit != 'BOSS': 
                target_exit = external_exit_to_exit[exit]
            else:
                continue
            for lock in locks:
                if lock[3] == 'external' and exit in lock[0]:
                    target_exit = None
            if target_exit != None and target_exit not in available_exits:
                available_exits.append(target_exit)

        # internal links (exits)
        for exit in available_exits:
            if exit != 'BOSS':
                target_exits = internal_exit_to_exit[exit]
            else:
                continue
            for target_exit in list(target_exits):
                for lock in locks:
                    if lock[3] == 'internal' and exit in lock[0] and target_exit in lock[0]:
                        target_exit = None
                if target_exit != None and target_exit not in available_exits:
                    available_exits.append(target_exit)

        # update available exits
        if 'BOSS' not in available_exits:
            available_exits = sorted(available_exits)

    print(available_exits)

    # check if boss was reached
    if 'BOSS' in available_exits:
        print('Yay! I made it to the end in this path :)')
        return True

    # unlock items
    items_found = []
    for item in internal_exit_to_item:
        item_is_locked = False
        for lock in locks:
            if lock[3] == 'item' and item[0] in lock[0]:
                item_is_locked = True
        if item[1] == 'Grey Key': print('OOOOOOOOOOO',item_is_locked, locks)
        if item[0] in available_exits and not item_is_locked:
            items_found.append(item)
    for item_found in items_found:
        internal_exit_to_item.remove(item_found)
        available_items.append(item_found[1])

    print(available_items)

    # determine all the possible decisions
    possible_unlocks = []
    for lock in locks:
        requirement_is_filled = False
        for exit in available_exits:
            if exit in lock[0]: requirement_is_filled = True
        if requirement_is_filled and lock[1] in available_items:
            possible_unlocks.append(lock)

    print(possible_unlocks)

    # explore all possible paths
    for unlock in possible_unlocks:
        temporary_items = available_items.copy()
        temporary_exits = available_exits.copy()
        temporary_locks = locks.copy()
        temporary_items.remove(unlock[1])

        if isinstance(unlock[2][0], str):
            if unlock[2][0] == 'BOSS':
                temporary_exits.append('BOSS')
            else:
                temporary_items.append(unlock[2][0])
        else:
            for exit in unlock[2]:
                if exit not in temporary_exits:
                    temporary_exits.append(exit)
        temporary_locks.remove(unlock)
        print('NEW PATH, layer:',current_layer+1)
        this_path_is_ok = softlocksVerification(internal_exit_to_exit, internal_exit_to_item, external_exit_to_exit, temporary_locks, temporary_exits, temporary_items, current_layer+1)
        print('PATH RESULT:', this_path_is_ok,', for layer:',current_layer+1)

        if not this_path_is_ok:
            return False
    if possible_unlocks == [] and 'BOSS' not in available_exits:
        return False
    else:
        return True
            

print('FINAL RESULT:', softlocksVerification(internal_exit_to_exit, internal_exit_to_item, external_exit_to_exit, locks, available_exits, available_items, 0))