# Written by Eric Martin for COMP9021


import sys
from random import seed, randint, randrange

try:
    arg_for_seed, upper_bound, length = \
        (int(x) for x in input('Enter three integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()


def length_of_longest_increasing_sequence(L):
    copy_l = L
    record_sequence = []
    if len(L) == 0:
        return 0
    if len(L) == 1:
        return 1
    if len(set(L)) == 1:
        return len(L)
    else:
        if L[0] < L[-1]:
            for i in range(len(L) - 1):
                count_length = 1
                for j in range(i, len(L) -1):
                    if L[j] <= L[j + 1]:
                        count_length += 1
                    else:
                        break
                record_sequence.append(count_length)
        else:
            new_l = L + copy_l
            for i in range(len(new_l) - 1):
                count_length = 1
                for j in range(i, len(new_l) - 1):
                    if new_l[j] <= new_l[j + 1]:
                        count_length += 1
                    else:
                        break
                record_sequence.append(count_length)
        longest_sequence = max(record_sequence)
        return longest_sequence


def max_int_jumping_in(L):
    number_sequence = []
    if len(L) == 0:
        return
    else:
        for ind in range(len(L)):
            member = [L[ind]]
            number_index = []
            number_index.append(ind)
            while L[number_index[-1]] not in number_index:
                number_index.append(L[number_index[-1]])
                member.append(L[number_index[-1]])

            number_sequence.append(int(''.join(str(m) for m in member)))
        return max(number_sequence)


seed(arg_for_seed)
L_1 = [randint(0, upper_bound) for _ in range(length)]
print('L_1 is:', L_1)
print('The length of the longest increasing sequence\n'
      '  of members of L_1, possibly wrapping around, is:',
      length_of_longest_increasing_sequence(L_1), end='.\n\n'
      )
L_2 = [randrange(length) for _ in range(length)]
print('L_2 is:', L_2)
print('The maximum integer built from L_2 by jumping\n'
      '  as directed by its members, from some starting member\n'
      '  and not using any member more than once, is:',
      max_int_jumping_in(L_2)
      )


