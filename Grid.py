import copy
import Empty
import pygame
import Terrain
import Creature
import Grass
import Clover
import random
import Sheep
import Wolf


class Grid:
    count = 0

    def __init__(self, block_size, width, height, display_surf):
        self.grid = []
        self.block_size = block_size
        self.width = width
        self.height = height
        self.display_surf = display_surf
        self.creature_cnt = 0
        self.length = 0
        self.sheep = 0
        self.wolves = 0
        self.max_sheep = 0
        self.max_wolves = 0
        self.sheep_starved = 0
        self.wolves_starved = 0
        self.sheep_killed = 0

        # Colors needed to make the terrain of the grid
        self.GRASS      = ( 10,  80,  10)
        self.CLOVER     = (  0, 255,   0)
        self.DEADGRASS  = (244, 185,  75)
        self.DEADCLOVER = (244, 212,  13)


    def generate_grid(self, surf):
        """
        Generates a new grid with randomized terrain covering the map.
        :param surf: surface images are displayed to
        :return: stored data
        """
        row_len = 0
        for row in range(self.width // self.block_size):
            col_len = 0
            self.grid.append([])
            for col in range(self.height // self.block_size):
                grass_or_clover = random.randint(0, 5)
                spot = [[row_len, col_len, self.block_size, self.block_size], Creature.Creature(""),
                        Terrain.Terrain(""), ]
                spot[1] = Empty.Empty()
                if grass_or_clover > 1:
                    spot[2] = Grass.Grass()
                else:
                    spot[2] = Clover.Clover()
                spot[2].set_color("alive")
                spot.append(pygame.draw.rect(surf, spot[2].get_color(), spot[0]))
                self.grid[row].append(spot)
                col_len += self.block_size
            row_len += self.block_size
        return self.grid

    def draw_grid(self, grid, surf, blocksize):
        """
        Draws the grid to the screen and displays all the images.
        :param grid: stored data
        :param surf: surface images are displayed to
        :param blocksize: size of blocks/ spot
        """
        for row in range(self.width // self.block_size):
            for col in range(self.height // self.block_size):
                grid[row][col][3] = pygame.draw.rect(surf, grid[row][col][2].get_color(), grid[row][col][0])
                if grid[row][col][1].get_creature() == "sheep" or grid[row][col][1].get_creature() == "wolf":
                    grid[row][col][1].display(surf, grid[row][col][3], blocksize, False)
                elif grid[row][col][1].get_creature() == "" and grid[row][col][1].get_death():
                    grid[row][col][1].display(surf, grid[row][col][3], blocksize, True)

    def reset_grid(self, grid):
        """
        resets all the creatures to be able to move again
        :param board: the simulation being reset
        :return: NULL
        """
        for row in range(self.width // self.block_size):
            for col in range(self.height // self.block_size):
                grid[row][col][1].clear()

    def add_creatures(self, grid, title, creature_amt, grid_len):
        """
        This will add creatures into the simulation in a random location on the grid
        :param grid: stored data
        :param title: type of creature
        :param creature_amt: amount of specific type of creature
        :param grid_len: length of grid
        :return: updated data
        """
        creature_amt = int(creature_amt)
        while self.creature_cnt < creature_amt:
            if title == "sheep":
                creature_row = random.randint(0, grid_len - 1)
                creature_col = random.randint(0, grid_len - 1)
                if grid[creature_row][creature_col][1].is_open():
                    grid[creature_row][creature_col][1] = Sheep.Sheep()
                self.creature_cnt += 1
            elif title == "wolves":
                creature_row = random.randint(0, grid_len - 1)
                creature_col = random.randint(0, grid_len - 1)
                if grid[creature_row][creature_col][1].is_open():
                    grid[creature_row][creature_col][1] = Wolf.Wolf()
                self.creature_cnt += 1

        if title == "sheep":
            self.sheep = self.creature_cnt
            self.max_sheep = self.sheep
        else :
            self.wolves = self.creature_cnt
            self.max_wolves = self.wolves
        self.creature_cnt = 0
        return grid

    def update_grid(self, grid, surf, grid_len):
        """
        This will update the grid one iteration, this is called in a while loop while the program is in start mode.
        :param grid: stored data
        :param surf: surface images are displayed to
        :param grid_len: length of the grid
        :return:
        """
        # do I need to do this if I return the grid every time it updates
        # (change all of the grids to self.grid) self.grid = grid
        self.length = int(grid_len)
        # this should relate to my stop and start button
        for row in range(0, int(grid_len)):
            for col in range(0, int(grid_len)):
                if self.grid[row][col][1].occupied() and self.grid[row][col][1].get_energy() > 0 and\
                        not self.grid[row][col][1].has_moved():
                    if grid[row][col][1].get_creature() == "sheep":
                        grid = self.creature_move(grid, row, col, self.sheep)
                    else:
                        grid = self.creature_move(grid, row, col, self.wolves)

        # reset all the creatures in the grid after they have moved
        self.reset_grid(grid)
        for row in range(0, int(grid_len)):
            for col in range(0, int(grid_len)):
                # is it possible to combine these to functions to a (check_grid)
                grid = self.creature_death_check(grid, row, col, self.sheep, self.wolves)
                self.check_terrain(grid, surf, row, col)

        if self.sheep > self.max_sheep:
            self.max_sheep = self.sheep
        if self.wolves > self.max_wolves:
            self.max_wolves = self.wolves

        return grid, self.sheep, self.wolves, self.sheep_starved, self.sheep_killed, self.max_sheep, self.max_wolves,\
               self.wolves_starved

    def creature_move(self, grid, x, y, creature_amt):
        """
        this allows for the creature to move around the grid. It also checks to see if the creature can reproduce or eat.
        :param grid: stored data
        :param x: x location
        :param y: y location
        :param creature_amt: amount of creature
        :return:
        """
        self.reproduction(grid, x, y, creature_amt)
        grid, move_x, move_y, self.sheep, self.sheep_killed = grid[x][y][1].action(grid, x, y, self.length, self.sheep,
                                                                                   self.sheep_killed)
        grid = self.swap(grid, move_x, move_y, x, y)
        return grid

    def reproduction(self, grid, creatureX, creatureY, creature_amt):
        """
        This produces a child of the creature depending on whether the creature meets the requirements
        :param grid: stored data
        :param creatureX: x location
        :param creatureY: y location
        :param creature_amt: amount of creature
        :return:
        """
        parent = grid[creatureX][creatureY][1]
        birth_chance = random.randint(0, 100)
        babyX, babyY = self.check_surroundings(grid, creatureX, creatureY, "")
        if birth_chance <= parent.natural_birth(creature_amt):
            if parent.get_creature() == "sheep":
                grid[babyX][babyY][1] = Sheep.Sheep()
                self.sheep += 1
                return grid
            else:
                grid[babyX][babyY][1] = Wolf.Wolf()
                self.wolves += 1
                return grid
        else:
            return grid





    def check_surroundings(self, grid, x, y, creature):
        """
        creates a list of all the spots surrounding the creature
        :param x: the row of the creature
        :param y: the col of the creature
        :return: list of spots surrounding the creature
        """

        if grid[(x - 1) % self.length][y][1].get_creature() == creature:
            return (x - 1) % self.length, y
        if grid[x][(y + 1) % self.length][1].get_creature() == creature:
            return x, (y + 1) % self.length
        if grid[(x + 1) % self.length][y][1].get_creature() == creature:
            return (x + 1) % self.length, y
        if grid[x][(y - 1) % self.length][1].get_creature() == creature:
            return x, (y - 1) % self.length
        if grid[(x - 1) % self.length][(y - 1) % self.length][1].get_creature() == creature:
            return (x - 1) % self.length, (y - 1) % self.length
        if grid[(x - 1) % self.length][(y + 1) % self.length][1].get_creature() == creature:
            return (x - 1) % self.length, (y + 1) % self.length
        if grid[(x + 1) % self.length][(y + 1) % self.length][1].get_creature() == creature:
            return (x + 1) % self.length, (y + 1) % self.length
        if grid[(x + 1) % self.length][(y - 1) % self.length][1].get_creature() == creature:
            return (x + 1) % self.length, (y - 1) % self.length
        return x, y



    def swap(self, grid, open_x, open_y , row, col):
        """
        Swaps a creature object with a None object
        :param index1: first index to be swapped
        :param index2: second index to be swapped
        :return: None
        """
        grid[row][col][1].moved()
        # this will swap the creature with the spot it is moving to
        grid[row][col][1], grid[open_x][open_y][1] = grid[open_x][open_y][1], grid[row][col][1]
        return grid

    def creature_death_check(self, grid, row, col, sheep, wolves):
        """
        Sets the creature to empty and undraws the creature
        :param row
        :param col
        :param sheep
        :param wolves
        :param grid
        :return: none
        """
        if not grid[row][col][1].is_open() and grid[row][col][1].get_energy() <= 0:
            if grid[row][col][1].get_creature() == "sheep":
                self.sheep -= 1
                self.sheep_starved += 1
                grid[row][col][1] = Empty.Empty()
                return grid
            else:
                self.wolves -= 1
                self.wolves_starved += 1
                grid[row][col][1] = Empty.Empty()
                return grid
        else:
            return grid

    def check_terrain(self, grid, surf, row, col):
        """
        checks each terrain and determines if it is alive or dead and redraws the image
        :param row is the row of the grid
        :param col is the col of the grid
        :param grid is the grid
        :return: none
        """
        # if the terrain is fully grown
        if grid[row][col][2].fully_grown():
            grid[row][col][2].set_color("alive")
        # if the terrain is eaten
        elif not grid[row][col][2].fully_grown():
            grid[row][col][2].set_color("dead")
        # grow the grass by one instance
        grid[row][col][2].grow()








