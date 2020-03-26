'''
Will be tested with letters a string of DISTINCT UPPERCASE letters only.
'''
import re
from itertools import permutations
def f(letters):
    '''
    >>> f('ABCDEFGH')
    There is no solution
    >>> f('GRIHWSNYP')
    The pairs of words using all (distinct) letters in "GRIHWSNYP" are:
    ('SPRING', 'WHY')
    >>> f('ONESIX')
    The pairs of words using all (distinct) letters in "ONESIX" are:
    ('ION', 'SEX')
    ('ONE', 'SIX')
    >>> f('UTAROFSMN')
    The pairs of words using all (distinct) letters in "UTAROFSMN" are:
    ('AFT', 'MOURNS')
    ('ANT', 'FORUMS')
    ('ANTS', 'FORUM')
    ('ARM', 'FOUNTS')
    ('ARMS', 'FOUNT')
    ('AUNT', 'FORMS')
    ('AUNTS', 'FORM')
    ('AUNTS', 'FROM')
    ('FAN', 'TUMORS')
    ('FANS', 'TUMOR')
    ('FAR', 'MOUNTS')
    ('FARM', 'SNOUT')
    ('FARMS', 'UNTO')
    ('FAST', 'MOURN')
    ('FAT', 'MOURNS')
    ('FATS', 'MOURN')
    ('FAUN', 'STORM')
    ('FAUN', 'STROM')
    ('FAUST', 'MORN')
    ('FAUST', 'NORM')
    ('FOAM', 'TURNS')
    ('FOAMS', 'RUNT')
    ('FOAMS', 'TURN')
    ('FORMAT', 'SUN')
    ('FORUM', 'STAN')
    ('FORUMS', 'NAT')
    ('FORUMS', 'TAN')
    ('FOUNT', 'MARS')
    ('FOUNT', 'RAMS')
    ('FOUNTS', 'RAM')
    ('FUR', 'MATSON')
    ('MASON', 'TURF')
    ('MOANS', 'TURF')
    '''
    solutions = []
    # Insert your code here
    with open('dictionary.txt') as file:
        dic = set([line.strip() for line in file if len(line.strip()) == len(set(line.strip()))])
        words = sorted([''.join(x) for i in range(2,len(letters)) for x in permutations(letters, i) if ''.join(x) in dic])
        for w in words:
                left = set(letters) - set(w)
                l_w = sorted([''.join(x) for x in permutations(left, len(left)) if ''.join(x) in dic])
                for j in l_w:
                    if j in dic:
                        if (w,j) and (j,w) not in solutions:
                            solutions.append((w,j))
        if solutions:
            print(f'The pairs of words using all (distinct) letters in "{letters}" are:')
            for s in sorted(solutions):
                print(s)
        else:
            print(f'There is no solution')
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    with open('dictionary.txt') as file:
#        dic = set([line.strip() for line in file
#                      if len(line.strip()) == len(set(line.strip()))])
#        words = sorted([''.join(x) for i in range(2, len(letters))
#                        for x in permutations(letters,i)
#                        if ''.join(x) in dic])
#        for word in words:
#            remain_letters = set(letters) - set(word)
#            left_poss_words = sorted([''.join(x)
#                                      for x in permutations(remain_letters, len(remain_letters))
#                                      if ''.join(x) in dic])
#            for word_left in left_poss_words:
#                if (word, word_left) not in solutions and (word_left, word) not in solutions:
#                    solutions.append((word, word_left))
#        
#    if not solutions:
#        print('There is no solution')
#    else:
#        print(f'The pairs of words using all (distinct) letters in "{letters}" are:')
#        for solution in solutions:
#            print(solution)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
