#!/bin/usr/python3

from Lawnmower import Lawnmower
from Orientations import Orientations
import sys


# Class for controlling mowers on a rectangular grid
class MowerController:

    def __init__(self, size, instructions):
        self.occupied_spaces = set()
        self.lawnmowers = []
        self.size = (int(size[0]), int(size[1]))
        self.instructions = instructions

        # Go through and initialize the lawnmowers on the grid
        for line in instructions:
            words = line.split()

            # If the line indicates a mower starting position, place it if possible
            if len(words) == 3:
                words[0] = int(words[0])
                words[1] = int(words[1])
                if words[0] > self.size[0] or words[1] > self.size[1] or words[0] < 0 or words[1] < 0:
                    raise Exception('Mower placement outside grid')
                else:
                    start_position = (words[0], words[1])

                    # Place the mower if its starting position is not occupied
                    if start_position not in self.occupied_spaces:
                        self.occupied_spaces.add(start_position)
                        self.lawnmowers.append(Lawnmower((words[0], words[1]), words[2]))
                    else:
                        raise Exception('Two lawnmowers share a starting location')

    # Method for processing lawnmower instructions
    def move_lawnmowers(self):

        for i in range(0, len(self.instructions)):
            words = self.instructions[i].split()
            if len(words) == 3:
                lawnmower = self.lawnmowers[int(i/2)]
                words[0] = int(words[0])
                words[1] = int(words[1])

                # Ensure that the instruction is being processed for the correct lawnmower
                if lawnmower.position != (words[0], words[1]):
                    raise Exception('Processing instructions for incorrect lawnmower')

                # Execute instructions and calculate ending position/collisions
                self.process_instruction(lawnmower, self.instructions[i + 1])

    def process_instruction(self, lawnmower, instruction):

        # Execute instruction list for the given lawnmower
        for ch in instruction:
            if ch == 'L':
                lawnmower.orientation = (lawnmower.orientation - 1) % 4
            elif ch == 'R':
                lawnmower.orientation = (lawnmower.orientation + 1) % 4
            elif ch == 'F':
                self.occupied_spaces.remove(lawnmower.position)

                if lawnmower.orientation == Orientations.N:
                    lawnmower.position = self.calc_new_position(lawnmower.position, (0, 1))
                elif lawnmower.orientation == Orientations.E:
                    lawnmower.position = self.calc_new_position(lawnmower.position, (1, 0))
                elif lawnmower.orientation == Orientations.S:
                    lawnmower.position = self.calc_new_position(lawnmower.position, (0, -1))
                else:
                    lawnmower.position = self.calc_new_position(lawnmower.position, (-1, 0))

                self.occupied_spaces.add(lawnmower.position)

        print('{} {} {}'.format(lawnmower.position[0], lawnmower.position[1], Orientations(lawnmower.orientation).name))

    def calc_new_position(self, curr_position, move):
        new_position = (curr_position[0] + move[0], curr_position[1] + move[1])

        if new_position[0] > self.size[0] or new_position[1] > self.size[1] or \
           new_position[0] < 0 or new_position[1] < 0:
            new_position = curr_position
        else:
            if new_position in self.occupied_spaces:
                raise Exception('Mower collision')

        return new_position


if __name__ == '__main__':
    try:
        with open(sys.argv[1], 'r') as fd:
            doc_contents = fd.readlines()
    except FileNotFoundError:
        print('Instruction file not found')

    grid_size = tuple(doc_contents[0].split())
    mower_instructions = doc_contents[1:]
    mower_controller = MowerController(grid_size, mower_instructions)
    mower_controller.move_lawnmowers()


