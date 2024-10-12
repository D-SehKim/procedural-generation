'''
Daniel Kim
CS 021 Fall 2022 Final Project
Island Procedural Generation Program
This program will take a set of rules which they can modify in order to
procedurally generate colors on a 100x100 grid. They will be random shapes, and once they're all generated,
they will be filled, then the outide will be made into an ocean.

throughout the program, the term "rectangle" is used broadly to also represent
squares
'''

# importing pygame and random
# pygame for the Visual Aspect
# Random for "procedural generation"
import pygame
import random

# by making all these variables global, all functions can use them w/o having
# return statements

# make a surface to display, (can increase/decrease size later)
height_of_display = 530
width_of_display = 530
DISPLAY = pygame.display.set_mode((width_of_display, height_of_display))

# defining constants and colors for pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

AQUATIC_BLUE = (2, 159, 250)
DESERT_YELLOW = (249, 255, 66)
FOREST_GREEN = (38, 110, 62)
PLAINS_GREEN = (77, 240, 88)
TUNDRA_GREY = (196, 196, 185)

# parameters for the larger outlining square,
# (able to increase/decrease it later) 
x_coord_of_outline_rect = 14
y_coord_of_outline_rect = 14

height_of_outline_rect = 501
width_of_outline_rect = 501

OUTLINE_RECT = (x_coord_of_outline_rect, y_coord_of_outline_rect, width_of_outline_rect, height_of_outline_rect)


