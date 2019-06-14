import pygame

class Terrain:
    """
    This class defines all the methods that terrain is allowed to do.
    """
    def __init__(self, terrain_type):
        self.terrain_type = terrain_type
        self.growth = 0
        self.energy = 0
        self.full_growth = 0
        self.color = (255, 255, 255)
        self.alive_color = (255, 255, 255)
        self.dead_color = (255, 255, 255)

    def get_color(self):
        """
        gets the color
        :return: color
        """
        return self.color

    def get_dead_color(self):
        """
        gets the color of dead terrain
        :return: color
        """
        return self.dead_color

    def set_terrain_type(self, terrain_type):
        """
        sets the type of terrain
        :param terrain_type: terrain type
        :return:
        """
        self.terrain_type = terrain_type

    def get_terrain_type(self):
        """
        gets the type of terrain
        :return: terrain
        """
        return self.terrain_type

    def get_growth(self):
        """
        gets the growth
        :return: growth
        """
        return self.growth_rate

    def set_growth(self, growth):
        """
        sets the growth of terrain
        :param growth: growth of terrain
        :return:
        """
        if growth == "eaten":
            self.growth = 0

    def get_energy(self):
        """
        gets energy
        :return: energy
        """
        return self.energy

    def set_energy(self, energy):
        """
        sets energy
        :param energy:
        :return:
        """
        self.energy = energy

    def fully_grown(self):
        """
        Determines if the terrain is fully grown
        :return:
        """
        if self.growth == self.full_growth:
            return True
        return False

    def grow(self):
        """
        Grows the terrain
        :return:
        """
        if self.growth + 1 >= self.full_growth:
            self.growth = self.full_growth
        else:
            self.growth += 1

    def set_color(self, life):
        """
        sets the color
        :param life: type of color
        :return:
        """
        if life == "alive":
            self.color = self.alive_color
        else:
            self.color = self.dead_color
