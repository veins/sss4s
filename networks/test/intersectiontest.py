import sys
from src.input import check_numbers_valid


class TestIntersection():
    def __init__(self,intersection_x_length, intersection_y_length,lanes, multiple, speed, building):
        self.test_intersection_x_length = intersection_x_length
        self.test_intersection_y_length = intersection_y_length
        self.test_lanes = lanes
        self.test_multiple = multiple
        self.test_building = building
        self.test_speed = speed
        

    

    def multiple_test(self):
        
        self.test_multiple = check_numbers_valid(self.test_multiple)
        
        if self.test_multiple < 0:
            sys.exit("Enter a value above zero for the command -m/--multiple.")
    

    def test_intersection_length(self):

        self.test_intersection_y_length = check_numbers_valid(self.test_intersection_y_length, 'float')
        self.test_intersection_x_length = check_numbers_valid(self.test_intersection_x_length, 'float')

        if self.test_intersection_y_length < 0.1 or self.test_intersection_x_length < 0.1:
            sys.exit("Please enter a number above 0.1 for the length of roads")


    

    def test_lane(self):
    
        self.test_lanes = check_numbers_valid(self.test_lanes)

        if self.test_lanes < 0:
            sys.exit("Please enter a number above zero for -l/--lanes")

        if self.test_lanes > 10:
            sys.exit("Please enter a number between zero and twelve for -l/--lanes.")

    

    def speed_test(self):

        self.test_speed = check_numbers_valid(self.test_speed, 'float')

        if self.test_speed < 0:
            sys.exit("Please enter a value above zero for the command -s/--speed.")


   

    #Calling the test_functions for Grid
    def test_intersection(self):
        self.test_lane()
        self.test_intersection_length()
        self.speed_test()
        self.multiple_test()