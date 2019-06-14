import Terrain


class Clover(Terrain.Terrain):

    def __init__(self):
        super().__init__("clover")
        self.growth = 7
        self.energy = 2
        self.full_growth = 7
        self.alive_color = (0, 255,   0)
        self.dead_color = (244, 212,  13)

