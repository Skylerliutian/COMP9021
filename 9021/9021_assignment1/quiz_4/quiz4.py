# Uses Heath Nutrition and Population statistics,
# stored in the file HNP_Data.csv.gz,
# assumed to be located in the working directory.
# Prompts the user for an Indicator Name. If it exists and is associated with
# a numerical value for some countries or categories, for some the years 1960-2015,
# then finds out the maximum value, and outputs:
# - that value;
# - the years when that value was reached, from oldest to more recents years;
# - for each such year, the countries or categories for which that value was reached,
#   listed in lexicographic order.
#
# Written by *** and Eric Martin for COMP9021


import sys
import os
import csv
import gzip


def main2(indicator_of_interest):
    filename = 'HNP_Data.csv.gz'
    if not os.path.exists(filename):
        print(f'There is no file named {filename} in the working directory, giving up...')
        sys.exit()

    #indicator_of_interest = input('Enter an Indicator Name: ')

    first_year = 1960
    number_of_years = 56
    max_value = None
    countries_for_max_value_per_year = {}

    with gzip.open(filename) as csvfile:
        file = csv.reader(line.decode('utf8').replace('\0', '') for line in csvfile)
        next(file)
        for line in file:
            if len(line) == 0:
                continue
            else:
                if line[2] == indicator_of_interest:
                    for index_year in range(number_of_years):
                        year = index_year + first_year
                        if line[index_year + 4] != '':
                            value_of_year = float(line[index_year + 4])
                            if max_value is None:
                                max_value = value_of_year
                            elif value_of_year > max_value:
                                max_value = value_of_year
                                countries_for_max_value_per_year = {}
                            elif value_of_year < max_value:
                                continue
                            if year not in countries_for_max_value_per_year:
                                countries_for_max_value_per_year[year] = [line[0]]
                            else:
                                countries_for_max_value_per_year[year].append(line[0])
        print(max_value)
        if max_value is None:
            pass
        elif round(max_value) == round(max_value, 1):

            max_value = round(max_value)
        else:
            max_value = round(max_value, 1)

    if max_value is None:
        print('Sorry, either the indicator of interest does not exist or it has no data.')
    else:
        print('The maximum value is:', max_value)
        print('It was reached in these years, for these countries or categories:')
        print('\n'.join(f'    {year}: {countries_for_max_value_per_year[year]}'
                        for year in sorted(countries_for_max_value_per_year)
                        )
              )
main2('Literacy rate, youth total (% of people ages 15-24)')