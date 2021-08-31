class RandomizerError(BaseException):
    pass

def world_indexes(world=None):
    if world or world==0:
        assert 0 <= world <= 4, "World must be 0, 1, 2, 3 or 4"
        id_per_world =   [0, 16, 32, 58, 88, 114]
        return range(id_per_world[world], id_per_world[world+1])
    return range(114)

def room_to_index(tup=None, id=None):
        id_per_world =   [0, 16, 32, 58, 88]
        if tup:
            return id_per_world[tup[0]] + tup[1]
        elif id:
            for world, borne in enumerate(id_per_world[-1::-1]):
                if id >= borne:
                    return (4 - world, id - borne)
        elif id == 0:
            return (0,0)

