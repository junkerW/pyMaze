from random import randrange


class Direction:

    SOUTH = 0
    EAST = 1
    WEST = 2
    NORTH = 3

    str_switch = {0: 'South', 1: 'East', 2: 'West', 3: 'North'}

    def __init__(self, direction: int=None):
        if direction is not None:
            self.__direction = direction
        else:
            self.__direction = self.__get_random_direction_number()

    def __get_random_direction_number(self):
        return randrange(0, 4)

    def get_direction(self):
        return self.__direction

    def __str__(self):
        return Direction.str_switch[self.get_direction()]