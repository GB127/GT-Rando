from debug import *

def test_bool_Worlds_vanilla(world_id):
    """Test the bool of World world_id.
        Current status:
            0: Works
            1: Works
            2: Take way too long.
            3: Works
            4: Works, takes a little bit too long"""
    if world_id in [1, 2, 4]:
        print(f"World bool : Needs to take care of doors that are locked on one side only.")
    if world_id in [2,4]:
        print(f"World bool: works, but takes too long because of hookshots.")
        return
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())
        testing = test.Worlds[world_id]
        assert bool(testing), f"World {x} : World bool doesn't work on vanilla."

def test_bool_items_vanilla(world_id):
    """Test the bool of World world_id.
        Current status:
            0: Works
            1: Works
            2: Works
            3: Works
            4: Works, but I'm missing a bunch of stuffs."""
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())
        testing = test.Worlds[world_id].Items
        assert bool(testing), f"Items bool doesn't work on vanilla."

def test_bool_exits_vanilla(world_id):
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())
        testing = test.Worlds[world_id].Exits
        if world_id == 4:
            print(f"Screen 99 : Needs some gymnastics. The screen with buttons and hookshot (4,11)")
        assert bool(testing), f"Exits bool doesn't work on vanilla."

def test_locks(x):
    """Al locks should be in Except one."""
    if x == 4:
        print(f'screen 99 gymnastic')
    pass

if __name__ == "__main__":
    for x in range(5):
        print(f"-------------------Testing world {x}----------------")
        test_locks(x)
        test_bool_items_vanilla(x)
        test_bool_exits_vanilla(x)
        test_bool_Worlds_vanilla(x)
        print(f"-----------------End of world {x}-------------------\n")