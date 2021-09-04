from gameclass import GT
from world import World
from exits import Exits
from items import Items
from generic import world_indexes

class debug(GT):
    def __init__(self, data):
        super().__init__(data)        
        del self.Worlds
        self.Worlds = [World_debug(self.data, x) for x in range(5)]

    def save(self):
        super().save("debug.smc")

class World_debug(World):
    def __init__(self, data, world_i):
        super().__init__(data, world_i)
        del self.Exits
        del self.Items
        
        self.Exits = Exits_debug(self.data, self.world_i, world_indexes(self.world_i))
        self.Items = Items_debug(self.data, self.world_i, world_indexes(self.world_i))
"""
    def showMap(self, world_i, show_exits=True, show_items=True):
        this_world = self.all_worlds[world_i]  # This is now self.world_i
        
        #map
        filenames = ['map0.png','map1.png','map2.png','map3.png','map4.png']
        img = cv2.imread('maps/'+filenames[this_world.world_i])
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        fig,ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(RGB_img)
        # frames and items
        frame_size = (256, 221)
        all_worlds_frame_positions = [[(128, 1442),(384, 1442),(384, 1221),(384, 1000),(640, 1000),(128, 779),(384, 779),(640, 779),(128, 558),(384, 558),(640, 558),(640, 337),(128, 337),(384, 337),(128, 116),(128, 1221)],
                                        [(384, 2110),(384, 1889),(384, 1668),(384, 1447),(128, 1447),(128, 1226),(128, 1005),(384, 1226),(384, 1005),(384, 784),(640, 784),(896, 784),(640, 563),(896, 563),(896, 342),(896, 121)],
                                        [(1195, 1292),(1195, 1071),(939, 1071),(1451, 1071),(939, 850),(1195, 850),(1451, 850),(939, 629),(1195, 629),(1451, 629),(384, 1255),(640, 1255),(128, 1034),(384, 1034),(640, 1034),(128, 1255),(281, 746),(537, 746),(281, 525),(537, 525),(837, 333),(1093, 333),(837, 112),(1093, 112),(1464, 333),(1464, 112)],
                                        [(384, 3580),(128, 3580),(384, 3359),(384, 3138),(640, 3138),(896, 3138),(896, 2917),(640, 2917),(896, 2696),(896, 2254),(1152, 2254),(1408, 2254),(896, 2033),(1408, 2033),(640, 2033),(1408, 1591),(640, 1591),(1152, 1591),(896, 1370),(1152, 1370),(1152, 1149),(1152, 928),(1152, 707),(1408, 707),(1152, 486),(1152, 265),(896, 2475),(640, 1370),(640, 1812),(1408, 1812)],
                                        [(128, 1350),(128, 1129),(384, 1129),(1003, 1334),(747, 1334),(747, 1113),(1003, 1113),(1259, 1113),(1259, 1334),(2065, 1334),(1809, 1334),(1809, 1113),(1553, 1113),(1553, 1334),(2065, 1113),(1809, 892),(2065, 892),(1553, 892),(747, 892),(1003, 892),(1259, 892),(2065, 141),(2065, 362),(2065, 583),(1809, 362),(1809, 141)]]
        frame_positions = all_worlds_frame_positions[this_world.world_i]
        for frame_i in range(this_world.nFrames):
            base_pos = frame_positions[frame_i]
            ax.add_patch(Circle((base_pos[0],base_pos[1]),24, color='w'))
            ax.text(base_pos[0],base_pos[1],str(frame_i),fontsize=11,
                    horizontalalignment='center', verticalalignment='center')
            if show_items:#items
                if frame_i in this_world.items.frames: 
                    item_i = [i for i, x in enumerate(this_world.items.frames) if x == frame_i] #items in this frame
                    item_name = [this_world.items.names[i] for i in item_i]
                    ax.text(base_pos[0],base_pos[1]+40,str(item_i),fontsize=7,
                        horizontalalignment='center', verticalalignment='center', color='w')
                    ax.text(base_pos[0],base_pos[1]+65,str(item_name),fontsize=5,
                        horizontalalignment='center', verticalalignment='center', color='w')
        
        #exits
        if show_exits:
            for i,source in enumerate(this_world.exits.source_frames):
                this_color = list(1-np.random.choice(range(256), size=3)/300)
                #source exit
                base_pos = frame_positions[source]
                source_pos = (base_pos[0]-frame_size[0]/2+this_world.exits.source_Xpos[i], base_pos[1]-frame_size[1]/2+this_world.exits.source_Ypos[i])
                ax.add_patch(Circle(source_pos,5, color=this_color))
                ax.text(source_pos[0],source_pos[1],str(i),fontsize=10,
                        horizontalalignment='center', verticalalignment='center', color='red')
                #target exit
                base_pos = frame_positions[this_world.exits.destination_frames[i]]
                target_pos = (base_pos[0]-frame_size[0]/2+this_world.exits.destination_Xpos[i], base_pos[1]-frame_size[1]/2+this_world.exits.destination_Ypos[i])
                ax.arrow(source_pos[0],source_pos[1],target_pos[0]-source_pos[0], target_pos[1]-source_pos[1], 
                        head_width=15,length_includes_head=True, color=this_color)
        plt.show()
        return


"""

class Exits_debug(Exits):
    pass

class Items_debug(Items):
    def set_item(self, B7, item_id, new_item):
        def compatible_ids():
            liste = []
            for item_id in range(32):
                check_item = self.data.screens[self.screens[B7]].class_2_sprites[item_id].type
                if check_item in items_names.keys():
                    liste.append(item_id)
            return liste

        items_names = {0x8 : "Hookshot", 0x9 : "Candle  ", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel  ", 0xD : "Bell    ", 0xE : "Bridge  ", 0x40 : "Cherry  ", 0x42: "Banana  ", 0x44 : "Red Gem ", 0x46 : "Blue Gem"}
        assert new_item in items_names.keys(), f"New item need to be a value in {list(items_names)}"

        self.data.screens[self.screens[B7]].class_2_sprites[compatible_ids()[item_id]].type = new_item
        self.generate_data()


if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())
        world_test = test.Worlds[4].Items
        world_test.set_item(9,0,10)
        print(world_test)
