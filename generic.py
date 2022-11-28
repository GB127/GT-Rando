class RandomizerError(BaseException):
    pass

class LogicError(BaseException):
    pass


def room_to_index(tup=None, id=None):
    """Returns (B6, B7), or the id of the level.
        Args:
            tup : (B6, B7) => Returns Id of level
            id : Returns (B6, B7)
    """
    id_per_world =   [0, 16, 32, 58, 88]
    if tup:
        return id_per_world[tup[0]] + tup[1]
    elif id:
        for world, borne in enumerate(id_per_world[-1::-1]):
            if id >= borne:
                return (4 - world, id - borne)
    elif id == 0:
        return (0,0)

if __name__ == "__main__":
    print(room_to_index(tup=(4,5)))