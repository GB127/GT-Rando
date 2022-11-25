from generic import world_indexes, LogicError
from items import Items
import matplotlib.pyplot as plt
from exits import Exits
from doors import Doors
from copy import deepcopy
import networkx as net # version 2.5

class World():
    def __init__(self, data, world_i):
        self.world_i = world_i
        self.data = data
        self.screens = world_indexes(self.world_i)

        self.Exits = Exits(self.data,self.world_i,self.screens)
        self.Items = Items(self.data, self.world_i, self.screens)
        self.Doors = Doors(self.data, self.world_i, self.screens)

    def __call__(self):
        self.Exits(randomize=True, keep_direction=True, pair_exits=True)
        self.Items(randomize_items=True)


    def __bool__(self):
        # World 0 : Vanilla Works
        # World 1 : Vanilla Works
        # World 2 :
        # World 3 : Vanilla will work once we take care of the internal puzzles that makes some paths unidirect.
        # World 4 :
        def get_items(graphik, spawn) -> list:
            """Get all accessible items from specified spawn."""
            items = []
            for access in net.shortest_path(graphik, spawn).keys():
                if isinstance(access, tuple):
                    items.append(access)
            return items

        def get_locks(graphik,locks, spawn) -> list:
            """Get all accessible locks from a specified spawn."""
            accessible_locks = set()
            for screen_lock in locks.values():
                for lock, exits in screen_lock.items():
                    for duo in exits:
                        for exit in duo:
                            if exit in net.shortest_path(graphik, spawn):
                                accessible_locks.add((lock, exit))
            return list(accessible_locks)

        def use_lock(graphik, locks, lock, used):  # Returns the new graphic after using the item specified on the lock specified.!
            copy_g = deepcopy(graphik)

            used_item = lock[0]
            which_spawn = lock[1]
            which_screen = self.B7_screen(int(which_spawn[:-3]))
            for lock, links in locks[which_screen].items():
                if lock != used_item:
                    continue
                for edge in links:
                    copy_g.add_edge(*edge)
                copy_g.remove_node(used)
            del locks[self.B7_screen(int(which_spawn[:-3]))][used_item]

            if self.world_i == 0:
                if which_screen == 5:
                    del locks[8][used_item]
                elif which_screen == 8:
                    del locks[5][used_item]
            if self.world_i == 1:
                if which_screen == 26:
                    del locks[28][used_item]
                elif which_screen == 28:
                    del locks[26][used_item]


            return copy_g, locks

        def play(graph, spawn, locks):
            # Check if locks are accessible:
            accessible_locks = get_locks(graph,locks, spawn)
            accessible_items = get_items(graph, spawn)
            if not accessible_locks:  # Tout est supposément débarré.
                accessible_spawn = net.shortest_path(graph, spawn).keys()
                for sortie in self.Exits:
                    if str(sortie) not in accessible_spawn:
                        net.draw(graph, with_labels=True)
                        plt.savefig("recursive_bug.png", format="PNG")
                        plt.clf()
                        raise LogicError(f"{sortie} not accessible")
                #raise BaseException("Tout est accessible!")
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

        print("Starting the recursion...")
        play(g, "0 (N)", initial_locks)
        return True


    def B7_screen(self, B7):
        return self.screens[B7]


    def nodes(self):
        # Add something for internal puzzles. Like in the cave.


        g = net.compose(self.Exits.nodes(), self.Items.nodes(self.Exits))
        net.draw(g, with_labels=True)
        plt.savefig("recursive_world1bug.png", format="PNG")
        plt.clf()
        for x in self.Doors.nodes(self.Exits, self.Items).edges():
            g.remove_edge(x[0], x[1])
        return g


    def __getitem__(self, screen):
        return {"exits":self.Exits[screen], "items":self.Items[screen]}
