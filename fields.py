from abc import abstractmethod


class Field:
    __treated: bool = False
    __backtracked: bool = False

    @abstractmethod
    def is_free(self):
        pass

    @abstractmethod
    def get_print_value(self, add_prop):
        pass

    def is_occupied(self):
        return not self.is_free()

    def is_treated(self):
        return self.is_occupied() or self.__treated

    def set_treated(self, treated=True):
        self.__treated = treated

    def is_backtracked(self):
        return self.is_occupied() or self.__backtracked

    def set_backtracked(self, backtracked=True):
        self.__backtracked = backtracked

    def add_prop_to_print(self, input, add=True):
        if not add:
            return input
        if self.is_treated():
            input += 4
        if self.is_backtracked():
            input += 8
        return input


class Wall(Field):

    def is_free(self):
        return False

    def get_print_value(self, add_prop=False):
        return self.add_prop_to_print(0, add_prop)


class Space(Field):
    def is_free(self):
        return True

    def get_print_value(self, add_prop=False):
        return self.add_prop_to_print(1, add_prop)


class Border(Field):
    def is_free(self):
        return False

    def get_print_value(self, add_prop=False):
        return self.add_prop_to_print(2, add_prop)
