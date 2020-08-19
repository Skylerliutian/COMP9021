# A polynomial object can be created from a string that represents a polynomial
# as sums or differences of monomials.
# - Monomials are ordered from highest to lowest powers.
# - All factors are strictly positive, except possibly for the leading factor
# - For nonzero powers, factors of 1 are only implicit.
# A single space surrounds + and - signs between monomials.

# Written by *** and Eric Martin for COMP9021


import re # split() suffices though
from collections import defaultdict
from copy import deepcopy


class Polynomial:
    def __init__(self, polynomial=None):
        self.grid = defaultdict(int)
        if polynomial is None:
            self.grid[0] = 0
        else:
            elements = polynomial.split(' ')
            first_pow_and_coe = self.construst_dic(elements[0])
            self.grid[first_pow_and_coe[0]] = first_pow_and_coe[1]
            for i in range(2, len(elements), 2):
                pow_and_coe = self.construst_dic(elements[i])
                if elements[i - 1] == '-':
                    self.grid[pow_and_coe[0]] = -1 * pow_and_coe[1]
                else:
                    self.grid[pow_and_coe[0]] = pow_and_coe[1]


    def construst_dic(self, part_element):
        index_of_x = part_element.find('x')
        if part_element[0] == '-':
            if index_of_x == -1:
                power = 0
                coe = int(part_element)
                return power, coe
            if index_of_x == len(part_element) - 1:
                power = 1
                if index_of_x > 1:
                    coe = int(part_element[:index_of_x])
                else:
                    coe = -1
            else:
                power = int(part_element[index_of_x + 2:])
                if index_of_x > 1:
                    coe = int(part_element[:index_of_x])
                else:
                    coe = -1
            return power, coe
        else:
            if index_of_x == -1:
                power = 0
                coe = int(part_element)
                return power, coe
            if index_of_x == len(part_element) - 1:
                power = 1
                if index_of_x != 0:
                    coe = int(part_element[:index_of_x])
                else:
                    coe = 1
            else:
                power = int(part_element[index_of_x + 2:])
                if index_of_x != 0:
                    coe = int(part_element[:index_of_x])
                else:
                    coe = 1
            return power, coe

    def __add__(self, other):
        new_grid = deepcopy(self)
        for o_key in other.grid.keys():
            if o_key in new_grid.grid.keys():
                new_grid.grid[o_key] = new_grid.grid[o_key] + other.grid[o_key]
            else:
                new_grid.grid[o_key] = other.grid[o_key]
        return new_grid

    def __mul__(self, other):
        new_grid = Polynomial()
        new_grid.grid.pop(0)
        for s_key in self.grid.keys():
            for o_key in other.grid.keys():
                if s_key + o_key not in new_grid.grid.keys():
                    new_grid.grid[s_key + o_key] = self.grid[s_key] * other.grid[o_key]
                else:
                    new_grid.grid[s_key + o_key] = new_grid.grid[s_key + o_key] + self.grid[s_key] * other.grid[o_key]
        return new_grid

    def __str__(self):
        if 0 in self.grid.keys() and self.grid[0] == 0:
            self.grid.pop(0)
        comp_dic = deepcopy(self.grid)
        for key in comp_dic.keys():
            if comp_dic[key] == 0:
                self.grid.pop(key)
        if len(self.grid) == 0:
            return '0'
        else:
            # 对字典进行排序
            sorted_dic = sorted(self.grid.items(), reverse=True)

            # 先提取出head部分
            if sorted_dic[0][0] == 0:
                if sorted_dic[0][1] == 1:
                    head = str(sorted_dic[0][1])
                elif sorted_dic[0][1] == -1:
                    head = '-1'
                else:
                    head = str(sorted_dic[0][1])
            elif sorted_dic[0][0] == 1:
                if sorted_dic[0][1] == 1:
                    head = 'x'
                elif sorted_dic[0][1] == -1:
                    head = '-x'
                else:
                    head = str(sorted_dic[0][1]) + 'x'
            else:
                if sorted_dic[0][1] == 1:
                    head = 'x^' + str(sorted_dic[0][0])
                elif sorted_dic[0][1] == -1:
                    head = '-x^' + str(sorted_dic[0][0])
                else:
                    head = str(sorted_dic[0][1]) + 'x^' + str(sorted_dic[0][0])

            result = ''

            # 对剩下的部分进行判断
            for i in range(1, len(sorted_dic)):
                if sorted_dic[i][1] < 0:
                    if sorted_dic[i][0] == 1:
                        if sorted_dic[i][1] != -1:
                            result += ' - ' + str(-1 * sorted_dic[i][1]) + 'x'
                        else:
                            result += ' - ' + 'x'
                    elif sorted_dic[i][0] == 0:
                        if sorted_dic[i][1] != -1:
                            result += ' - ' + str(-1 * sorted_dic[i][1])
                        else:
                            result += ' - ' + '1'
                    else:
                        if sorted_dic[i][1] != -1:
                            result += ' - ' + str(-1 * sorted_dic[i][1]) + 'x^' + str(sorted_dic[i][0])
                        else:
                            result += ' - ' + 'x^' + str(sorted_dic[i][0])
                else:
                    if sorted_dic[i][0] == 1:
                        if sorted_dic[i][1] != 1:
                            result += ' + ' + str(sorted_dic[i][1]) + 'x'
                        else:
                            result += ' + ' + 'x'
                    elif sorted_dic[i][0] == 0:
                        if sorted_dic[i][1] != 1:
                            result += ' + ' + str(sorted_dic[i][1])
                        else:
                            result += ' + ' + '1'
                    else:
                        if sorted_dic[i][1] != 1:
                            result += ' + ' + str(sorted_dic[i][1]) + 'x^' + str(sorted_dic[i][0])
                        else:
                            result += ' + ' + 'x^' + str(sorted_dic[i][0])

            result = head + result
            return result

# print(Polynomial())
# p = Polynomial('x')
# print(p + Polynomial('2x^3 + x - 4'))
#
# print(p)
# p += Polynomial('2x^3 + x - 4')
# print(p)
# p = Polynomial('4x^5 - x^2 + 6')
# print(p * Polynomial('x^3 - x + 4'))
# print(p)
# p *= Polynomial('x^3 - x + 4')
# print(p)
# p = Polynomial('x^4 - x^3 + x^2 - x')
# print(p * Polynomial('-2x^3 + 3x^2 - 4x + 5'))
# p = Polynomial('-5')
# p1 = Polynomial('x + 5')
# print(p1 + p)
# print(Polynomial('-x^2 + x - 5')+Polynomial('x^2 - x + 5'))


