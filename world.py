from generic import LogicError, room_to_index
from items import Items
import matplotlib.pyplot as plt
from exits import Exits
from locks import Locks
from copy import deepcopy
import networkx as net # version 2.5
from itertools import permutations

class World():
    def __init__(self, data, world_i, screens_ids):
        self.world_i = world_i
        self.data = data
        self.screens = screens_ids

        self.Exits = Exits(self.data,self.world_i,self.screens)
        self.Items = Items(self.data, self.world_i, self.screens)
        self.Doors = Locks(self.data, self.world_i, self.screens, self.Exits, self.Items)

    def __getitem__(self, screen:int):
        """self[screen_id] = {"exits": [All Exits], "items": [All items]}"""
        return {"exits":self.Exits[screen], "items":self.Items[screen]}

    def __call__(self):
        self.Exits(randomize=True, keep_direction=True, pair_exits=True)
        self.Items(randomize_items=True, randomize_fruits=True)
        self.Doors = Locks(self.data, self.world_i, self.screens, self.Exits, self.Items)
        print("finished randomizing!")


    def __bool__(self):
        def get_items(graphik, spawn) -> list:
            """Get all accessible items from specified spawn."""
            items = []
            for access in net.shortest_path(graphik, spawn).keys():
                if isinstance(access, tuple):
                    items.append(access)
            return items

        def get_locks(graphik,current_locks, spawn) -> list:
            """Get all accessible locks from a specified spawn."""
            accessible_locks = set()
            for screen_lock in current_locks.values():
                for lock, exits in screen_lock:
                    for duo in exits:
                        for exit in duo:
                            if isinstance(exit, tuple): continue  # Hack to avoid stupid items.
                            if exit in net.shortest_path(graphik, spawn):
                                accessible_locks.add((lock, exit))
            return list(accessible_locks)

        def use_lock(graphik, current_locks, to_unlock, used):  # Returns the new graphic after using the item specified on the lock specified.!
            copy_g = deepcopy(graphik)
            used_item = to_unlock[0]
            which_spawn = to_unlock[1]
            which_screen = self.B7_screen(int(which_spawn[:-3]))

            for which, screen_lock in enumerate(current_locks[which_screen]):
                if screen_lock[0] != used_item:
                    continue
                if not any(to_unlock[1] in x for x in screen_lock[1]):
                    continue  # Wrong lock. Next please.

                for edge in screen_lock[1]:
                    copy_g.add_edge(*edge)
                copy_g.remove_node(used)
                break
            
            del current_locks[self.B7_screen(int(which_spawn[:-3]))][which]
            if self.world_i == 0:
                if which_screen == 5:
                    del current_locks[8]
                elif which_screen == 8:
                    del current_locks[5]
            if self.world_i == 1:
                if which_screen == 26:
                    del current_locks[28]
                    copy_g.add_edge("12 (S)", "10 (N)")
                elif which_screen == 28:
                    del current_locks[26]

            return copy_g, current_locks

        def play(graph, spawn, locks):
            # Check if locks are accessible:
            accessible_locks = get_locks(graph,locks, spawn)  # Ok.
            accessible_items = get_items(graph, spawn)
            if not accessible_locks:  # Tout est supposément débarré.
                accessible_spawn = net.shortest_path(graph, spawn).keys()
                for sortie in self.Exits:
                    if str(sortie) not in accessible_spawn:
                        net.draw(graph, with_labels=True)
                        plt.savefig("recursive_spawn_bug.png", format="PNG")
                        plt.clf()
                        raise LogicError(f"{sortie} not accessible")
                # Tout est accessible!"
            else: # Il reste encore des trucs à débarrer.
                if not accessible_items:
                    raise LogicError(f"Il n'y a plus d'objets disponibles.")
                for_verif = [x[1] for x in accessible_items]
                if not any([x[0] in for_verif for x in accessible_locks]):
                    net.draw(graph, with_labels=True)
                    plt.savefig("recursive_bug_noitems.png", format="PNG")
                    plt.clf()
                    raise LogicError("Les objets accessibles ne peuvent débloquer les locks actuels.")
                for lock in accessible_locks:
                    for objet in accessible_items:
                        if lock[0] != objet[1]:  # Cet objet ne débarre pas.
                            continue
                        new_locks = deepcopy(locks)
                        new_graph, after_use_lock = use_lock(graph,new_locks, lock, objet)
                        play(new_graph, lock[1], after_use_lock)
            return True

        g = self.nodes()
        initial_locks = deepcopy(self.Doors.world_locks)

        play(g, "0 (N)", initial_locks)
        return True

    def nodes(self):
        def clear_internal_puzzles():
            """At this moment, the exits layout passed the check and all exits should be reachable from the first spawn.
                This function relinks all the exits of the said screens.
            """
            data = [74,  # One of the puzzles in Cave
                        75,  # One of the puzzles in Cave
                        93,  # Puzzle in pirate
                        110,  # W4 : Wheel puzzle room
                    ]
            for screen in self.screens:
                if screen not in data: continue
                for sortie_1, sortie_2 in permutations([f'{room_to_index(id=screen)[1]} ({x.direction})' for x in self.Exits[screen]], 2):
                    net.add_path(g, [sortie_1, sortie_2])

        g = net.compose(self.Exits.nodes(), self.Items.nodes(self.Exits))
        clear_internal_puzzles()
        for x in self.Doors.nodes().edges():
            g.remove_edge(x[0], x[1])
        return g

    def B7_screen(self, B7:int):
        """Convert B7 to screen_id."""
        return self.screens[B7]

