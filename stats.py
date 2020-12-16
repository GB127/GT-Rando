from gameclass import ROM, GT
import numpy
import matplotlib.pyplot as plot
import random
from debug import getoptions_debug
from copy import deepcopy



class stats(ROM):
    all_nFrames = [16, 16, 26, 30, 26]
    def __init__(self):
        self.passwords_data = [
                            [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0], [0,0,0,0]],
                            [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
                            [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
                            [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
                        ]
        self.first = [
            [0 for _ in range(self.all_nFrames[0])],
            [0 for _ in range(self.all_nFrames[1])],
            [0 for _ in range(self.all_nFrames[2])],
            [0 for _ in range(self.all_nFrames[3])],
            [0 for _ in range(self.all_nFrames[4])]
            ]
        self.icy = [
            [0 for _ in range(self.all_nFrames[0])],
            [0 for _ in range(self.all_nFrames[1])],
            [0 for _ in range(self.all_nFrames[2])],
            [0 for _ in range(self.all_nFrames[3])],
            [0 for _ in range(self.all_nFrames[4])]
            ]
        self.dark = [
            [0 for _ in range(self.all_nFrames[0])],
            [0 for _ in range(self.all_nFrames[1])],
            [0 for _ in range(self.all_nFrames[2])],
            [0 for _ in range(self.all_nFrames[3])],
            [0 for _ in range(self.all_nFrames[4])]
            ]

        self.dark_frequency = []

        self.exits = {}

        for world_index in range(5):
            self.exits[world_index] = {}
            for frame in range(stats.all_nFrames[world_index]):
                self.exits[world_index][frame] = [[],[],[],[]]
                for id in range(4):
                    self.exits[world_index][frame][id] = list(0 for _ in range(stats.all_nFrames[world_index]))
    def get_first_rooms(self, data):
        return [(data[0x1FFA7]),
                (data[0x1FFA8]),
                (data[0x1FFA9]),
                (data[0x1FFAA]),
                (data[0x1FFAB])]

    def update(self, data):
        
        def first_update(self,data):
            for world,frame in enumerate(self.get_first_rooms(data)):
                try:
                    self.first[world][frame] += 1
                except IndexError:
                    self.first[world][0] += 1
        

        def passwords_update(self, data):
            def getter_passwords(world):
                """Return the offsets of all passwords
                    """
                return [x for x in range(0x1C67F + 5*(world -1), 0x1C684 + 5*(world-1))]

            for world in range(1,5):
                for box, offset in enumerate(getter_passwords(world)):
                    self.passwords_data[world -1][box][data[offset]] += 1

        def icy_update(self, data):
            def get_iceframes(data):
                """Generate a list of tuples that contains the different frames that are icy.
                    """

                toreturn = []
                for no, offset in enumerate(range(0x1FF35, 0x1FFA7)):
                    if data[offset] & 1:
                        if no in range(0, 16):
                            toreturn.append((0, no))
                        elif no in range(16, 32):
                            toreturn.append((1, no - 16))
                        elif no in range(32, 58):
                            toreturn.append((2, no - 32))
                        elif no in range(58, 88):
                            toreturn.append((3, no - 58))
                        else:
                            toreturn.append((4, no - 88))
                return toreturn

            for tup in get_iceframes(data):
                self.icy[tup[0]][tup[1]] +=1

        def dark_update(self, data):
            def get_darkframes(data):
                """Generate a list of tuples that contains the different frames that are darks.

                    Returns:
                        list: list of tuples
                            tuples : (World, Frame)
                                World : int
                                Frame : int
                    """
                toreturn = []
                for no, offset in enumerate(range(0x1FF35, 0x1FFA7)):
                    if data[offset] & 2:
                        if no in range(0, 16):
                            toreturn.append((0, no))
                        elif no in range(16, 32):
                            toreturn.append((1, no - 16))
                        elif no in range(32, 58):
                            toreturn.append((2, no - 32))
                        elif no in range(58, 88):
                            toreturn.append((3, no - 58))
                        else:
                            toreturn.append((4, no - 88))
                return toreturn

            for tup in get_darkframes(data):
                self.dark[tup[0]][tup[1]] +=1
            self.dark_frequency.append(len(get_darkframes(data)))

        def update_exits(self, data):
            def getExitsFromData(data, world_i, nFrames):
                # J'ai fait ces deux checks au cas où.
                assert isinstance(data, bytearray), "Must be a bytearray"
                assert 0 <= world_i <= 4, "Must be in range 0-4."

                exits_values = []

                # Step 1 : Trouver la base.
                base = data[0x01F303 + world_i]
                for frame_i in nFrames:
                    adjust = 0x1F303 + base + 2*frame_i

                    temp1 = data[0x1F303 + base + 2*frame_i]  # Ceci est l'endroit où es tle count, du moins les deux premiers bytes on a les deux premiers chiffres! (pp)
                    temp2 = data[0x1F303 + base + 2*frame_i + 1]  # Les deux high bytes (HH)
                    temp3 = temp2 * 16 * 16 + temp1  
                    temp4 = 0x10000 + temp3
                    count = data[temp4]

                    for i in range(count):
                        exits_values.append(data[temp4 + 6 * i + 1])
                return exits_values

            for world_index in range(5):
                for frame in range(stats.all_nFrames[world_index]):
                    test = getExitsFromData(data, world_index, [frame])
                    for ind, dest in enumerate(test):
                        self.exits[world_index][frame][ind][dest] += 1


        icy_update(self,data)
        dark_update(self, data)
        first_update(self, data)
        passwords_update(self, data)
        update_exits(self, data)


    def first_plot(self, world):
        x = numpy.arange(self.all_nFrames[world])
        width = 0.15
        plot.bar(x, self.first[world])
        plot.title(f"World {world}")
        plot.show()




    def passwords_plot(self):
        x = numpy.arange(5)
        width = 0.15
        Cherry = [0,0,0,0,0]
        Banana = [0,0,0,0,0]
        RedGem = [0,0,0,0,0]
        BlueGem = [0,0,0,0,0]

        for box, content in enumerate(self.passwords_data[0]):
            Cherry[box] += content[0]
            Banana[box] += content[1]
            RedGem[box] += content[2]
            BlueGem[box] += content[3]

        plot.bar(x - 1.5*width, Cherry, width, label="Cherry")
        plot.bar(x - 0.5*width, Banana, width, label="Banana")
        plot.bar(x + 0.5*width, RedGem, width, label="Red Gem")
        plot.bar(x + 1.5*width, BlueGem, width, label="Blue Gem")
        
        plot.legend()
        plot.show()


    def icy_plot(self, world):
        x = numpy.arange(self.all_nFrames[world])
        width = 0.15
        plot.bar(x, self.icy[world])
        plot.title(f"World {world}")
        plot.show()

    def dark_plot(self, world):
        x = numpy.arange(self.all_nFrames[world])
        width = 0.15
        plot.bar(x, self.dark[world])
        plot.title(f"World {world}")
        plot.show()


    def dark_plot_frequency(self):
        plot.hist(self.dark_frequency,70)
        plot.show()

    def exit_plot_frequency(self, world,frame, index):
        x = numpy.arange(self.all_nFrames[world])
        data = self.exits[world][frame][index]

        width = 0.15
        plot.bar(x, data)
        plot.title(f"World {world}")
        plot.show()



if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as original:
        data = deepcopy(original.read())
        test = stats()
        for _ in range(800):
            game = GT(data, "Stats")
            game.randomizerWithVerification(getoptions_debug())
            test.update(game.data)
        test.exit_plot_frequency(4,20,1)
        test.exit_plot_frequency(4,20,0)