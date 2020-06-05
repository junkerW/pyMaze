from direction import Direction


class Position:

    __direction_switch = {}

    def __init__(self, col, row, direction: Direction=None):
        self.col = col
        self.row = row
        if direction is not None:
            self.change(direction)

    def change(self, dir:Direction):
        if dir.get_direction() == Direction.SOUTH:
            self.row += 1
        elif dir.get_direction() == Direction.EAST:
            self.col += 1
        elif dir.get_direction() == Direction.NORTH:
            self.row -= 1
        elif dir.get_direction() == Direction.WEST:
            self.col -= 1
        return self

    def __str__(self):
        return "Col: {}, Row: {}".format(self.col, self.row)