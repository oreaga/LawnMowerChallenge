#!/usr/bin/python3

from Orientations import Orientations


class Lawnmower:

    def __init__(self, position, orientation):
        if type(position) is tuple:
            self.position = position
        else:
            raise Exception('Position provided for lawnmower is not a tuple')

        if orientation in ['N', 'E', 'S', 'W']:
            if orientation == 'N':
                self.orientation = Orientations.N
            elif orientation == 'E':
                self.orientation = Orientations.E
            elif orientation == 'S':
                self.orientation = Orientations.S
            else:
                self.orientation = Orientations.W
        else:
            raise Exception('Orientation provided to lawnmower is not valid')



