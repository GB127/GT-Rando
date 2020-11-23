from debug import debug
from copy import deepcopy

def door_remover(data, world, frame, index):  #82C329
    offsets, values = [], []

    this_world_frame_offset = data[0x14461 + world] + frame
    offset_Y_1 = data[0x14461 + this_world_frame_offset]
    if offset_Y_1 != 0:
        offset_base = data[0x144D7 + offset_Y_1]
        current_offset = (offset_base & 0x00FF) + 0xC4D8
        vanilla_count = deepcopy(data[0x8000 + current_offset])  # + 1 for testing purpose
        data[0x8000 + current_offset] -= 1

        if vanilla_count != 0:  # Data collecting
            current_offset += 1
            for _ in range(vanilla_count):
                tempo, tempo_v = [], []
                tempo.append(0x8003 + current_offset)
                tempo_v.append(data[0x8003 + current_offset])

                door_data = data[0x8003 + current_offset]
                bit_offset = door_data & 0x07

                tempo.append(0x180B8 + bit_offset)
                tempo_v.append(data[0x180B8 + bit_offset])

                bit_to_check = data[0x180B8 + bit_offset]

                tempo.append(0x8000 + current_offset)
                tempo.append(0x8000 + current_offset + 1)

                tempo_v.append(data[0x8000 + current_offset])
                tempo_v.append(data[0x8000 + current_offset + 1])

                # This has been done earlier in the code for some reason.
                tempo.append(0x8002 + current_offset)
                tempo_v.append(data[0x8002 + current_offset])


                something_OxA = data[0x8002 + current_offset]
                # print("0xA", hex(0x8002 + current_offset))

                # ne pas changer ce qui est en dessous jusqu'au append.
                # door_remover
                something_OxA //= 2

                tempo.append(0x14452 + something_OxA)  # Tilemap format to remove.
                tempo_v.append(data[0x14452 + something_OxA])
                offsets.append(tempo)
                values.append(tempo_v)
                current_offset += 4

    for kit_offset in offsets[index:]:
        tempo = []
        current_index = offsets.index(kit_offset)
        try:
            for no, offset in enumerate(kit_offset):
                data[offset] = values[current_index+1][no]
                tempo.append(data[offset])
        except IndexError:
            pass



if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as original:
        game = debug(original.read())
        game.world_select()
        game.setExit(0,0,12)
        game.setExit(0,12,28)
        game.setExit(0,28,12)

        door_remover(game.data, 0, 5, 0)

        with open("debug.smc", "wb") as newgame:
            # print("Time taken to edit files : ", datetime.now() - startTime)
            # print(f"Testing case have been created! {datetime.now()}")
            newgame.write(game.data)
