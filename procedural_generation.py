'''
Daniel Kim
CS 021 Fall 2022 Final Project
Procedural Generation Program
This program will take a set of rules which they can modify in order to
procedurally generate colors on a 100x100 grid. They will be random shapes, and once they're all generated,
they will be filled, then the outide will be made into an ocean.  
'''

# source: https://betterprogramming.pub/making-grids-in-python-7cf62c95f413\
# source: https://www.google.com/search?q=rgb+color+picker&rlz=1C5CHFA_enUS891US891&oq=rgb+color+&aqs=chrome.1.69i57j69i59j46i433i512j69i60l5.3915j0j7&sourceid=chrome&ie=UTF-8
# source: https://www.geeksforgeeks.org/pygame-surface/

# pygame documentation: https://www.pygame.org/docs/

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
    initialize_and_background()
    rectangle_index, edge_rectangle = create_dictionaries()
    
    make_graph_squares(WHITE)
    for num in range(0, 7):
        water_rects = math_for_shapes(1000, AQUATIC_BLUE)
        desert_rects = math_for_shapes(1000, DESERT_YELLOW)
        forest_rects = math_for_shapes(1000, FOREST_GREEN)
        plains_rects = math_for_shapes(1000, PLAINS_GREEN)
        tundra_rects = math_for_shapes(1000, TUNDRA_GREY)
        print("one done")


    pygame.display.flip()
    # MAKE A CHECK TO SEE IF THERE ALREADY IS A COLOR THERE.
    # MAKE IT START CLOSE TO MIDDLE


def create_dictionaries():
    '''
    defining dictionaries for position of every
    rectangle/directions and what to do with each direction/
    the edge rectangles
    returns a dictionary with the position of every rectangle
    returns the dictionary of direction and what to do with each direction
    returns a list of all the rectanges on the edge
    '''
    
    rectangle_index = {}

    pos_of_rect_left = 15
    pos_of_rect_top = 15
    amount_between_rectangles = 5

    current_rect_index = 1

    for num in range(100):
        for num in range(100):
            rectangle_index[f"rect_{current_rect_index}"] = (pos_of_rect_left, pos_of_rect_top)
            pos_of_rect_left = pos_of_rect_left + amount_between_rectangles
            current_rect_index = current_rect_index + 1

        pos_of_rect_left = 15
        pos_of_rect_top = pos_of_rect_top + amount_between_rectangles

    edge_rectangle = []

    for num in range(len(rectangle_index)):
        if rectangle_index[f"rect_{num + 1}"][0] == 15 or rectangle_index[f"rect_{num + 1}"][0] == 510 or rectangle_index[f"rect_{num + 1}"][1] == 15 or rectangle_index[f"rect_{num + 1}"][1] == 510:
               edge_rectangle.append(f"rect_{num + 1}")

    return rectangle_index, edge_rectangle

    
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
        # make a loop to make a 100x100 graph
        
        # defining the variables for the inner (smaller) squares
        pos_of_rect_left = 15
        pos_of_rect_top = 15
        rect_width = 4
        rect_len = 4
        amount_between_rectangles = 5
        # nested loops to make a 100x100 graph
        for num in range(0, 100):
            for num in range(0, 100):
                pygame.draw.rect(DISPLAY, color, (pos_of_rect_left, pos_of_rect_top, rect_width, rect_len))
                pos_of_rect_left = pos_of_rect_left + amount_between_rectangles
            # reseting the variable back to restart creating graph
            pos_of_rect_left = 15
            pos_of_rect_top = pos_of_rect_top + amount_between_rectangles

    except Exception as error:
        print(error)



def math_for_shapes(size_limit, color):
    try:
        rectangle_index, edge_rectangle = create_dictionaries()
        certain_color_list = []

        # the starting point is a random rectangle along the edge
        start_rectangle = f"rect_{random.randint(0, 10000)}"
        
        # creates the coordinates for the starting rectange, and stores that rectangle_index key
        rectangle_coords = rectangle_index[start_rectangle]
        rectangle_index_key = start_rectangle
        
        # finding which direction we are going
        which_direction = random.randint(1, 4)
        go_this_way = " "

        # drawing the first rectange, before the loop changes anything
        pygame.draw.rect(DISPLAY, color, (rectangle_coords[0], rectangle_coords[1], 4, 4))

        # create edge detection and start the loop
        is_on_edge = False 
        while is_on_edge == False:
            
            # based on random number, choose which way to go
            if which_direction == 1:
                go_this_way = 1 # east
            elif which_direction == 2:
                go_this_way = -1 # west
            elif which_direction == 3:
                go_this_way = 100 # north
            elif which_direction == 4:
                go_this_way = -100 # south

            # the "number" of the rectangle_index_key rectangle
            rect_number = int(rectangle_index_key[5:])

            # if the number is not in the grid, then redo which direction you move
            if rect_number + go_this_way < 1 or rect_number + go_this_way > 10000:
                which_direction = random.randint(1, 4)

            # otherwise, we commence movement
            else:
                # we move a random number of spaces given by a size limit
                for num in range(0, random.randint(1, size_limit)):
                    
                    rectangle_coords = rectangle_index[f"rect_{rect_number + go_this_way}"]
                    
                    rectangle_index_key = f"rect_{rect_number + go_this_way}"

                    # if we go north or south
                    if go_this_way > 2 or go_this_way < -2:
                        pygame.draw.rect(DISPLAY, color, (rectangle_coords[0], rectangle_coords[1], 4, 4))
                    else:
                        pygame.draw.rect(DISPLAY, color, (rectangle_coords[0], rectangle_coords[1], 4, 4))

                certain_color_list.append(rectangle_index_key)
                which_direction = random.randint(1, 4)

            if rectangle_index_key in edge_rectangle:
                is_on_edge = True

        return certain_color_list
                
    except Exception as error:
        print(error)
        


def tundra():
    print("tundra")

def desert():
    print("desert")

def plains():
    print("plains")

def forest():
    print("forest")

def aqua():
    print("aqua")



def fill_with_random_colors():
    '''
    just a test function to fill the graph with random colors
    '''
    try:
        # make a loop to make a 100x100 graph
        # defining the variables for the inner squares
        pos_of_rect_left = 15
        pos_of_rect_top = 15
        rect_width = 4
        rect_len = 4
        amount_between_rectangles = 5
        
        # nested loops to make a 100x100 graph
        for num in range(0, 100):            
            for num in range(0, 100):
                r_value = random.randint(0, 255)
                g_value = random.randint(0, 255)
                b_value = random.randint(0, 255)
                color = (r_value, g_value, b_value)
                
                pygame.draw.rect(DISPLAY, color, (pos_of_rect_left, pos_of_rect_top, rect_width, rect_len))
                pos_of_rect_left = pos_of_rect_left + amount_between_rectangles
            # reseting the variable back to restart creating graph
            pos_of_rect_left = 15
            pos_of_rect_top = pos_of_rect_top + amount_between_rectangles

        # updating the window 
        pygame.display.flip()
    except:
        print("error with random colors")

    
if __name__ == "__main__":
    main()
