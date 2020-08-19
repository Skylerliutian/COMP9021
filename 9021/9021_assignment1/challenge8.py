# Finds all sequences of consecutive prime 5-digit numbers,
# say (a, b, c, d, e, f), such that
# b = a + 2, c = b + 4, d = c + 6, e = d + 8, and f = e + 10.


from math import sqrt


def primes_num(n):
    for i in range(2, round(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


print('The solutions are:\n')
condition = [0, 2, 6, 12, 20, 30]
for n in range(10_001, 99_970, 2):
    if all((i in condition) == primes_num(n + i) for i in range(0, 31, 2)):
        for i in condition[:5]:
            print(n + i, end=' ')
        print(n + condition[5])

