# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and determines the size of the largest
# isosceles triangle, consisting of nothing but 1s and whose base can be either
# vertical or horizontal, pointing either left or right or up or down.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import sys
from math import sqrt


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))


def size_of_largest_isosceles_triangle():
    times = []

# initialize grid
    for i in range(10):
        for j in range(10):
            if grid[i][j] != 0 and grid[i][j] != 1:
                grid[i][j] = 1

    for x in range(10):
        for y in range(10):
            if grid[x][y] == 0:
                continue
            if x <= y:
                left = 1
                right = 1
                up = 1
                down = 1
                if x <= 4:
                    for count in range(1, x + 1):
                        for j in range(x - count, x + count + 1):
                            left += grid[j][y - count]
                        if left == (count + 1) ** 2:
                            times.append(left)
                        else:
                            break
                else:
                    for count in range(1, 10 - x):
                        for j in range(x - count, x + count + 1):
                            left += grid[j][y - count]
                        if left == (count + 1) ** 2:
                            times.append(left)
                        else:
                            break
                if x <= 9 - y:
                    for count in range(1, x + 1):
                        for j in range(x - count, x + count + 1):
                            right += grid[j][y + count]
                        if right == (count + 1) ** 2:
                            times.append(right)
                        else:
                            break
                    for count in range(1, x + 1):
                        for j in range(y - count, y + count + 1):
                            up += grid[x - count][j]
                        if up == (count + 1) ** 2:
                            times.append(up)
                        else:
                            break
                else:
                    for count in range(1, 10 - y):
                        for j in range(x - count, x + count + 1):
                            right += grid[j][y + count]
                        if right == (count + 1) ** 2:
                            times.append(right)
                        else:
                            break
                    for count in range(1, 10 - y):
                        for j in range(y - count, y + count + 1):
                            up += grid[x - count][j]
                        if up == (count + 1) ** 2:
                            times.append(up)

                        else:
                            break

                if y <= 4:
                    for count in range(1, y + 1):
                        for j in range(y - count, y + count + 1):
                            down += grid[x + count][j]
                        if down == (count + 1) ** 2:
                            times.append(down)
                        else:
                            break
                else:
                    for count in range(1, 10 - y):
                        for j in range(y - count, y + count + 1):
                            down += grid[x + count][j]
                        if down == (count + 1) ** 2:
                            times.append(down)
                        else:
                            break
            else:
                left = 1
                right = 1
                up = 1
                down = 1
                if x <= 9 - y:
                    for count in range(1, y+1):
                        for j in range(x - count, x + count + 1):
                            left += grid[j][y - count]
                        if left == (count + 1) ** 2:
                            times.append(left)
                        else:
                            break
                    for count in range(1, y + 1):
                        for j in range(y - count, y + count + 1):
                            down += grid[x + count][j]
                        if down == (count + 1) ** 2:
                            times.append(down)
                        else:
                            break
                else:
                    for count in range(1, 10 - x):
                        for j in range(x - count, x + count + 1):
                            left += grid[j][y - count]
                        if left == (count + 1) ** 2:
                            times.append(left)
                        else:
                            break

                    for count in range(1, 10 - x):
                        for j in range(y - count, y + count + 1):
                            down += grid[x + count][j]
                        if down == (count + 1) ** 2:
                            times.append(down)
                        else:
                            break
                if x <= 4:
                    for count in range(1, x + 1):
                        for j in range(x - count, x + count + 1):
                            right += grid[j][y + count]
                        if right == (count + 1) ** 2:
                            times.append(right)
                        else:
                            break
                else:
                    for count in range(1, 10 - x):
                        for j in range(x - count, x + count + 1):
                            right += grid[j][y + count]
                        if right == (count + 1) ** 2:
                            times.append(right)
                        else:
                            break

                if y <= 4:
                    for count in range(1, y + 1):
                        for j in range(y - count, y + count + 1):
                            up += grid[x - count][j]
                        if up == (count + 1) ** 2:
                            times.append(up)
                        else:
                            break
                else:
                    for count in range(1, 10 - y):
                        for j in range(y - count, y + count + 1):
                            up += grid[x - count][j]
                        if up == (count + 1) ** 2:
                            times.append(up)
                        else:
                            break
    if len(times) == 0:
        return 0
    else:
        return int(sqrt(max(times)))


try:
    arg_for_seed, density = (abs(int(x)) for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()
print('The largest isosceles triangle has a size of',
      size_of_largest_isosceles_triangle()
     )
