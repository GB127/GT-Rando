from copy import deepcopy

class Doors():
    def __init__(self, data, world_i, exits):
        all_nFrames = [16, 16, 26, 30, 26]
        self.nFrames = all_nFrames[world_i]

        self.positions_offsets = []
        self.positions = []
        self.shape_types = []
        self.lock_bit_i = []
        self.frames = []
        self.boss_door = []
        for frame_i in range(self.nFrames):
            results = self.getKeyDoorsFromData(data, world_i, frame_i)
            if results:
                for elem in results:
                    self.positions_offsets.append(elem[0])

                    self.positions.append(data[elem[0] +1]*16*16 + data[elem[0]])

                    self.shape_types.append(elem[1])
                    self.lock_bit_i.append(elem[2])
                    self.boss_door.append(elem[3])
                    self.frames.append(frame_i)
        self.nDoors = len(self.frames)

        self.types = self.getDoorTypes()
        self.locked_exits = self.getLockedExits(exits)

    def getDoorTypes(self):
        types = []

        N_list = [14]
        S_list = [846]
        W_list = [256, 448]
        E_list = []
        center_list = [526, 654]
        
        for door_i in range(self.nDoors):
            if self.positions[door_i] in N_list:
                types.append('N')
            elif self.positions[door_i] in S_list:
                types.append('S')
            elif self.positions[door_i] in W_list:
                types.append('W')
            elif self.positions[door_i] in E_list:
                types.append('E')
            elif self.positions[door_i] in center_list:
                types.append('?')
            else:
                raise DoorTypeError('Could not assign a type to this door')
        
        return types

    def getLockedExits(self, exits):
        locked_exits = []
        for door_i in range(self.nDoors):
            for exit_i in range(exits.nExits):
                if (self.frames[door_i] == exits.source_frames[exit_i]) and (self.types[door_i] == exits.source_types[exit_i]):
                    locked_exits.append(exit_i)
                    break

        return locked_exits



    def getKeyDoorsFromData(self, data, world_i, frame_i):  #82C329
        """Get all doors of said world-frame.

            Data structure:
                (0, 1) : Où sur l'écran
                2 : Forme de la porte (Pour pouvoir bien l'éffacer)
                3 : format de la porte
                    Bit 0-2 : offset for getting the correct bit
                    Bit 3-6 : 0x1144 + X depending on the bit sets.
                        Sera tjs 0x1144 ou 0x1145 dans vanilla.
                    Bit 7 : Détermine si la porte est une porte de boss
                        ou une porte normale.

            Returns:
                (0, 1) : Où sur l'écran
                2 : Forme de la porte (Pour pouvoir bien l'éffacer)
                3 : Indice checké par la porte
                4 : 1 if boss door
            """
        result = []
        offset_Y_1 = data[0x14461 + data[0x14461 + world_i] + frame_i]
        if offset_Y_1 != 0:
            current_offset = (data[0x144D7 + offset_Y_1] & 0x00FF) + 0xC4D8
            count = data[0x8000 + current_offset]
            if count != 0:
                current_offset += 1
                for _ in range(count):
                    base_door = 0x8000 + current_offset
                    map_tile_offset = base_door  # [0] et [1], c'est une grosse lecture!
                        # C'est avec cette info ci-dessus que l'on va pouvoir déterminer si C'est une porte
                        # N,S,E ou W.
                    shape = data[base_door + 2]
                    door_data = data[base_door + 3]

                    # Manipulations à faire pour récupérer la bonne information pour la logique.
                    bit_offset = door_data & 0x07
                    which_door = (int((door_data & 0x7F) / 2 / 2 / 2) * 8) + bit_offset

                    boss = (door_data & 0x80) // 0x80
                    result.append([map_tile_offset, shape, which_door, boss])

                    current_offset += 4
        return result


