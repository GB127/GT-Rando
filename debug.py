from gameclass import GT
from infos import *  # This is for the tools in infos.
from datetime import datetime
from world import *
import random
from command import *

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import cv2
import numpy as np

class debug(GT):
    def __str__(self):
        string = ""
        for world in self.all_worlds:
            string += str(world)
        return string


    def print_world(self, world_i, arg=None):
        if arg == "items": 
            print(f"World {world_i} items")
            print(self.all_worlds[world_i].items)
        else: print(self.all_worlds[world_i])


    def __init__(self,data):
        self.list_freespace()
        super().__init__(data, seed="Debug")


    def do_all_modify(self):
        # Code that will do all stuffs that uses freespace except add credits since it's already in the init.
        self.modify_data_ice_dark_alert()
        self.modify_data_starting_frame()
        self.checksum()
        self.credits_frames_randomizer()

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
        



    def quick_bosses(self):
        #self[0xB4AB] = 0x1  # For now, only kill one to clear the boss for world 0.

        self[0xC563] = 0x1

    def early_bosses(self):
        """Changes exits so that bosses are reached within the very first exit of a world!
        """
        self[0x1F3ED] = 14
        self[0x1F4C3] = 15
        self[0x1F58D] = 25
        self[0x1f6f7] = 25
        self[0x1f6f7 + 4] = 180
        self[0x1F877] = 25


    def boss_randomizer(self):
        def boss0_throws(self):

            # Fast throw: les trois premiers ou les trois derniers. high throw c'est l'autre
            for no, offset in enumerate([0x018FA7, 0x018FAB, 0x018FAF, 0x018F9B, 0x018F9F, 0x018FA3]):
                direction = no%3
                check = False
                while check is False:
                    X = random.randint([0x1, 0x0, -0x5][direction],[0x5, 0x0, -0x1][direction])
                    Y = random.randint(0x1, 0x8)
                    if abs(X/Y) > 5/8: continue 
                    self[offset] = 0 if any([X == 0x5, X == -0x5]) else random.randint(0,0xFF)
                    # High byte
                    self[offset+1] = X if X >= 0 else 256 + X
                    self[offset + 2] = 0 if Y == 0x8 else random.randint(0x0, 0xFF)
                    self[offset + 3] = Y
                    check = True


            # Gravity:
            # Plus on descend en valeur, plus la gravité est forte

            # Highthrow
            # Initial throw
                # Valeurs à réviser
                # Minimum acceptable pour la vitesse minimale: F5
                # Maximum acceptable pour la vitesse minimale: F9
                # Minimum acceptable pour la vitesse maximale : 0
                # Maximum acceptable pour la vitesse maximale : 0xC0
            speedvalues = sorted([game[0x018FAA], game[0x018FAE], game[0x018FB2]])

            # Highest value possible plot
            a1 = (0xC0 - 0xF9)/(8 - 1)
            b1 = 0xC0 - a1 * 8
            # lowest value possible plot
            a2 = (0x0 - 0xF5)/(8 - 1)
            b2 = 0x00 - a2 * 8

            low = int(a2 * speedvalues[0] + b2)
            high = int(a1 * speedvalues[-1] + b1)
            lowest = int(a2 * speedvalues[-1] + b2)
            print(lowest, low, high)
            # Initial
            try:
                game[0x00430D] = random.randint(low, high)
            except ValueError: 
                # L'ordre des extrêmes donne une contradiction. 
                # Optons pour l'extrème qui donne plus de possibilités...
                game[0x430D] = random.randint(lowest, low)
            #game[0x00430E] = 0xFF
                # Ne pas changer, car ça sera trop fort sinon.


            # After the peak
            game[0x004312] = 0x0
                # 0 = Almost instantly drop down to the floor.
                # I will change that in the following days.
            #game[0x004313] = 0xFF
                # Ne pas change,r car ça sera trop fort sinon.






            for offset in [0x018F9B, 0x018F9F, 0x018FA3]:  # Fast throw
                pass

            #ZZZZZ


            # Fast throw
            # Initial
            #game[0x0042F5] = test
            #game[0x0042F6] = test2
            # After
            #game[0x0042FA] = test3  # Fast throw
            #game[0x0042FB] = test4  # Fast throw



        def boss0_behaviour_items(self):
            # NPC decision maker
            """ NPC decision maker
                dw $B266 ;02 ;Pop Out and Back In Routine without Items
                dw $B29A ;04 ;Pop Out and Back In Routine fake item
                dw $B2ED ;06 ;Pop Out and Back In Routine throwing random item

                Vanilla values:
                    3x2  (9.375%)  without items
                    6x4  (18.75%)  fake item
                    23x6 (71.875%)  throw
                """
            new_values = [0x6] * random.randint(0,32)
            while len(new_values) != 32:
                new_values.append(random.choice([0x2, 0x4]))  # I don't mind this one being 50/50 since it won't affect the gameplay
            random.shuffle(new_values)
            self.rewrite(0x1A1C8, new_values)

            
            # Thrown item table.
            """ Thrown item table.
                00 barel
                02 pot 
                04 egg 
                06 sign
                08 plant
                0A bomb
                0C log
                0E fence 
                10 ice 
                12 shell 
                14 plates
                16 rock
                18 nut
                1A spike
                FF = nothing
                
                10x0  (31.25%)  Barrel
                6xA  (18.75%)  Bomb
                8x1A  (25.0%)  Spike
                8xFF  (25.0%)  No item thrown
                """
            throwable_items = [0,0x2,0x4,0x6,0x8,0xC, 0xE, 0x10, 0x12, 0x14, 0x16, 0x18]
            bomb =  0xA
            spike = 0x1A
            nothing = 0xFF
            thrown_items = []
            for _ in range(random.randint(0,32)):  # TODO : Need to find the highest acceptable value.
                thrown_items.append(random.choice([nothing, spike])) # FIXME : I want something more random so it's not "always" 50/50

            # TODO: Do something for bombs

            random_item = random.choice(throwable_items + ["all"])
            while len(thrown_items) != 32:
                if random_item == "all":
                    thrown_items.append(random.choice(throwable_items))
                else:
                    thrown_items.append(random_item)
            random.shuffle(thrown_items)
            #self.rewrite(0x1A228, thrown_items)
            print(new_values)
            print(thrown_items)
        boss0_throws(self)
        #boss0_behaviour_items(self)

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

    def setExit(self, world_i, source_exit, destination_exit, match=False):
        """Set a specific exit to a specific exit."""
        this_world = self.all_worlds[world_i]
        this_world.exits.setExit(source_exit, destination_exit)
        self[this_world.exits.offsets[source_exit][0]] = this_world.exits.destination_frames[source_exit]
        self[this_world.exits.offsets[source_exit][4]] = this_world.exits.destination_Xpos[source_exit]
        self[this_world.exits.offsets[source_exit][5]] = this_world.exits.destination_Ypos[source_exit]
        #hook bug fix
        if self[this_world.exits.offsets[source_exit][3]]>=2**7:self[this_world.exits.offsets[source_exit][3]] = self[this_world.exits.offsets[source_exit][3]]-2**7
        self[this_world.exits.offsets[source_exit][3]] = self[this_world.exits.offsets[source_exit][3]]+this_world.exits.destination_hookshotHeightAtArrival[source_exit]*2**7

        if match:
            self.setExit(world_i, destination_exit, source_exit)

    def disable_heart_loss(self):
        self[0x5D1B] = 0xEA
        self[0x5D1C] = 0xEA

    def speed_goofy(self, value):
        self[0x18E1B] -= value
        self[0x18E1D] += value

        self[0x18E2B] += value
        self[0x18E2D] -= value

        self[0x18E17] -= value
        self[0x18E27] += value


        self[0x18E23] += value
        self[0x18E33] -= value


    def __setitem__(self,offset, value):
        if offset in self.freespace:
            self.used.append(offset)
            self.freespace.pop(self.freespace.index(offset))
        super().__setitem__(offset,value)

    def set_item(self, world_i,item_i,  value):
        self.all_worlds[world_i].items.set_item(item_i, value)
        self.all_worlds[world_i].writeWorldInData()

    def do_not_place_keydoors(self):
        self[0x14377] = 0xEA
        self[0x14378] = 0xEA

    def modify_data_stars(self):
        super().modify_data_stars()
        for offset in range(0x14621,0x14D32):
            self[offset] = 0
            self.freespace += [offset]






