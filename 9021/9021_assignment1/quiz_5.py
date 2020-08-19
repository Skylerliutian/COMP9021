# Prompts the user for a positive integer that codes a set S as follows:
# - Bit 0 codes 0
# - Bit 1 codes -1
# - Bit 2 codes 1
# - Bit 3 codes -2
# - Bit 4 codes 2
# - Bit 5 codes -3
# - Bit 6 codes 3
# ...
# Computes a derived positive integer that codes the set of running sums
# ot the members of S when those are listed in increasing order.
#
# Written by *** and Eric Martin for COMP9021


from itertools import accumulate
import sys

try:
    encoded_set = int(input('Input a positive integer: '))
    if encoded_set < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()


# POSSIBLY DEFINE OTHER FUNCTIONS
def built_compare_set_s(length):
    compare = []
    for i in range(length):
        if i%2 == 0:
            compare.append(int(i / 2))
        else:
            compare.append(int(-(i + 1)/2))
    return compare


def return_encoded_set(encoded_set):
    bin_encoded_set = [int(d) for d in f'{encoded_set:b}']
    bin_encoded_set.reverse()
    length = len(bin_encoded_set)
    list_encoded_set = []
    for i in range(length):
        if bin_encoded_set[i] == 1:
            list_encoded_set.append(built_compare_set_s(length)[i])
    list_encoded_set = sorted(list_encoded_set)
    return list_encoded_set


def display_encoded_set(encoded_set):
    bin_encoded_set = [int(d) for d in f'{encoded_set:b}']
    bin_encoded_set.reverse()
    length = len(bin_encoded_set)
    list_encoded_set = []
    for i in range(length):
        if bin_encoded_set[i] == 1:
            list_encoded_set.append(built_compare_set_s(length)[i])
    list_encoded_set = sorted(list_encoded_set)
    if len(list_encoded_set) == 0:
        print('{}')
    else:
        print('{',end='')
        for i in range(len(list_encoded_set)-1):
            print(list_encoded_set[i], end=', ')
        print(list_encoded_set[-1],'}',sep='')


def code_derived_set(encoded_set):
    encoded_running_sum = 0
    positive = 0
    negative = 0
    first_set = return_encoded_set(encoded_set)
    derived_set = list(set(accumulate(first_set)))
    for i in range(len(derived_set)):
        if derived_set[i] < 0:
            encoded_running_sum += 2 ** ((2 * -(derived_set[i])) - 1)
        else:
            encoded_running_sum += 2 ** (2 * derived_set[i])
    return encoded_running_sum


print('The encoded set is: ', end='')
display_encoded_set(encoded_set)
encoded_running_sum = code_derived_set(encoded_set)
print('The derived encoded set is: ', end='')
display_encoded_set(encoded_running_sum)
print('  It is encoded by:', encoded_running_sum)
