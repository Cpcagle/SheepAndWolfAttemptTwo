import Creature
import pygame


class Empty(Creature.Creature):
    """
    This class is to add an empty spot into the grid for any place where there is not a creature
    """
    def __init__(self):
        super().__init__("")
        self.energy = 0
        self.max_energy = 0
        self.death_image = pygame.image.load("death_mark.png")
        self.birthRate = 0
        self.birth_amt = 0
        self.birth_requirement = 0
        self.max_birth = 0
        self.type = ""
        self.kill_rate = 0
        self.given_birth = False
        self.dead = False

    def just_died(self):
        """
        Determines if a creature just died
        :return:
        """
        self.dead = True

    def get_death(self):
        """
        Gets the death of the creature
        :return:
        """
        if self.dead:
            self.dead = False
            return True
        return False