info = infos()
class randomized(debug):
    def __init__(self, data):
        self.data = bytearray(data)
        self.all_worlds = [World(self.data, 0),World(self.data, 1),World(self.data, 2),World(self.data, 3),World(self.data, 4)]


    def __setitem__(self,offset, value):
        self.data[offset] = value



    


def getoptions_debug():
    # Fonction qui aidera pour faire rouler les randomizers rapidement.

    options = getoptions()

    # Voici ce que l'On doit modifier à la main pour obtenir ce que l'On veut!

    options.Rfirst = False
    options.Rexits = True  #e
    options.Rexits_matchdir = False  #u
    options.Rexits_pair = False  #U
    options.Ritems_pos = True  #i
    options.Ritems = False  #I


    return options





    """
    JSR AntiPiracy      ;808024 ;Prevent SRAM to be used, if SRAM size != 0 loop forever
    ;80F2A9 / 0072A9
    AntiPiracy:
    {
    LDA #$70            ;80F2A9     
    PHA                 ;80F2AB     
    PLB                 ;80F2AC     ;Pull bank (#$70)
    REP #$10            ;80F2AD     ;XY is now 16bit
    LDX #$7F00          ;80F2AF     ;707F00
    .loopZero
    LDA #$00            ;80F2B2
    .loop    
    STA $0000,X         ;80F2B4     ;$707F00
    CMP $0000,X         ;80F2B7     
    BNE .return         ;80F2BA      
    CLC                 ;80F2BC     
    ADC #$11            ;80F2BD     ;ADD #$11
    BNE .loop           ;80F2BF     
    REP #$21            ;80F2C1     A in 16bit, set Carry
    TXA                 ;80F2C3     
    ADC #$FF00          ;80F2C4     ADD #$FF00
    TAX                 ;80F2C7     
    SEP #$20            ;80F2C8     A in 8bit
    BPL .loopZero       ;80F2CA     
    LDA #$80            ;80F2CC     
    STA $2100           ;80F2CE     Set Force Blank
    BRA $80F2D1         ;80F2D1   
    .return             
    SEP #$30            ;80F2D3     
    RTS                 ;80F2D5     
    }"""






