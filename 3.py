"""
Day 3
"""
import numpy as np
from typing import List, Tuple, Optional

filepath = "/home/warrot/projects/advent_of_coding/data/3.txt"

def index_constructor(n: int) -> List[List]:
    """
    Construct the indexes to search given a length of a number
    """

    # Default configuration for a single digit number
    arr = [[+1, -1], [+1, 0], [+1, +1], [0, -1], [0, +n], [-1, -1], [-1, 0], [-1, +1]]

    if n > 1:
        for i in range(2, n+1):
            arr.append([-1, +i])
            arr.append([+1, +i])

    return arr

def const_num(data: List[List], row: int, col: int, size: int) -> int:
    """
    Construct the number by stringing string together from a 2d array
    based on starting row, col and the length of the number
    """
    num = ''
    for i in range(size):
        num += data[row][col+i]
    
    return int(num)


def coords_are_valid(row, col, index_set, max: Optional[List[int]] = [140, 140]):  
    return (-1 < row + index_set[0] < max[0]) & (-1 < col + index_set[1] < max[1])

def find_data(data, row, col, index_set):
    """Return data value and index"""
    #index = [row+index_set[0], col+index_set[1]]
    return data[row+index_set[0]][col+index_set[1]]

def find_whole_number(data, row, col) -> Tuple[int, int]:
    """Return the full number based on a location with a single digit in the dataset
    Returns index of the first digit in the number, and the number itself
    """
    # What we know of the number
    digits = [data[row][col]]
    index = col
    continues_left = True
    continues_right = True

    # chek to the left
    check = -1
    while continues_left:
        if coords_are_valid(row, col, [0, check]):
            digit = find_data(data, row, col, [0, check])
            if digit in '0123456789':
                digits.insert(0, digit)
                index = col + check
                check -= 1
            else:
                continues_left = False
        else:
            continues_left = False

    check = 1
    while continues_right:
        if coords_are_valid(row, col, [0, check]):
            digit = find_data(data, row, col, [0, check])
            if digit in '0123456789':
                digits.append(digit)
                check += 1
            else:
                continues_right = False
        else:
            continues_right = False

    number = int(''.join(digits))

    return index, number


def run_3_2():
    """3_2
    Load all data into 2d array
    find all *
    Search around it for numbers, if 0 or none are present, discard
    Then determine if the digist above are one or two numbers, do the same below
    and add numbers to the sides. If not exactly 2 discard
    """
    total = 0
    
    # Load data in [row,cols]
    data = np.loadtxt(filepath, dtype=str, delimiter=None, comments=None)
    has_found_num = False

    places_to_side = [
        [0, -1], [0, +1],
    ]
    places_above = [
        [-1, -1], [-1, 0], [-1, +1],
    ]
    places_below = [
        [+1, -1], [+1, 0], [+1, +1]
    ]

    for row in range(len(data)):
        for col in range(len(data[0])):
            # Search for gears
            ratio = 1
            if data[row][col] == '*':
                num_of_num = 0
                
                # Check to the sides
                old_ind = []
                for place in places_to_side:
                    if coords_are_valid(row, col, place):
                        digit = find_data(data, row, col, place)
                        if digit in '0123456789':
                            ind, num = find_whole_number(data, row+place[0], col+place[1])
                            ratio *= num
                            num_of_num += 1
                
                # Check above
                old_ind = []
                for place in places_above:
                    if coords_are_valid(row, col, place):
                        digit = find_data(data, row, col, place)
                        if digit in '0123456789':
                            ind, num = find_whole_number(data, row+place[0], col+place[1])
                            if ind in old_ind:
                                continue  # break the cycle, its the same number
                            else:
                                old_ind.append(ind)
                                ratio *= num
                                num_of_num += 1

                # Check below
                old_ind = []
                for place in places_below:
                    if coords_are_valid(row, col, place):
                        print(f"{row=}, {col=}, {place=}")
                        if find_data(data, row, col, place) in '0123456789':
                            ind, num = find_whole_number(data, row+place[0], col+place[1])
                            if ind in old_ind:
                                continue  # break the cycle, its the same number
                            else:
                                old_ind.append(ind)
                                ratio *= num
                                num_of_num += 1
                if num_of_num == 2:
                    total += ratio
    return total


def run_3_1():
    """
    3_1
    Load all data into 2d array
    Loop over all rows and cols and look for numbers
    When a number is found look in all fields that are around and check if symbol exists
    If yes add to total, else continue
    """
    total = 0
    
    # Load data in [row,cols]
    data = np.loadtxt(filepath, dtype=str, delimiter=None, comments=None)
    has_found_num = False

    for row in range(len(data)):
        for col in range(len(data[0])):
            # Here it goes

            # Has already used part of this number
            if has_found_num:
                
                if data[row][col] in '0123456789':
                    # Still part of the same number
                    continue
                else:
                    # No longer part of number
                    has_found_num = False
                    continue
            
            # Discover start of new number
            if data[row][col] in '0123456789':
                has_found_num = True  # Used to skip parts of numbers after 
                is_num = True
                size = 1
                while is_num:
                    try:
                        if data[row][col+size] in '0123456789':
                            size += 1
                        else:
                            is_num = False
                    except IndexError:
                        is_num = False
                # Number construction done, now check adjecent indexes
                inds = index_constructor(size)
                #print(inds)
                for ind_set in inds:
                    if coords_are_valid(row, col, ind_set):
                        #print(f"found: {data[row+ind_set[0]][col+ind_set[1]]} as pos: {ind_set} relative to {const_num(data, row, col, size)}")
                        if data[row+ind_set[0]][col+ind_set[1]] not in ".0123456789":
                            # Is a valid symbol
                            num_is_valid = True
                            break
                        else:
                            num_is_valid = False
                    #else:
                     #   print(f"coords: {row+ind_set[0]}, {col+ind_set[1]}, are invalid")
                # Add the number to the total
                if num_is_valid:
                    #breakpoint()
                    total += const_num(data, row, col, size)

    return total

if __name__ == '__main__':
    print(run_3_2())