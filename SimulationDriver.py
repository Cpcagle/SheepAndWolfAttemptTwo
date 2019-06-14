from Grid import *
import pygame
import sys
import Button
import InputBox
import DrawText

class SimulationDriver:

    def __init__(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT, PAUSE

        self.width = 608
        self.height = 608
        self.blocksize = 14
        self.sheep = None
        self.wolves = None
        self.max_sheep = 0
        self.max_wolves = 0
        self.sheep_starved = 0
        self.wolves_starved = 0
        self.sheep_killed = 0
        self.simulation_ready = False

        # Colors of the terrain for program
        self.GRASS       = ( 10,  80,  10)
        self.CLOVER      = (  0, 255,   0)
        self.DEADGRASS   = (244, 185,  75)
        self.DEADCLOVER  = (244, 212,  13)
        self.WHITE       = (255, 255, 255)
        self.BUTTONCOLOR = (200, 200, 200)
        self.BUTTONCLICK = (255, 255,   0)
        self.grid = []
        self.fps = 6

        pygame.init()
        PAUSE = False
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.width + 360, self.height + 30))
        DISPLAYSURF.fill([0, 0, 0])
        self.INPUTSURF = pygame.display.set_mode((self.width + 360, self.height + 30))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Sheep & Wolves Simulation')

    def simulation_setup(self):
        """
        sets up the simulation by creating the grid and the GUI
        """
        simulation_grid = Grid(self.blocksize, self.width, self.height, DISPLAYSURF)

        # do i need to return the grid here to add sheep and wolves
        self.grid = simulation_grid.generate_grid(DISPLAYSURF)
        self.saved_grid = simulation_grid.generate_grid(DISPLAYSURF)

        # adding all the buttons to the GUI
        start_button = Button.button(self.BUTTONCOLOR, self.width + 20, 20, 150, 60, DISPLAYSURF, 'START')
        stop_button = Button.button(self.BUTTONCOLOR, self.width + 190, 20, 150, 60, DISPLAYSURF, 'STOP')
        save_button = Button.button(self.BUTTONCOLOR, self.width + 20, 100, 150, 60, DISPLAYSURF, 'SAVE')
        load_button = Button.button(self.BUTTONCOLOR, self.width + 190, 100, 150, 60, DISPLAYSURF, 'LOAD')

        wolf_in_txt = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Initial Wolves: ', self.width + 100,
                                        (self.height / 2) - 80)
        sheep_in_txt = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Initial Sheep: ', self.width + 100,
                                         (self.height / 2) - 120)
        wolf_starve = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Wolves starved: ', self.width + 100,
                                        self.height / 2)
        sheep_starve = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Sheep starved: ', self.width + 100,
                                         (self.height / 2) - 40)
        max_sheep = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Max sheep: ', self.width + 100,
                                      (self.height / 2) + 40)
        max_wolves = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Max wolves: ', self.width + 100,
                                       (self.height / 2) + 80)
        sheep_killed = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Sheep killed: ', self.width + 100,
                                         (self.height / 2) + 120)
        wolf_starve_num = DrawText.DrawText(BASICFONT, DISPLAYSURF, self.wolves_starved, self.width + 210,
                                            (self.height / 2) - 40)
        sheep_starve_num = DrawText.DrawText(BASICFONT, DISPLAYSURF, self.sheep_starved, self.width + 210,
                                             self.height / 2)
        max_sheep_num = DrawText.DrawText(BASICFONT, DISPLAYSURF, self.max_sheep, self.width + 210,
                                          (self.height / 2) + 40)
        max_wolves_num = DrawText.DrawText(BASICFONT, DISPLAYSURF, self.max_wolves, self.width + 210,
                                           (self.height / 2) + 80)
        sheep_killed_num = DrawText.DrawText(BASICFONT, DISPLAYSURF, self.sheep_killed, self.width + 210,
                                             (self.height / 2) + 120)

        wolf_cnt = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Wolf Count: ', 200,
                                     self.height + 5)
        sheep_cnt = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'Sheep Count: ', 400,
                                      self.height + 5)
        sheep_num = DrawText.DrawText(BASICFONT, DISPLAYSURF, self.sheep, 485,
                                      self.height + 5)
        wolf_num = DrawText.DrawText(BASICFONT, DISPLAYSURF, self.wolves, 285,
                                     self.height + 5)
        author = DrawText.DrawText(BASICFONT, DISPLAYSURF, 'By: Cameron Cagle', self.width + 170,
                                   (self.height / 2) + 290)

        title2 = DrawText.DrawText(pygame.font.Font('freesansbold.ttf', 35), DISPLAYSURF, 'SIMULATION',
                                   self.width + 170, (self.height / 2) + 230)
        title = DrawText.DrawText(pygame.font.Font('freesansbold.ttf', 35), DISPLAYSURF, 'SHEEP & WOLF',
                                  self.width + 170, (self.height / 2) + 200)
        background2 = DrawText.DrawText(pygame.font.Font('freesansbold.ttf', 38), DISPLAYSURF, 'SIMULATION',
                                        self.width + 170, (self.height / 2) + 230)
        background = DrawText.DrawText(pygame.font.Font('freesansbold.ttf', 38), DISPLAYSURF, 'SHEEP & WOLF',
                                       self.width + 170, (self.height / 2) + 200)
        sheep_input = InputBox.InputBox(self.width + 180, (self.height / 2) - 125, 60, 30, BASICFONT, 'sheep',
                                        self.INPUTSURF)
        wolf_input = InputBox.InputBox(self.width + 180, (self.height / 2) - 85, 60, 30, BASICFONT, 'wolf',
                                       self.INPUTSURF)

        press_button = [start_button, stop_button, save_button, load_button]
        txt_boxes = [wolf_in_txt, sheep_in_txt, sheep_cnt, wolf_cnt, sheep_starve, wolf_starve, max_sheep, max_wolves,
                     title, title2, author, sheep_killed]
        color_boxes = [background, background2]
        input_boxes = [sheep_input, wolf_input]
        if self.simulation_intro(simulation_grid, txt_boxes, color_boxes, input_boxes, press_button, sheep_num,
                                 wolf_num, wolf_input, sheep_input,wolf_starve_num, sheep_starve_num, max_sheep_num,
                                 max_wolves_num, sheep_killed_num):
            simulation_ready = True
        setup = True
        while setup:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.isOver(mouse_pos) and simulation_ready:
                        self.simulation_loop(simulation_grid, press_button, txt_boxes, color_boxes, input_boxes,
                                             sheep_num, wolf_num, stop_button, start_button, wolf_starve_num,
                                             sheep_starve_num, max_sheep_num, max_wolves_num, sheep_killed_num)
                    if load_button.isOver(mouse_pos):
                        print("load")
                    if save_button.isOver(mouse_pos):
                        print("save")

            DISPLAYSURF.fill((0, 0, 0))
            self.redraw_screen(txt_boxes, color_boxes, input_boxes, press_button, sheep_num, wolf_num,
                               wolf_starve_num, sheep_starve_num, max_sheep_num, max_wolves_num, sheep_killed_num )
            simulation_grid.draw_grid(self.grid, DISPLAYSURF, self.blocksize)
            pygame.display.update()

    def simulation_intro(self, simulation_grid, txt_boxes, color_boxes, input_boxes, press_button, sheep_num, wolf_num,
                         wolf_input, sheep_input, wolf_starve_num, sheep_starve_num, max_sheep_num, max_wolves_num,
                         sheep_killed_num):
        """
        This function makes sure that the user has input two values for the amount of sheep and wolves.
        :param simulation_grid: stored data
        :param txt_boxes: all text boxes
        :param color_boxes: colored text
        :param input_boxes: input boxes
        :param press_button: buttons
        :param sheep_num: number of sheep
        :param wolf_num: number of wolves
        :param wolf_input: wolf input
        :param sheep_input: sheep input
        :param wolf_starve_num: wolves starved
        :param sheep_starve_num: sheep starved
        :param max_sheep_num: max sheep in the simulation
        :param max_wolves_num: max wolves in the simulation
        :param sheep_killed_num: sheep killed in simulation
        :return:
        """
        intro = True

        sheep_start = False
        wolf_start = False
        while intro:
            DISPLAYSURF.fill((0, 0, 0))
            self.redraw_screen(txt_boxes, color_boxes, input_boxes, press_button, sheep_num, wolf_num,
                               wolf_starve_num, sheep_starve_num, max_sheep_num, max_wolves_num, sheep_killed_num)
            simulation_grid.draw_grid(self.grid, DISPLAYSURF, self.blocksize)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if self.sheep is None:
                    self.sheep = sheep_input.handle_event(event)
                elif sheep_start is not True:
                    self.grid = simulation_grid.add_creatures(self.grid, "sheep", self.sheep,
                                                              self.width // self.blocksize)
                    sheep_start = True

                if self.wolves is None:
                    self.wolves = wolf_input.handle_event(event)
                elif wolf_start is not True:
                    self.grid = simulation_grid.add_creatures(self.grid,  "wolves", self.wolves,
                                                              self.width // self.blocksize)
                    wolf_start = True

            if wolf_start and sheep_start:
                return True

    def simulation_loop(self, simulation_grid, press_button, txt_boxes, color_boxes, input_boxes, sheep_num, wolf_num,
                        stop_button, start_button, wolf_starve_num, sheep_starve_num, max_sheep_num, max_wolves_num,
                        sheep_killed_num):
        """
        This will run the simulation on a loop until an event is pressed to stop or load another simulation.
        :param simulation_grid: stored data
        :param txt_boxes: all text boxes
        :param color_boxes: colored text
        :param input_boxes: input boxes
        :param press_button: buttons
        :param sheep_num: number of sheep
        :param wolf_num: number of wolves
        :param wolf_input: wolf input
        :param sheep_input: sheep input
        :param wolf_starve_num: wolves starved
        :param sheep_starve_num: sheep starved
        :param max_sheep_num: max sheep in the simulation
        :param max_wolves_num: max wolves in the simulation
        :param sheep_killed_num: sheep killed in simulation
        :return:
        """

        loop = True
        count = 0
        while loop:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if stop_button.isOver(mouse_pos):
                        self.simulation_pause(simulation_grid, txt_boxes, color_boxes, input_boxes, press_button,
                                              sheep_num, wolf_num, stop_button, start_button, wolf_starve_num,
                                              sheep_starve_num, max_sheep_num, max_wolves_num, sheep_killed_num)

            # this will keep running until the pause button is pressed.
            self.grid, self.sheep, self.wolves, self.sheep_starved, self.sheep_killed, self.max_sheep, self.max_wolves,\
            self.wolves_starved = simulation_grid.update_grid(self.grid, DISPLAYSURF, self.width / self.blocksize)
            DISPLAYSURF.fill((0, 0, 0))
            self.redraw_screen(txt_boxes, color_boxes, input_boxes, press_button, sheep_num, wolf_num, wolf_starve_num,
                               sheep_starve_num, max_sheep_num, max_wolves_num, sheep_killed_num)
            simulation_grid.draw_grid(self.grid, DISPLAYSURF, self.blocksize)
            pygame.display.update()
            FPSCLOCK.tick(self.fps)
            count += 1

    def redraw_screen(self, txt, txt_color, input, press_button, shp_counter, wolf_counter, wolf_starve_num,
                      sheep_starve_num, max_sheep_num, max_wolves_num, sheep_killed_num):
        """
        This function redraws the GUI and clears the old one from memory.
        :param txt: txt boxes
        :param txt_color: txt boxes with color
        :param input: input boxes
        :param press_button: buttons
        :param shp_counter: sheep counter
        :param wolf_counter: wolf counter
        :param wolf_starve_num: wolves starved
        :param sheep_starve_num: sheep starved
        :param max_sheep_num: max sheep
        :param max_wolves_num: max wolves
        :param sheep_killed_num: sheep killed by wolves
        """
        # draw buttons
        for press in press_button:
            press.draw(self.WHITE)

        for color in txt_color:
            color.draw_color()

        # draw txt boxes
        for txt in txt:
            txt.draw_text()

        # draw input boxes
        for box in input:
            box.draw(DISPLAYSURF)
            box.update()

        wolf_starve_num.draw_num(self.wolves_starved)
        sheep_starve_num.draw_num(self.sheep_starved)
        max_sheep_num.draw_num(self.max_sheep)
        max_wolves_num.draw_num(self.max_wolves)
        sheep_killed_num.draw_num(self.sheep_killed)
        shp_counter.draw_num(self.sheep)
        wolf_counter.draw_num(self.wolves)

    def simulation_pause(self, simulation_grid, txt_boxes, color_boxes, input_boxes, press_button, sheep_num, wolf_num,
                         stop_button, start_button, wolf_starve_num, sheep_starve_num, max_sheep_num, max_wolves_num,
                         sheep_killed_num):
        """
        This function will pause the simulation and not allow anything to manipulate data at this time.
        :param simulation_grid: stored data
        :param txt_boxes: all text boxes
        :param color_boxes: colored text
        :param input_boxes: input boxes
        :param press_button: buttons
        :param sheep_num: number of sheep
        :param wolf_num: number of wolves
        :param wolf_input: wolf input
        :param sheep_input: sheep input
        :param wolf_starve_num: wolves starved
        :param sheep_starve_num: sheep starved
        :param max_sheep_num: max sheep in the simulation
        :param max_wolves_num: max wolves in the simulation
        :param sheep_killed_num: sheep killed in simulation
        :return:
        """
        PAUSE = True

        while PAUSE:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.isOver(mouse_pos):
                        self.simulation_loop(simulation_grid, press_button, txt_boxes, color_boxes, input_boxes,
                                             sheep_num, wolf_num, stop_button, start_button, wolf_starve_num,
                                             sheep_starve_num, max_sheep_num, max_wolves_num, sheep_killed_num)

            DISPLAYSURF.fill((0, 0, 0))
            self.redraw_screen(txt_boxes, color_boxes, input_boxes, press_button, sheep_num, wolf_num, wolf_starve_num,
                               sheep_starve_num, max_sheep_num, max_wolves_num, sheep_killed_num)
            simulation_grid.draw_grid(self.grid, DISPLAYSURF, self.blocksize)
            pygame.display.update()

driver = SimulationDriver()
driver.simulation_setup()
