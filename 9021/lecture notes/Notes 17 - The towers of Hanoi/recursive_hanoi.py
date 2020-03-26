# Written by Eric Martin for COMP9021


'''
Recursive solution to the Tower of Hanoi puzzle.
'''


def move_towers(n, start_position, end_position, intermediate_position):
    '''
    Move a tower of n disks from start_position to end_position,
    with intermediate_position available.

    >>> move_towers(4, 0, 2, 1)
    Move smallest disk from position 0 to position 1
    Move disk of size 2 from position 0 to position 2
    Move smallest disk from position 1 to position 2
    Move disk of size 3 from position 0 to position 1
    Move smallest disk from position 2 to position 0
    Move disk of size 2 from position 2 to position 1
    Move smallest disk from position 0 to position 1
    Move disk of size 4 from position 0 to position 2
    Move smallest disk from position 1 to position 2
    Move disk of size 2 from position 1 to position 0
    Move smallest disk from position 2 to position 0
    Move disk of size 3 from position 1 to position 2
    Move smallest disk from position 0 to position 1
    Move disk of size 2 from position 0 to position 2
    Move smallest disk from position 1 to position 2
    '''
    if n == 1:
        print(f'Move smallest disk from position {start_position} '
              f'to position {end_position}'
              )
    else:
        move_towers(n - 1, start_position, intermediate_position, end_position)
        print(f'Move disk of size {n} from position {start_position} '
              f'to position {end_position}'
              )
        move_towers(n - 1, intermediate_position, end_position, start_position)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
