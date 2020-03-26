# Randomly fills a grid with True and False, with width, height and density
# controlled by user input, and computes the number of all "good paths" that link
# a point of coordinates (x1, y1) to a point of coordinates (x2, y2)
# (x1 and x2 are horizontal coordinates, increasing from left to right,
# y1 and y2 are vertical coordinates, increasing from top to bottom,
# both starting from 0), that is:
# - paths that go through nothing but True values in the grid
# - paths that never go through a given point in the grid more than once;
# - paths that never keep the same direction (North, South, East, West) over
#   a distance greater than 2.
#
# Written by *** and Eric Martin for COMP9021


from collections import namedtuple
import numpy as np
from random import seed, randrange
import sys


Point = namedtuple('Point', 'x y')


def display_grid():
    for row in grid:
        print('   ', ' '.join(str(int(e)) for e in row))


def valid(pt):
    return 0 <= pt.x < width and 0 <= pt.y < height


# in order to record searched points
already_search = []


def trace_direction(pt_1, pt_2, count_up=0, count_down=0, count_right=0, count_left=0, nb_of_sol=0):

    # start and end point must be true
    if grid[pt_2.y][pt_2.x]:
        if grid[pt_1.y][pt_1.x]:

            # already_search.append(pt_1)
            if pt_1.x == pt_2.x and pt_1.y == pt_2.y:
                nb_of_sol += 1
            else:

                # record this point first
                already_search.append(pt_1)

                # go up
                if 0 < pt_1.y < height:
                    new_pt_1 = Point(pt_1.x, pt_1.y - 1)
                    if new_pt_1 not in already_search and count_up < 2:
                        already_search.append(new_pt_1)
                        nb_of_sol = trace_direction(new_pt_1, pt_2, count_up + 1, 0, 0, 0, nb_of_sol)
                        already_search.remove(new_pt_1)

                # go down
                if 0 <= pt_1.y < height - 1:
                    new_pt_1 = Point(pt_1.x, pt_1.y + 1)
                    if new_pt_1 not in already_search and count_down < 2:
                        already_search.append(new_pt_1)
                        nb_of_sol = trace_direction(new_pt_1, pt_2, 0, count_down + 1, 0 , 0, nb_of_sol)
                        already_search.remove(new_pt_1)

                # go left
                if 0 < pt_1.x < width:
                    new_pt_1 = Point(pt_1.x - 1, pt_1.y)
                    if new_pt_1 not in already_search and count_left < 2:
                        already_search.append(new_pt_1)
                        nb_of_sol = trace_direction(new_pt_1, pt_2, 0, 0, 0, count_left + 1, nb_of_sol)
                        already_search.remove(new_pt_1)

                # go right
                if 0 <= pt_1.x < width - 1:
                    new_pt_1 = Point(pt_1.x + 1, pt_1.y)
                    if new_pt_1 not in already_search and count_right < 2:
                        already_search.append(new_pt_1)
                        nb_of_sol = trace_direction(new_pt_1, pt_2, 0, 0, count_right + 1, 0, nb_of_sol)
                        already_search.remove(new_pt_1)

                # remove this point in order to reset the already_search list, if failed
                already_search.remove(pt_1)

    return nb_of_sol


def nb_of_good_paths(pt_1, pt_2):
    sol_nb = trace_direction(pt_1, pt_2)
    return sol_nb


try:
    for_seed, density, height, width = (abs(int(i)) for i in
                                                  input('Enter four integers: ').split()
                                       )
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
if not density:
    density = 1
seed(for_seed)
grid = np.array([randrange(density) > 0
                              for _ in range(height * width)
                ]
               ).reshape((height, width))
print('Here is the grid that has been generated:')
display_grid()

try:
    i1, j1, i2, j2 = (int(i) for i in input('Enter four integers: ').split())
    pt_1 = Point(i1, j1)
    pt_2 = Point(i2, j2)
    if not valid(pt_1) or not valid(pt_2):
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
print('Will compute the number of good paths '
      f'from ({pt_1.x}, {pt_1.y}) to ({pt_2.x}, {pt_2.y})...'
     )

paths_nb = nb_of_good_paths(pt_1, pt_2)


if not paths_nb:
    print('There is no good path.')
elif paths_nb == 1:
    print('There is a unique good path.')
else:
    print('There are', paths_nb, 'good paths.')






