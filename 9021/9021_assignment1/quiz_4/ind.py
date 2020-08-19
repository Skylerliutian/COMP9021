import sys
from random import seed, randint, randrange
import quiz4 as q4
from pathlib import Path


if __name__ == '__main__':
    import doctest
    print('test start.....')
    with open(Path('indicator.txt')) as f:
        line_list = f.readlines()
        for line in line_list:
            print(line)
            q4.main2(line.strip())


    #doctest.testmod()
    print('Test Done! If not show "Test Failed", you pass all my test')