def main():
    '''
    main function, all functions are called and used in here
    '''

    # initalizing and making background
    initialize_and_background()
    rectangle_index, edge_rectangle = create_dictionaries()


    # in-case the user wishes to continue making islands
    y_or_n = "y"    
    while y_or_n == "y" or y_or_n == "Y":

        # display the title first
        display_title()

        # then make the squares surrounding the land into oceans
        make_graph_squares(AQUATIC_BLUE)

        # ask for user input on topic
        amount_of_deserts = input("\nHow prevelant should deserts be? \n(0 is non-existant)\n(10 being the min amount & 25 being the max amount of desert)\n>>>")
        # validate the user input
        while amount_of_deserts not in ["0", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"]:
            amount_of_deserts = input("\nPLEASE USE CORRECT INPUT\nHow prevelant should deserts be? \n(0 is non-existant)\n(10 being the min amount & 25 being the max amount of desert?)\n>>>")
        # after validation, start rendering
        math_for_shapes(15, DESERT_YELLOW, int(amount_of_deserts))

        # ask for user input on topic
        amount_of_tundras = input("\nHow prevelant should tundra be? \n(0 is non-existant)\n(9 being the min amount & 13 being the max amount of tundra)\n>>>")
        # validate the user input
        while amount_of_tundras not in ["0", "9", "10", "11", "12", "13"]:
            amount_of_tundras = input("\nPLEASE USE CORRECT INPUT\nHow prevelant should tundra be? \n(0 is non-existant)\n(9 being the min amount & 13 being the max amount of tundra?)\n>>>")
        # after validation, start rendering
        math_for_shapes(15, TUNDRA_GREY, int(amount_of_tundras))

        # ask for user input on topic               
        amount_of_plains = input("\nHow prevelant should plains be? \n(0 is non-existant)\n(6 being the min amount & 9 being the max amount of plains)\n>>>")
        # validate the user input
        while amount_of_plains not in ["0", "6", "7", "8", "9"]:
            amount_of_plains = input("\nPLEASE USE CORRECT INPUT\nHow prevelant should plains be? \n(0 is non-existant)\n(6 being the min amount & 9 being the max amount of plains)\n>>>")
        # after validation, start rendering
        math_for_shapes(15, PLAINS_GREEN, int(amount_of_plains))

        # ask for user input on topic
        amount_of_forests = input("\nHow prevelant should forests be? \n(0 is non-existant)\n(3 being the min amount & 6 being the max amount of forests)\n>>>")
        # validate the user input
        while amount_of_forests not in ["0", "3", "4", "5", "6"]:
            amount_of_forests = input("\nPLEASE USE CORRECT INPUT\nHow prevelant should forests be? \n(0 is non-existant)\n(3 being the min amount & 6 being the max amount of forests)\n>>>")
        # after validation, start rendering
        math_for_shapes(15, FOREST_GREEN, int(amount_of_forests))

        # keeping the user updated
        print("\n\nPlease wait, we are now generating your island...")

        # update the pygame screen once fully rendered
        pygame.display.flip()

        # user updated
        print("\n\nYour island has been generated!!\nEnjoy it!")

        # asking user if they want to restart, if n, no, if y, yes
        y_or_n = input("Would you like to generate another island? (enter 'y' or 'n')\n>>>")
        # validate the input
        while y_or_n not in ["y", "Y", "n", "N"]:
             y_or_n = input("\nINPUT WAS NOT CORRECT\nWould you like to generate another island?\n>>>")
    # if n, exit loop, say thanks, also quits pygame
    print("\nThank you for using Procedural Island Generator")
    pygame.quit()

    
def display_title():
    '''
    This function will display the title and instructions for user input
    '''
    print(f"\n\n---------------------------\n"
          f"Island Proceudral Generator\n"
          f"---------------------------")
    print(f"Welcome to your own Proceudral Island Generator, you can use\n"
          f"this to generate islands with different biomes! (It even includes lakes)\n"
          f"Obviously, as an island it will be surrounded by oceans!\n"
          f"Please input a integer, the larger the integer,\n"
          f"the higher the chance that, the biome with\n"
          f"the large integer will be more prevelant on the island.\n"
          f"In other words, higher integer = higher chance that the biome will be large\n\n"
          f"Procedural Generation is random, so there are no promises!\n"
          f"If you dislike the island generated, you can also create a new one!")
          


def create_dictionaries():
    '''
    defining dictionaries for position of every
    rectangle/directions and what to do with each direction/
    the edge rectangles
    returns a dictionary with the position of every rectangle
    returns the dictionary of direction and what to do with each direction
    returns a list of all the rectanges on the edge
    '''
    try:
        # empty rectangle dictionary
        rectangle_index = {}

        # setting up variables for the first rectangle
        pos_of_rect_left = 15
        pos_of_rect_top = 15
        amount_between_rectangles = 5

        # the current rectangle (starts at 1)
        current_rect_index = 1

        # looping through all 10000 rectangles and assigning it a number as a key, along with its (x,y) coords as it's value
        for num in range(100):
            # this will loop thorugh horizontially
            for num in range(100):
                # adding every rectangle on the x-axis
                rectangle_index[f"rect_{current_rect_index}"] = (pos_of_rect_left, pos_of_rect_top)
                pos_of_rect_left = pos_of_rect_left + amount_between_rectangles
                current_rect_index = current_rect_index + 1

            # jump down one row, then reset back to the first rectangle column
            pos_of_rect_left = 15
            pos_of_rect_top = pos_of_rect_top + amount_between_rectangles

            
        # empty list of all rectangle index/keys that are on the edge
        edge_rectangle = []

        # if x or y = 15 or 510, then it is an edge rectangle
        for num in range(len(rectangle_index)):
            # loops through all the rectangles in recangle_index, if the x or y = 15 or 510, then add it
            if rectangle_index[f"rect_{num + 1}"][0] == 15 or rectangle_index[f"rect_{num + 1}"][0] == 510 or rectangle_index[f"rect_{num + 1}"][1] == 15 or rectangle_index[f"rect_{num + 1}"][1] == 510:
                   edge_rectangle.append(f"rect_{num + 1}")

        # return the dictionary of all rectangles, and list of edge rectangles
        return rectangle_index, edge_rectangle
    
    except Exception as error:
        print(error)
    
def initialize_and_background():
    '''
    this will initalize pygame and make a background display
    '''
    try:
        # initialize pygame
        pygame.init()

        # making the display white
        DISPLAY.fill(WHITE)

        #draw the outline rectangle
        pygame.draw.rect(DISPLAY, BLACK, OUTLINE_RECT)

    except:
        print("error making background/initalizing")


def make_graph_squares(color):
    '''
    this will make the graph filled with color squares given in the parameter
    '''
    try:        
        # defining the variables for the inner (smaller) rectangles
        pos_of_rect_left = 15
        pos_of_rect_top = 15
        rect_width = 4
        rect_len = 4

        # the amount of space between each "rectangle"
        amount_between_rectangles = 5
        # nested loops to make a 100x100 graph
        for num in range(0, 100):
            # first loop is for horizontal, then moves down one vertical, resets back to square one and goes down horizontal again
            for num in range(0, 100):
                # drawing the smaller rectangles with variables defined earlier
                pygame.draw.rect(DISPLAY, color, (pos_of_rect_left, pos_of_rect_top, rect_width, rect_len))
                # move down the horizontal
                pos_of_rect_left = pos_of_rect_left + amount_between_rectangles
            # reseting the left position back to square one
            pos_of_rect_left = 15
            # moving down vertiacally
            pos_of_rect_top = pos_of_rect_top + amount_between_rectangles

    except Exception as error:
        print(error)


def math_for_shapes(size_limit, color, total_areas):
    try:
        '''
        given the paramters of size_limit (the size_limit of each side length), color (the biome color) and, total_areas (the
        amount of areas the user wants generated)
        The program will procedurally generate the desired biome, along with its color
        '''
        # creating dictionaries within the function as they are not global
        rectangle_index, edge_rectangle = create_dictionaries()

        # creating the width and height of rectangles
        rectangle_width = 4
        rectanlge_height = 4

        # based on user input of how many areas of that biome to create, we will loop the creating process that many times
        for num in range(0, total_areas):
            # the starting point is a random rectangle along the edge
            start_rectangle = f"rect_{random.randint(0, 10000)}"
            
            # creates the coordinates for the starting rectange, and stores that rectangle_index key
            rectangle_coords = rectangle_index[start_rectangle]
            rectangle_index_key = start_rectangle
            
            # finding which direction we are going
            which_direction = random.randint(1, 4) # 4 for the 4 directions possible

            value_of_direction = " "

            # drawing the first rectange, before the loop changes anything
            pygame.draw.rect(DISPLAY, color, (rectangle_coords[0], rectangle_coords[1], rectangle_width, rectanlge_height))

            # create edge detection and start the loop
            is_on_edge = False 
            while is_on_edge == False:
                
                # based on random number, choose which way to go
                if which_direction == 1:
                    value_of_direction = 1 # east
                elif which_direction == 2:
                    value_of_direction = -1 # west
                elif which_direction == 3:
                    value_of_direction = 100 # north
                elif which_direction == 4:
                    value_of_direction = -100 # south

                # the "number" of the rectangle_index_key rectangle
                rect_number = int(rectangle_index_key[5:])

                # if the number is not in the grid, then redo which direction you move
                if rect_number + value_of_direction < 1 or rect_number + value_of_direction > 10000:
                    which_direction = random.randint(1, 4)
                    
                # if the value exists, we commence movement
                else:
                    # we move a random number of spaces given by a size limit, that way, its not just 1x1 movements
                    for num in range(0, random.randint(1, size_limit)):

                        # find the coords of the new rectangle
                        rectangle_coords = rectangle_index[f"rect_{rect_number + value_of_direction}"]
                        # find the index of the new rectangle
                        rectangle_index_key = f"rect_{rect_number + value_of_direction}"

                        # then we draw the rectangle at the new values
                        pygame.draw.rect(DISPLAY, color, (rectangle_coords[0], rectangle_coords[1], rectangle_width, rectanlge_height))
                       
                    # reset the direction of movement
                    which_direction = random.randint(1, 4)
                # after everything, edge detection, if there is an edge, exit the loop.  
                if rectangle_index_key in edge_rectangle:
                    is_on_edge = True

    except Exception as error:
        print(error)

    
if __name__ == "__main__":
    main()
