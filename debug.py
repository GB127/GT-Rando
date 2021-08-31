from gameclass import GT
from patch import *


class debug(GT):
    def list_freespace(self):
        self.freespace = [offset for offset in range(0x7374, 0x7FB0)]
        self.freespace += [offset for offset in range(0xFF33, 0x10000)]
        self.freespace += [offset for offset in range(0x1401, 0x15E00)]
        self.freespace += [offset for offset in range(0x1F9C1, 0x1FA42)]
        self.freespace += [offset for offset in range(0x1FADC, 0x20000)]
        self.freespace += [offset for offset in range(0x2A796, 0x2C000)]
        self.freespace += [offset for offset in range(0x47DFE, 0x48000)]
        self.freespace += [offset for offset in range(0x45055, 0x4F100)]
        self.freespace += [offset for offset in range(0x4FD48, 0x50000)]
        self.freespace += [offset for offset in range(0x53F70, 0x54000)]
        self.freespace += [offset for offset in range(0x55FC0, 0x56000)]
        self.freespace += [offset for offset in range(0x57E00, 0x58000)]
        self.freespace += [offset for offset in range(0x5E240, 0x5F000)]
        self.freespace += [offset for offset in range(0x5FBDC, 0x5FE00)]
        self.freespace += [offset for offset in range(0xFB5BE, 0xFD400)]
        self.freespace += [offset for offset in range(0x7FB20, 0x7FE00)]
        self.freespace += [offset for offset in range(0x7FE50, 0x7FEA0)]
        self.freespace += [offset for offset in range(0x7FED0, 0x7FF00)]
        self.freespace += [offset for offset in range(0x7FFB0, 0x7FFFF)]


        self.freespace += [offset for offset in range(0x72A9, 0x72D6)]
        self.used = []


    def save_file(self):
        result = s_result()
        rv = self.lib.conclude(pointer(result))
        with open("debug.smc", "wb") as debug_file:
            debug_file.write(self.data[0:result.num_banks*32768])

"""  BOSS RANDOMIZER WIP
            def boss_randomizer(self):
            def boss0_behaviour_items(self):
                # NPC decision maker
                NPC decision maker
                    dw $B266 ;02 ;Pop Out and Back In Routine without Items
                    dw $B29A ;04 ;Pop Out and Back In Routine fake item
                    dw $B2ED ;06 ;Pop Out and Back In Routine throwing random item

                    Vanilla values:
                        3x2  (9.375%)  without items
                        6x4  (18.75%)  fake item
                        23x6 (71.875%)  throw
                    
                new_values = [0x6] * random.randint(0,32)
                while len(new_values) != 32:
                    new_values.append(random.choice([0x2, 0x4]))  # I don't mind this one being 50/50 since it won't affect the gameplay
                random.shuffle(new_values)
                self.rewrite(0x1A1C8, new_values)

    def showMap(self, world_i, show_exits=True, show_items=True):
        this_world = self.all_worlds[world_i]
        
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
        return ''
    """

if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())  # Open the debug class, which, as the time of writting, an exact copy of the class GT on gameclass.py

        test.save_file()
        print(test)