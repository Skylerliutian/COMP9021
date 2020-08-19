# Finds all triples of consecutive positive three-digit integers
# each of which is the sum of two squares.


# Insert you code here# Finds all triples of consecutive positive three-digit integers
# each of which is the sum of two squares.
from math import sqrt


def nb_of_consecutive_squares(n):
    if sums_of_two_squares[n] is not None and sums_of_two_squares[n + 1] is not None and sums_of_two_squares[n + 2] is not None:
        return 1


# The largest number whose square is a 3-digit number.
max = 31
# For all n in [100, 999], if n is found to be of the form a^2 + b^2
# then sums_of_two_squares[n] will be set to (a, b).
# Note that there might be other decompositions of n into a sum of 2 squares;
# we just recall the first decomposition we find.
# Also note that we waste the 100 first elements of the array;
# we can afford it and this choice makes the program simpler.
sums_of_two_squares = [None] * 1_000

# Insert your code here so that sums_of_two_squares[n] = (a, b) for some a, b with a^2 + b^2 == n
# in case such a pair (a, b) indeed exists.
for p_1 in range(max + 1):
    for p_2 in range(p_1, max + 1):
        s = p_1 ** 2 + p_2 ** 2
        if 100 <= s < 1000:
            sums_of_two_squares[s] = [p_1, p_2]

for n in range(100, 1_000):
    i = nb_of_consecutive_squares(n)
    if i == 1:
        print(f'({n}, {n+1}, {n+2}) (equal to ({sums_of_two_squares[n][0]}^2+{sums_of_two_squares[n][1]}^2,'
                f' {sums_of_two_squares[n+1][0]}^2+{sums_of_two_squares[n+1][1]}^2,'
                f' {sums_of_two_squares[n+2][0]}^2+{sums_of_two_squares[n+2][1]}^2)) is a solution.')