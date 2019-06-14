# creature class that inherits wolf, sheep, and other animals.
#    @author: cameron cagle
#    @version: 10/18/19
from random import *
import pygame

class Creature:
    count = 0

    # think about adding in a random birth value at 4% for sheep and 5% for wolves.

    # rand(0, 100) >=
    def __init__(self, creature):
        self.creature = creature
        self.energy = 0
        self.max_energy = 0
        self.image = pygame.Surface([0, 0])
        self.birthRate = 0
        self.birth_requirement = 0
        self.max_birth = 0
        self.already_moved = False
        self.type = ""
        self.given_birth = False
        self.birth_chance = 0
        self.birth_high = 0
        self.birth_low = 0
        self.too_many = 0
        self.too_little = 0

    def natural_birth(self, creature_amt):
        """
        Checks how many creatures are on the grid and what the birth rate should be based off that data
        :param creature_amt: amount of creatures in simulation
        :return:
        """
        if creature_amt < self.too_little:
            return self.birth_high
        elif creature_amt > self.too_many:
            return self.birth_low
        else:
            return self.birth_chance

    def get_image(self):
        """
        Gets the image of the creature
        :return: image
        """
        return self.image

    def clear(self):
        """
        resets the creatures movement ability.
        :return:
        """
        self.already_moved = False

    def get_creature(self):
        """
        gets the creature type
        :return: creature
        """
        return self.creature

    def set_creature(self, creature):
        """
        sets the creature type
        :param creature: type of creature
        :return: NULL
        """
        self.creature = creature

    def is_open(self):
        """
        checks if the spot is open.
        :return: true if the spot is open.
        """
        if self.creature == "":
            return True
        else:
            return False

    def get_life(self):
        """
        gets the life
        :return: returns life
        """
        return self.life

    def set_life(self, life):
        """
        sets the life
        :param life: the life of the creature
        :return: NULL
        """
        self.life = life

    def get_energy(self):
        """
        gets the energy of the sheep
        :return: the energy of the sheep
        """
        return self.energy

    def set_energy(self, energy):
        """
        sets the energy of the creature
        :param energy: energy of creature
        :return:
        """
        self.energy = energy

    def eat(self, energy_added):
        """
        adds energy to the creature
        :param energy_added: energy to be added to the creature
        :return:
        """
        if self.energy + energy_added >= self.max_energy:
            self.energy = self.max_energy
        else:
            self.energy += energy_added

    def display(self, surf, rect, blocksize, just_died):
        """
        creates an image to display for the creature
        :param board: the grid/ board
        :param row: the row of the creature
        :param col: the col of the creature
        :return: an image of the creature
        """
        surf.blit((pygame.transform.smoothscale(self.image,(blocksize,blocksize))), rect)
        if just_died:
            surf.blit((pygame.transform.smoothscale(self.death_image, (blocksize, blocksize))), rect)


    def get_birth_rate(self):
        """
        gets the birth rate of the creature
        :return: birth rate
        """
        return self.birthRate

    def able_to_birth(self):
        """
        determines if the creature has enough energy to give birth
        :return: true if the creature can give birth
        """
        if self.energy > self.birth_requirement:
            return True
        return False

    def has_birthed(self):
        """
        decreases the creatures energy by 1/4th the original amount
        :return: null
        """
        self.energy = self.energy - (self.energy / 2)

    def occupied(self):
        """
        determines if the spot given is occupied or not
        :return: true if the spot is occupied
        """
        if self.creature == "sheep" or self.creature == "wolf":
            return True
        else:
            return False

    def get_type(self):
        """
        gets predator or prey based on the type
        :return: the type of the creature
        """
        return self.type