def door_adder(data, world_i, frame_i, tile_high, tile_low, forme, which_door):  #82C329
    """Ajoute une porte.

        IMPORTANT : Toujours retirer une porte présente avant d'utiliser cette fonction.
        Le code est entièrement fonctionnel. Mais l'emplacement actuel des données de portes
        ne permet pas d'ajouter des portes et je devrai les déplacer.

        Aussi, l'ajout d'une porte est purement mécanique : le visuel n'est pas changé et donc
        pour tester cela, il faut vraiment localisre où la mécanique est ajoutée et utiliser une clé.

        Args:
            data ([type]): data of the game.
            world_i (int): World you want to add a door.
            frame_i ([type]): frame you want to add a door.
            tile_high ([type]): [description]
            tile_low ([type]): [description]
            forme (0, 4 ou 2): Forme de la porte.
                Pourrait disparaître si on comprend le tile_high/low.
                0 = N
                4 = S
                2 = EW
            which_door (0 - 32): Which bit to check if locked or not.
                In vanilla, it will never fo over 15 (16 bits available, but not all used).
        """

    offset_Y_1 = data[0x14461 + data[0x14461 + world_i] + frame_i]
    if offset_Y_1 != 0:
        current_offset = (data[0x144D7 + offset_Y_1] & 0x00FF) + 0xC4D8
        vanilla_count = deepcopy(data[0x8000 + current_offset])
        data[0x8000 + current_offset] += 1
        current_offset += 1
        if vanilla_count != 0:
            for _ in range(vanilla_count): current_offset += 4
        base_door = 0x8000 + current_offset

        data[base_door] = tile_low
        data[base_door + 1] = tile_high
        data[base_door + 2] = forme

        # manips pour convertir which_door en données comprenable pour le jeu.
        bits_3_6 = (which_door // 8)  * 2 * 2 * 2
        bits_0_2 = which_door % 8
        data[base_door + 3] = bits_0_2 + bits_3_6
        # Je crois que bit # 7 c'est pour la clé du boss. À vérifier.


def door_remover(data, world, frame, index):  #82C329
    """Retire une porte. Ça retire le mécanisme de déverouillage d'une porte.
    Cependant, le visuel et le physique demeure : les portes resteront là même
    si retirées à l'aide de la présente fonction.

    Args:
        data (bytearray): game data
        world ([type]): World
        frame ([type]): Frame
        index ([type]): Which door to remove
            In case a frame has more than one key locked door.
            It never happen in vanilla. But it works.
    """

    offsets, values = [], []

    offset_Y_1 = data[0x14461 + data[0x14461 + world] + frame]
    if offset_Y_1 != 0:
        current_offset = (data[0x144D7 + offset_Y_1] & 0x00FF) + 0xC4D8
        vanilla_count = deepcopy(data[0x8000 + current_offset])
        data[0x8000 + current_offset] -= 1
        if vanilla_count != 0:  # Data collecting
            current_offset += 1
            for _ in range(vanilla_count):
                tempo, tempo_v = [], []
                # Tilemap locaton [0-1]
                tempo.append(0x8000 + current_offset)
                tempo.append(0x8000 + current_offset + 1)
                tempo_v.append(data[0x8000 + current_offset])
                tempo_v.append(data[0x8000 + current_offset + 1])

                # Forme related [2]
                tempo.append(0x8002 + current_offset)
                tempo_v.append(data[0x8002 + current_offset])
                forme = data[0x8002 + current_offset]
                forme //= 2
                tempo.append(0x14452 + forme)  # Tilemap format to remove.
                tempo_v.append(data[0x14452 + forme])


                # Format de la porte [3] et ses caractéristiques
                tempo.append(0x8003 + current_offset)
                tempo_v.append(data[0x8003 + current_offset])

                door_data = data[0x8003 + current_offset]
                bit_offset = door_data & 0x07

                tempo.append(0x180B8 + bit_offset)
                tempo_v.append(data[0x180B8 + bit_offset])

                bit_to_check = data[0x180B8 + bit_offset]

                offsets.append(tempo)
                values.append(tempo_v)
                current_offset += 4

    # Décalage des valeurs au cas où un frame aurait plus qu'une porte barrée.
        # N'arrivera jamais en vanilla. Mais possiblement au rando et donc on couvre
        # cette possibilité avec ceci!

    for kit_offset in offsets[index:]:
        tempo = []
        current_index = offsets.index(kit_offset)
        try:
            for no, offset in enumerate(kit_offset):
                data[offset] = values[current_index+1][no]
                tempo.append(data[offset])
        except IndexError:
            pass
