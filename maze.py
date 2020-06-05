from datetime import datetime

from direction import Direction
from fields import Space, Wall, Border, Field
import numpy as np
import matplotlib.pyplot as plt
from position import Position
import progressbar
import png

class Maze:

    def __init__(self, size, size_col=None):
        self.size = size
        if size_col is not None:
            self.size_col = size_col
        else:
            self.size_col = self.size

        self.dim_row = self.size * 2 + 3
        self.dim_col = self.size_col * 2 + 3
        self.cells = self.size * self.size
        self.bar = progressbar.ProgressBar(maxval=self.cells,
                                           widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        self.bar.start()
        self.maze = self.build_maze()
        self.bar.finish()

    def build_maze(self):
        self.maze = self.__init_with_space()
        self.maze = self.__insert_walls()
        self.maze = self.__insert_borders()
        self.maze = self.__insert_paths()
        return self.maze

    def __init_with_space(self):
        maze = []

        # fill with space
        for row in range(self.dim_row):
            maze.append([])
            for col in range(self.dim_col):
                maze[row].append(Space())
        return maze

    def __insert_walls(self,):
        # insert walls
        for row in range(3, self.dim_row - 2, 2):
            for col in range(2, self.dim_col - 2, 1):
                self.maze[row][col] = Wall()
                self.maze[col][row] = Wall()
        return self.maze

    def __insert_borders(self):
        for i in range(self.dim_row):
            self.maze[i][0] = Border()
            self.maze[i][1] = Border()
            self.maze[i][self.dim_col - 2] = Border()
            self.maze[i][self.dim_col - 1] = Border()

        for j in range(self.dim_col):
            self.maze[0][j] = Border()
            self.maze[1][j] = Border()
            self.maze[self.dim_row - 2][j] = Border()
            self.maze[self.dim_row - 1][j] = Border()

        return self.maze

    def __insert_paths(self):

        treated_cells = 1
        pos = Position(2, 2)
        self.__set_treated(pos)
        while treated_cells < self.cells:
            self.bar.update(treated_cells)
            # print('Pos: {} {}'.format(pos.col, pos.row))
            # self.show()
            while self.__in_dead_end(pos):
                # self.show()
                pos = self.__step_back(pos)
                # print('Stepping back to {} {}'.format(pos.col, pos.row))
            dir = Direction()

            if not self.__behind_wall_is_treated(pos, dir):
                pos.change(dir)
                self.__break_wall(pos)
                pos.change(dir)
                self.__set_treated(pos)
                treated_cells += 1
        return self.maze

    def __set_field(self, position: Position, field: Field):
        self.maze[position.row][position.col] = field

    def __get_field(self, position) -> Field:
        return self.maze[position.row][position.col]

    def __set_treated(self, position: Position):
        self.maze[position.row][position.col].set_treated()

    def get_as_image(self, bw=True):
        img = []
        for row in range(self.dim_row):
            img.append([])
            for col in range(self.dim_col):
                img[row].append(self.maze[row][col].get_print_value(add_prop=not bw))
        img = np.asarray(img)
        img[img == 2] = 0
        return img.astype(float)

    def show(self, bw=True):
        plt.close('all')
        plt.imshow(self.get_as_image(bw=bw))
        plt.show()

    def __break_wall(self, pos):
        self.__set_field(pos, Space())
        self.__set_treated(pos)

    def __behind_wall_is_treated(self, pos, dir):
        check_pos = Position(col=pos.col, row=pos.row, direction=dir)
        check_pos.change(dir)
        return self.__get_field(check_pos).is_treated()

    def __in_dead_end(self, pos):
        end = True
        for dir in range(4):
            # check all four directions
            if not self.__behind_wall_is_treated(pos, Direction(dir)):
                end = False
                break
        return end

    def __step_back(self, pos: Position):
        self.__get_field(pos).set_backtracked()
        new_pos = Position(col=pos.col, row=pos.row)
        for diri in range(4):
            dir = Direction(diri)
            new_pos = Position(col=pos.col, row=pos.row, direction=dir)
            step_field = self.__get_field(new_pos)
            if step_field.is_free() and not step_field.is_backtracked():
                # self.__get_field(new_pos).set_backtracked()
                break
            # new_pos = Position(col=pos.col, row=pos.row)
        if new_pos == pos:
            raise Exception("Stuck")
        return new_pos

    def export_pdf(self):
        self.get_as_image()

    def export_png(self, path=None):
        if path is None:
            path = 'maze_{}_{}.png'.format(self.size, str(datetime.now().isoformat()))
            path = path.replace(':', '-')
        img = self.get_as_image()
        img[img > 0] = 255
        png.from_array(img.astype(np.uint8), mode='L').save(path)



