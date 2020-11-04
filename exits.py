import random
from copy import deepcopy

class Exits:
    def __init__(self, data, world_i):
        
        all_nFrames = [16, 16, 26, 30, 26]
        all_boss_frame = [14, 15, 25, 25, 25]
        self.nFrames = all_nFrames[world_i]
        self.boss_frame = all_boss_frame[world_i]

        # getter utilization
        self.offsets,values,self.source_frames = self.getExitsFromData(data,world_i,self.nFrames)
        self.nExits = len(values)
        self.destination_frames = [value[0] for value in values]
        self.source_raw_types = [value[3] for value in values]
        self.destination_Xpos = [value[4] for value in values]
        self.destination_Ypos = [value[5] for value in values]

        for i in range(self.nExits):
                if self.destination_frames[i] == self.boss_frame:
                    self.preboss_frame = i
                    break

        # other methods
        self.source_Xpos, self.source_Ypos = self.getSourcePositions()
        self.source_types, self.destination_types = self.getTypes()
        self.pairs = self.getPairs()
        
        
    def getExitsFromData(self, data, world_i, nFrames):
        """Fonction allant chercher les offsets ET les valeurs. Je ne sais pas encore si on a besoin 
            des deux ou pas. Donc j'ai retourné les deux.

            Big thank you to Psychomaniac, reference : https://pastebin.com/y8yYPcfd

            Voici la logique :
                1- Lecture d'un byte à un endroit précis qui dépend du World. L'info sera un premier offset. C'est la base.
                    offset 1 = 0x01F303 + World  ou $83:F303 + level_index
                2- L'endroit de lecture suivant dépend du level et de la lecture précédente. Ça donne un autre offset.
                    NOTE : ON DOIT LIRE UN "BIG BYTE", DONC ON LIT LE BYTE SUIVANT POUR LE HIGH ENDIAN chose.
                    offset 2 = 0x1F303 + offset 1 + 2 * level
                3- La lecture à ce dernier offset donnera l'infos sur la quantité de exits à loader.
                    0x10000 + offset2
                4- On load les informations des exits qui sont entreposés dans les cinq offsets par exits.
                    Le premier débute au offset juste après la lecture à l'étape 3.

            Args:
                data (bytearray): data du jeu.
                World (int): World que l'on veut loader.


            Return (tuple): exits_offsets, exits_values
                exits_offsets (liste): Liste de liste qui contient les 6 offsets des exits.
                exits_values (liste): Liste de liste qui contient les 6 infos des exits.
                    [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5] ...]
                    0 : Screen this exit leads to
                    1 : Base tile index on collision map
                    2 : Pas spécifié par psychomaniac
                    3 : Type d'exit, It specifies how the exit's collision tiles are laid down, See below.
                        If bit 6 is set (0x20) then it is a vertical line, otherwise it is horizontal or 2x2
                        If bit 6 is not set and bits 1-4 are 0x0F, then the exit is 2x2 (x,y) (x+1,y) (x,y+1) and (x+1,y+1)
                        For horizontal or vertical lines, bits 1-4 specify the length and bit 5 says if it is 1 or 2 tiles thick.
                    4 : X position on the destination screen to place Max and/or Goofy
                    5 : Y position on the destination screen to place Max and/or Goofy

            """
        # J'ai fait ces deux checks au cas où.
        assert isinstance(data, bytearray), "Must be a bytearray"
        assert 0 <= world_i <= 4, "Must be in range 0-4."

        exits_values = []
        exits_offsets = []
        exits_frames = []

        # Step 1 : Trouver la base.
        base = data[0x01F303 + world_i]
        for frame_i in range(nFrames):
        # J'ai mis ces lignes en commentaires, car ces lignes forcent l'itération. 
        # Je pense que l'itération serait beaucoup mieux
        # Si elle était faite en dehors de la fonction.

        # Comme ça, ça nous permet d'aller chercher spécifiquement les exits à UN endroit souhaité.

                # On doit trouver l'endroit du count.

                # On doit aller chercher le GROS byte. et pour cela, on doit avoir un "adjust" qui est dépendant du frame.
            adjust = 0x1F303 + base + 2*frame_i

            #Lecture du Gros Byte. On doit lire le byte présent et le byte suivant et les combiner ensemble.
                # GROS BYTE : 0xHHpp
            temp1 = data[0x1F303 + base + 2*frame_i]  # Cecu est l'endroit où es tle count, du moins les deux premiers bytes on a les deux premiers chiffres! (pp)
            temp2 = data[0x1F303 + base + 2*frame_i + 1]  # Les deux high bytes (HH)

            # Donc le fond on doit faire 2 shift left pour ajouter deux zeros. 
            # Puis additionner.
                # 0xHH => 0xHH00 => 0xHHpp
            # Je ne comprends pas pourquoi 16^2 ne fonctionne psa ici.

            temp3 = temp2 * 16 * 16 + temp1  

            # Trouvons enfin l'endroit du count.
            temp4 = 0x10000 + temp3
            count = data[temp4]  # This will be the count.

            for i in range(count):
                exits_offsets.append(list(temp4 + x + 6 * i + 1 for x in range(6)))  # Voici les offsets.
                # Il devrait être possible d'utiliser Exit() ici.
                exits_values.append([data[temp4 + x + 6 * i + 1] for x in range(6)])  # Voici les valeurs retrouvées dans chaque offsets.
                exits_frames.append(frame_i)
                """
                    0 : Screen this exit leads to
                    1 : Base tile index on collision map
                    2 : Pas spécifié par psychomaniac
                    3 : Type d'exit, It specifies how the exit's collision tiles are laid down, See below.
                        If bit 6 is set (0x20) then it is a vertical line, otherwise it is horizontal or 2x2
                        If bit 6 is not set and bits 1-4 are 0x0F, then the exit is 2x2 (x,y) (x+1,y) (x,y+1) and (x+1,y+1)
                        For horizontal or vertical lines, bits 1-4 specify the length and bit 5 says if it is 1 or 2 tiles thick.
                    4 : X position on the destination screen to place Max and/or Goofy
                    5 : Y position on the destination screen to place Max and/or Goofy
                """
        return exits_offsets, exits_values, exits_frames  # On retourne les listes
    
    def getSourcePositions(self):
        source_Xpos = []
        source_Ypos = []
        for i in range(self.nExits): #source
            is_a_destination = False
            for j in range(self.nExits): #destination
                if (self.destination_frames[i] == self.source_frames[j])&(self.destination_frames[j] == self.source_frames[i]):
                    source_Xpos.append(self.destination_Xpos[j])
                    source_Ypos.append(self.destination_Ypos[j])
                    is_a_destination = True
                    break
            if is_a_destination == False:
                # this source is not a destination: means that the exit leads to the boss (North)
                source_Xpos.append(120)
                source_Ypos.append(28)

        return source_Xpos, source_Ypos

    def getPairs(self):
        pairs = []
        for i in range(self.nExits):
            for j in range(self.nExits):
                if (self.destination_frames[i] == self.source_frames[j])&(self.destination_frames[j] == self.source_frames[i]):
                    if sorted([i,j]) not in pairs: 
                        pairs.append(sorted([i,j]))
        return pairs

    def getTypes(self):
        source_types = []
        destination_types = []
        N_list = [4, 18, 20, 146, 148]
        S_list = [68, 82, 84, 196, 210]
        W_list = [98, 100, 226, 228]
        E_list = [34, 35, 36, 50, 162, 164]
        stairs_list = [15, 143]
        for i in range(self.nExits):
            if self.source_raw_types[i] in N_list:
                destination_types.append('S')
                source_types.append('N')
            elif self.source_raw_types[i] in S_list:
                destination_types.append('N')
                source_types.append('S')
            elif self.source_raw_types[i] in W_list:
                destination_types.append('E')
                source_types.append('W')
            elif self.source_raw_types[i] in E_list:
                destination_types.append('W')
                source_types.append('E')
            elif self.source_raw_types[i] in stairs_list:
                destination_types.append('?')
                source_types.append('?')
            else:
                raise ExitTypeError('Could not assign a type to this exit')

        return source_types, destination_types #destination types will not be valid if there had already been a randomization

    def determineRandomizationOrder(self, fix_boss_exit, keep_direction, pair_exits):
        new_order = list(range(self.nExits))
        if keep_direction & (not pair_exits):#keep direction
            for targeted_type in ['N','S','W','E','?']:
                targeted_i = [i for i, destination_type in enumerate(self.destination_types) if destination_type == targeted_type]
                if fix_boss_exit: 
                    if self.preboss_frame in targeted_i: targeted_i.remove(self.preboss_frame)
                shuffled_i = deepcopy(targeted_i)
                random.shuffle(shuffled_i)
                for j,i in enumerate(targeted_i):
                    new_order[i] = shuffled_i[j]

        elif (not keep_direction) & (pair_exits):#pair exits
            shuffled_pairs = deepcopy(self.pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(self.pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]

        elif keep_direction & pair_exits: #keep direction AND pair exits
            pairs_to_sort = deepcopy(self.pairs)
            NS_pairs = []
            WE_pairs = []
            stairs_pairs = []
            for pair in pairs_to_sort:
                if (self.destination_types[pair[0]] == 'N') or (self.destination_types[pair[0]] == 'S'):
                    NS_pairs.append(pair)
                elif (self.destination_types[pair[0]] == 'W') or (self.destination_types[pair[0]] == 'E'):
                    WE_pairs.append(pair)
                elif (self.destination_types[pair[0]] == '?'):
                    stairs_pairs.append(pair)
            #North and South pairs
            shuffled_pairs = deepcopy(NS_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(NS_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]
            #West and East pairs
            shuffled_pairs = deepcopy(WE_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(WE_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]
            #stairs pairs
            shuffled_pairs = deepcopy(stairs_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(stairs_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]

        else: #totally random
            random.shuffle(new_order)
            if fix_boss_exit:
                new_order.remove(self.preboss_frame)
                new_order.insert(self.preboss_frame,self.preboss_frame)

        return new_order

    def randomize(self, fix_boss_exit, keep_direction, pair_exits): #fix_boss_exit is a bool
            
        #determine new order
        new_order = self.determineRandomizationOrder(fix_boss_exit, keep_direction, pair_exits)

        #assign elements in new order
        self.destination_frames = [self.destination_frames[i] for i in new_order]
        self.destination_Xpos = [self.destination_Xpos[i] for i in new_order]
        self.destination_Ypos = [self.destination_Ypos[i] for i in new_order]
        self.destination_types = [self.destination_types[i] for i in new_order]
