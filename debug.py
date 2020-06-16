def test_boss_w0(game):
    # This code changes 0-0 up exit to the boss.
    game[0x1F3ED] = 14
