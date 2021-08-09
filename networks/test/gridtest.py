import sys
import re 
from collections import Iterable, Mapping
from src.input import check_numbers_valid




class TestGrid():
    def __init__(self, name, grid_x_length, grid_y_length, grid_x_dir, grid_y_dir, lanes,speed, building):
        self.test_grid_x_length = grid_x_length
        self.test_grid_y_length = grid_y_length
        self.test_grid_x_dir = grid_x_dir
        self.test_grid_y_dir = grid_y_dir
        self.test_lanes = lanes
        self.test_building = building
        self.test_speed = speed
        

    def test_grid_size(self):

        self.test_grid_x_dir = check_numbers_valid(self.test_grid_x_dir)
        self.test_grid_y_dir = check_numbers_valid(self.test_grid_y_dir)
        

        if (self.test_grid_x_dir) < 2 or (self.test_grid_y_dir) < 2:
            sys.exit("Please enter a number above two for the number of nodes in vertical and horizontal direction!")

        if self.test_grid_x_dir > 20 or self.test_grid_y_dir >20:
            sys.exit("Too many nodes")


    def test_grid_length(self):

        self.test_grid_y_length = check_numbers_valid(self.test_grid_y_length, 'float')
        self.test_grid_x_length = check_numbers_valid(self.test_grid_x_length, 'float')
        
        if  self.test_grid_y_length < 0.1 or self.test_grid_x_length < 0.1:
            sys.exit("Please for the length of the roads a number above zero.")

    

    def test_lane(self):
        
        
        self.test_lanes = check_numbers_valid(self.test_lanes)

    
        if self.test_lanes < 0:
            sys.exit("Please enter a number above zero for -l/--lanes")

        if self.test_lanes > 10:
            sys.exit("Please enter a number between zero and twelve for -l/--lanes.")

   



    def speed_test(self):

        self.test_speed = check_numbers_valid(self.test_speed, 'float')


        if self.test_speed < 0:
            sys.exit("Please enter a number above zero for the command -s/--speed.")


    #Calling the test_functions for Grid


    def test_grid(self):
        self.test_grid_size()
        self.test_lane()
        self.test_grid_length()
        self.speed_test()
