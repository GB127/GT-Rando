def passwords(self, world):
    return [self[x] for x in range(0x1C67F + 5*world, 0x1C682 + 5*world)]

def range_passwords(self):
    return [range(0x1C67F, 0x1C93)]