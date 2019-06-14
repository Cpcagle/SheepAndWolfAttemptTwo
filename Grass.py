import Terrain


class Grass(Terrain.Terrain):

    def __init__(self):
        super().__init__("grass")
        self.growth = 4
        self.energy = 1
        self.full_growth = 4
        self.alive_color = (10,  80,  10)
        self.dead_color = (244, 185,  75)



