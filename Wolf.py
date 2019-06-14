import Creature
import pygame
import Empty
import random

class Wolf(Creature.Creature):
    """
    This class declares all the variables for a wolf
    """
    def __init__(self):
        super().__init__("wolf")
        self.energy = 7
        self.max_energy = 20
        self.image = pygame.image.load("newWolf.png")
        self.birthRate = .5
        self.already_moved = False
        self.birth_requirement = 30
        self.birth_amt = 0
        self.max_birth = 1
        self.type = "predator"
        self.kill_rate = 75
        self.given_birth = False
        self.birth_chance = 4
        self.birth_high = 8
        self.birth_low = 2
        self.too_many = 40
        self.too_little = 18

    def moved(self):
        """
        Changes the energy of the creature after it moved
        :return:
        """
        self.energy = self.energy - 1
        self.already_moved = True

    def has_moved(self):
        """
        Determines if the creature has moved
        :return:
        """
        return self.already_moved

    def action(self, grid, x, y, board_length, sheep_amt, sheep_killed):
        """
        Action performed by a wolf, kill, move, or starve
        :param grid: stored data
        :param x: x location
        :param y: y location
        :param board_length: size of the grid
        :param sheep_amt: sheep amount
        :param sheep_killed: sheep killed by wolves
        :return:
        """
        kill_x, kill_y, position = self.kill(grid, x, y, board_length)
        # predator has a 100% chance to kill a prey at a perpendicular location
        if position == "no prey":
            move_x, move_y = self.surrounding_creatures(grid, x, y, board_length)
            return grid, move_x, move_y, sheep_amt, sheep_killed

        elif position == "perpendicular":
            grid[kill_x][kill_y][1] = Empty.Empty()
            grid[kill_x][kill_y][1].just_died()
            if self.energy + 5 >= self.max_energy:
                self.energy = self.max_energy
            else:
                self.energy += 5
            sheep_amt -= 1
            sheep_killed += 1

        else:
            kill_chance = random.randint(0, 100)
            # checks if the wolf can kill the predator to its diagonal
            # if the random int in less than or equal to 75
            if kill_chance <= self.kill_rate:
                grid[kill_x][kill_y][1] = Empty.Empty()
                grid[kill_x][kill_y][1].just_died()
                self.energy += 5
                sheep_amt -= 1
                sheep_killed += 1

        move_x, move_y = self.surrounding_creatures(grid, x, y, board_length)

        return grid, move_x, move_y, sheep_amt, sheep_killed

    def surrounding_creatures(self, grid, x, y, board_size):
        """
        creates a list of all the spots surrounding the creature
        :param x: the row of the creature
        :param y: the col of the creature
        :return: list of spots surrounding the creature
        """
        move_x = 0
        move_y = 0
        choice_list = []
        highest_rank = 0

        choice_list.append(self.give_rank(grid, grid[(x - 1) % board_size][y],
                                           (x - 1) % board_size, y, "left", board_size))
        choice_list.append(self.give_rank(grid, grid[(x - 1) % board_size][(y - 1) % board_size],
                                           (x - 1) % board_size, (y - 1) % board_size, "upper left", board_size))
        choice_list.append(self.give_rank(grid, grid[x][(y - 1) % board_size], x,
                                           (y - 1) % board_size, "top", board_size))
        choice_list.append(self.give_rank(grid, grid[(x + 1) % board_size][(y - 1) % board_size],
                                           (x + 1) % board_size, (y - 1) % board_size, "upper right", board_size))
        choice_list.append(self.give_rank(grid, grid[(x + 1) % board_size][y],
                                           (x + 1) % board_size, y, "right", board_size))
        choice_list.append(self.give_rank(grid, grid[(x + 1) % board_size][(y + 1) % board_size],
                                           (x + 1) % board_size, (y + 1) % board_size,"lower right", board_size))
        choice_list.append(self.give_rank(grid, grid[x][(y + 1) % board_size], x,
                                           (y + 1) % board_size, "bottom", board_size))
        choice_list.append(self.give_rank(grid, grid[(x - 1) % board_size][(y + 1) % board_size],
                                           (x - 1) % board_size, (y + 1) % board_size, "lower left", board_size))

        # I need to see if I can
        for i in range(len(choice_list) - 1):

            neighbor1 = choice_list[(i - 1) % len(choice_list)][0]
            neighbor2 = choice_list[(i + 1) % len(choice_list)][0]
            rank = choice_list[i][0] + neighbor1 + neighbor2

            # checks if the rank is the higher than the current highest
            if rank > highest_rank:
                highest_rank = rank
                move_x = choice_list[i][1]
                move_y = choice_list[i][2]

        if highest_rank == 0:
            rand_choice = random.randint(0, len(choice_list) - 1)
            move_x = choice_list[rand_choice][1]
            move_y = choice_list[rand_choice][2]

        return move_x, move_y

    def give_rank(self, grid, block, x, y, position, size):
        """
        Gives each position a rank so the creature can determine where to move
        :param grid: stored data
        :param block: block with data
        :param x: x location
        :param y: y location
        :param position: position being checked
        :param size: size of the board
        :return:
        """
        rank = 0
        # creates a dictionary of all possible functions relative to their
        # positions on the board.
        position_choice = {"left": self.left_right(grid, (x - 1) % size, y, size, rank),
                    "right": self.left_right(grid, (x + 1) % size, y, size, rank),
                    "top": self.top_bottom(grid, x, (y - 1) % size, size, rank),
                    "bottom": self.top_bottom(grid, x, (y + 1) % size, size, rank),
                    "upper_left": self.up_low_left(grid, x, (y - 1) % size, size, rank, "upper left"),
                    "lower_left": self.up_low_left(grid, x, (y + 1) % size, size, rank, "lower left"),
                    "upper_right": self.up_low_right(grid, x, (y - 1) % size, size, rank, "upper right"),
                    "lower_right": self.up_low_right(grid, x, (y + 1) % size, size, rank, "lower right")}

        # checks if the block holds a prey
        if block[1].get_type() == "prey":
            rank = rank + 7

        # there is a problem with this idea because if there are no sheep found then the wolf will keep going
        # back to the exact same spot they came from

        elif not block[2].fully_grown() and block[2].get_terrain_type() == "clover":
            rank = rank + 2
        elif not block[2].fully_grown() and block[2].get_terrain_type() == "grass":
            rank = rank + 1


        elif position == "left":
            rank = position_choice['left']
        elif position == "right":
            rank = position_choice['right']
        elif position == "top":
            rank = position_choice['top']
        elif position == "bottom":
            rank = position_choice['bottom']
        elif position == "upper left":
            rank = position_choice['upper_left']
        elif position == "upper right":
            rank = position_choice['upper_right']
        elif position == "lower left":
            rank = position_choice['lower_left']
        elif position == "lower right":
            rank = position_choice['lower_right']

        return [rank, x, y]

    def left_right(self, grid, x, y, size, rank):
        """
        Checks the left or the right
        :param grid: stored data
        :param x: x location
        :param y: y location
        :param size: size of the grid
        :param rank: rank of the position
        :return:
        """
        # checks left or right
        if grid[x][y][1].get_type() == "prey":
            rank = rank + 3
        # checks bottom side
        elif grid[x][(y + 1) % size][1].get_type() == "prey":
            rank = rank + 3
        # checks top side
        elif grid[x][(y - 1) % size][1].get_type() == "prey":
            rank = rank + 3
        return rank

    def top_bottom(self, grid, x, y, size, rank):
        """
        Checks the top or bottom position
        :param grid: stored data
        :param x: x location
        :param y: y location
        :param size: size of the grid
        :param rank: rank of spot
        :return:
        """
        # checks top or bottom
        if grid[x][y][1].get_type() == "prey":
            rank = rank + 3
        # checks left side
        elif grid[(x - 1) % size][y][1].get_type() == "prey":
            rank = rank + 3
        # checks right side
        elif grid[(x + 1) % size][y][1].get_type() == "prey":
            rank = rank + 3
        return rank

    def up_low_left(self, grid, x, y, size, rank, position):
        """
        Checks the upper and lower left positions
        :param grid: stored data
        :param x: x location
        :param y: y location
        :param size: size of the grid
        :param rank: rank of the position
        :param position: position being checked
        :return:
        """
        # checks upper left
        if grid[x][(y + 1) % size][1].get_type() == "prey":
            rank = rank + 3
        # checks left
        elif grid[x][y][1].get_type() == "prey":
            rank = rank + 3
        # checks lower left
        elif grid[x][(y - 1) % size][1].get_type() == "prey":
            rank = rank + 3

        elif position == "upper left":
            # checks top
            if grid[(x + 1) % size][(y - 1) % size][1].get_type() == "prey":
                rank = rank + 3
            # checks upper right, on the left
            elif grid[(x + 2) % size][(y - 1) % size][1].get_type() == "prey":
                rank = rank + 3

        elif position == "lower left":
            # checks bottom
            if grid[(x + 1) % size][(y + 1) % size][1].get_type() == "prey":
                rank = rank + 3
            # checks lower right, on the left
            elif grid[(x + 2) % size][(y + 1) % size][1].get_type() == "prey":
                rank = rank + 3

        return rank

    def up_low_right(self, grid, x, y, size, rank, position):
        """
        This will check the upper and lower left spots
        :param grid: stored data
        :param x: x location
        :param y: y location
        :param size: size of the grid
        :param rank: rank the position has
        :param position: spot being checked
        :return:
        """
        # checks upper right
        if grid[x][(y + 1) % size][1].get_type() == "prey":
            rank = rank + 3
        # checks right
        elif grid[x][y][1].get_type() == "prey":
            rank = rank + 3
        # checks lower right
        elif grid[x][(y - 1) % size][1].get_type() == "prey":
            rank = rank + 3

        elif position == "upper right":
            # checks top
            if grid[(x - 1) % size][(y - 1) % size][1].get_type() == "prey":
                rank = rank + 3
            # checks upper left, on the right
            elif grid[(x - 2) % size][(y - 1) % size][1].get_type() == "prey":
                rank = rank + 3

        elif position == "lower right":
            # checks bottom
            if grid[(x - 1) % size][(y + 1) % size][1].get_type() == "prey":
                rank = rank + 3
            # checks lower left, on the right
            elif grid[(x - 2) % size][(y + 1) % size][1].get_type() == "prey":
                rank = rank + 3

        return rank

    def kill(self, grid, x, y, board_size):
        """
        This will try and kill a sheep if in the kill zone
        :param grid: stored data
        :param x: x location
        :param y: y location
        :param board_size: size of the board
        :return:
        """

        kill_perpendicular = []
        kill_diagonal = []

        kill_perpendicular.append([grid[(x - 1) % board_size][y],
                                   (x - 1) % board_size, y])
        kill_diagonal.append([grid[(x - 1) % board_size][(y - 1) % board_size],
                              (x - 1) % board_size, (y - 1) % board_size])
        kill_perpendicular.append([grid[x][(y - 1) % board_size], x,
                                   (y - 1) % board_size])
        kill_diagonal.append([grid[(x + 1) % board_size][(y - 1) % board_size],
                              (x + 1) % board_size, (y - 1) % board_size])
        kill_perpendicular.append([grid[(x + 1) % board_size][y],
                                   (x + 1) % board_size, y])
        kill_diagonal.append([grid[(x + 1) % board_size][(y + 1) % board_size],
                              (x + 1) % board_size, (y + 1) % board_size])
        kill_perpendicular.append([grid[x][(y + 1) % board_size], x,
                                   (y + 1) % board_size])
        kill_diagonal.append([grid[(x - 1) % board_size][(y + 1) % board_size],
                              (x - 1) % board_size, (y + 1) % board_size])

        # adds all spots that hold a prey to the select list
        # need to make a while loop for this with an index and count
        i = 0
        count = 0
        perp_amt = len(kill_perpendicular)
        while i < perp_amt:
            # increment i no matter what
            i = i + 1
            # if not prey
            if not kill_perpendicular[count][0][1].get_type() == "prey":
                kill_perpendicular.pop(count)
            else:
                # increment the count because nothing was pop'd off
                count = count + 1

        # resets the count and index variable
        i = 0
        count = 0
        # checks to see if kill perpendicular is empty
        if not kill_perpendicular:
            diag_amt = len(kill_diagonal)
            while i < diag_amt:
                # increment i no matter what
                i = i + 1
                # if not prey
                if not kill_diagonal[count][0][1].get_type() == "prey":
                    # appends the block with prey to diagonal_select
                    kill_diagonal.pop(count)
                else:
                    # increment the count because nothing was pop'd off
                    count = count + 1

            if not kill_diagonal:
                return x, y, "no prey"
            else:
                # randomly selects a block with a prey in it to kill
                selection = random.randint(0, len(kill_diagonal) - 1)
                return kill_diagonal[selection][1], kill_diagonal[selection][2], "diagonal"
        else:
            # len starts at 1 while lists start at 0
            # randomly selects a block with a prey in it to kill
            selection = random.randint(0, len(kill_perpendicular) - 1)
            return kill_perpendicular[selection][1], kill_perpendicular[selection][2], "perpendicular"




