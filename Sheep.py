import Creature
import pygame


class Sheep(Creature.Creature):
    """
    This class defines the variables for a sheep.
    """
    def __init__(self):
        super().__init__("sheep")
        self.energy = 5
        self.max_energy = 20
        self.already_moved = False
        self.image = pygame.image.load("sheep_img.png")
        self.birthRate = 1
        self.birth_requirement = 5
        self.birth_amt = 0
        self.max_birth = 1
        self.type = "prey"
        self.birth_chance = 6
        self.birth_high = 9
        self.birth_low = 2
        self.too_many = 180
        self.too_little = 30

    def moved(self):
        """
        Moves the sheep
        :return:
        """
        self.energy = self.energy - 1
        self.already_moved = True

    def has_moved(self):
        """
        Determines if the sheep has moved
        :return:
        """
        return self.already_moved

    def action(self, grid, x, y, board_length, sheep_num, sheep_killed):
        """
        This function allows the sheep to eat and move if it is able to
        :param grid: stored data
        :param x: x location
        :param y: y location
        :param board_length: length of the board
        :param sheep_num: sheep amount
        :param sheep_killed: sheep killed
        :return:
        """
        move_x, move_y = self.surrounding_terrain(grid, x, y, board_length)
        if grid[x][y][2].fully_grown():
            grid[x][y][1].eat(grid[x][y][2].get_energy())
            grid[x][y][2].set_growth("eaten")

        return grid, move_x, move_y, sheep_num, sheep_killed

    def surrounding_terrain(self, grid, x, y, board_size):
        """
        creates a list of all the spots surrounding the creature
        :param x: the row of the creature
        :param y: the col of the creature
        :return: list of spots surrounding the creature
        """
        highest_rank = 0
        move_x = 0
        move_y = 0
        choice_list = []

        choice_list.append(self.give_rank(grid[(x - 1) % board_size][y],
                                           (x - 1) % board_size, y))
        choice_list.append(self.give_rank(grid[(x - 1) % board_size][(y - 1) % board_size],
                                           (x - 1) % board_size, (y - 1) % board_size))
        choice_list.append(self.give_rank(grid[x][(y - 1) % board_size], x,
                                           (y - 1) % board_size))
        choice_list.append(self.give_rank(grid[(x + 1) % board_size][(y - 1) % board_size],
                                           (x + 1) % board_size, (y - 1) % board_size))
        choice_list.append(self.give_rank(grid[(x + 1) % board_size][y],
                                           (x + 1) % board_size, y))
        choice_list.append(self.give_rank(grid[(x + 1) % board_size][(y + 1) % board_size],
                                           (x + 1) % board_size, (y + 1) % board_size))
        choice_list.append(self.give_rank(grid[x][(y + 1) % board_size], x,
                                           (y + 1) % board_size))
        choice_list.append(self.give_rank(grid[(x - 1) % board_size][(y + 1) % board_size],
                                           (x - 1) % board_size, (y + 1) % board_size))

        for i in range(len(choice_list)):
            # gets the rank of the neighbors
            neighbor1 = (choice_list[(i + 1) % len(choice_list)][0]) / 2
            neighbor2 = (choice_list[(i - 1) % len(choice_list)][0]) / 2

            # adds the rank of the neighbors to the rank square
            rank = choice_list[i][0] + neighbor1 + neighbor2

            # checks if the rank is the higher than the current highest
            if rank > highest_rank:
                highest_rank = rank
                move_x = choice_list[i][1]
                move_y = choice_list[i][2]

        return move_x, move_y

    def give_rank(self, block, x, y):
        """
        This gives a rank based on the data at the specific location
        :param block: spot being checked
        :param x: x location
        :param y: y location
        :return:
        """
        rank = 0
        # checks if the block contains a predator.
        if block[1].get_type() == "predator":
            rank = rank - 5

        # checks if the block is occupied.
        elif block[1].occupied():
            rank = rank - 3

        # checks if the block contains clover.
        elif block[2].get_terrain_type() == "clover" and block[2].fully_grown():
            rank = rank + 2

        # checks if the block contains grass.
        elif block[2].get_terrain_type() == "grass" and block[2].fully_grown():
            rank = rank + 1

        # returns the rank of the block, the x location, and the y location.
        return [rank, x, y]