if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as original:
        startTime = datetime.now()
        print("generating...")

        game = debug(original.read())
        # game = randomized(original.read())
        game.activateWorldSelection()


        game.setExit(0,0,7)
        game.do_all_modify()

               ###################### |
        #0x100 #0                   # | + 0x80
        #0x180 # 4                  # v
        #0x200 #  ...    60    70   #
        #0x280 #                    #   # Moitié : Environ 0x300
        #0x300 #         E0    F0   #
        # ...  #                    #
               #                    #
               ######################
        #        -----> + 0x4
                    # Moitié : 60
                    # Dernier cinquième : 70

        # Up/down : 
            # half block : - 0x040
            # Full block : 0x080
        # Left/right :
            # full block : 0x004


        # Difficulty 1
        # Level 0-15 : Something need to be done for the pots
        # 0-2 : Same as US
        # 0-3: [0x28C,0x3AC, 0x430, 0x434, 0x4B4]

        # 0-6:[0x220, 0x40C,  0x430]

        # 0-11:[0x398, 0x334, 0x414,  0x428])
        # 0-5 : 0x498
        # 0-13 : same as usa
        # 0-14:  same as usa
        # 1-0: [0x318, 0x324]
        #1-2: [0x40C, 0x4A8, 0x424, 0x420]
        # 1-7 : []
        # 1-6 : Ya une différence et n'a pas de bloc étoilé
        # 1-9 : [0x21C, 0x22C] (Ya des pierres bombales...)
        # 1-13 : []
        # 2-19 : Some pierre bombales
        # 3-4 : L apierre étoilée est au bon endroit. Mais pas les pierres bombales.
        # 3-9 : Pierre bombées
        



        #game.showMap(3)


        test = [0x28C, 0x2B0, 0x40C,  0x430]
        game.remove_stars(3,1)
        game.add_stars(3,1, [0x328, 0x418, 0x41C, 0x420])

        with open("debug.smc", "wb") as newgame:
            # print("Time taken to edit files : ", datetime.now() - startTime)
            print(f"Testing case have been created! {datetime.now()}")
            newgame.write(game.data)

