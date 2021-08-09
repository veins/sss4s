import sys
from src import input

class TestFreeway():
    def __init__(self,lanes, length, speed):
        self.test_lanes = lanes
        self.test_length = length
        self.test_speed = speed


    
    def test_freeway_length(self):
        
        self.test_length = input.check_numbers_valid(self.test_length, 'float')

        try:
            c = float(self.test_length)
        except:
            sys.exit("Please enter numbers for the command -len/--length.")

        if c < 0.1:
            sys.exit("Please for the length of the roads a number above zero.")

    



    def test_lane(self):
    
        self.test_lanes =  input.check_numbers_valid(self.test_lanes)
        
        if self.test_lanes < 0:
            sys.exit("Please enter a number above zero for -l/--lanes")

        if self.test_lanes > 8:
            sys.exit("Please enter a number between zero and ten for -l/--lanes.")

    


    def speed_test(self):

        self.test_speed = input.check_numbers_valid(self.test_speed, 'float')

        if self.test_speed < 0:
            sys.exit("Please enter a value above zero for the command -s/--speed.")


    def test_freeway(self):
        self.test_freeway_length()
        self.test_lane()
        self.speed_test()

