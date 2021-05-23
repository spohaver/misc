#!/usr/bin/env python3
# Testing out python functions vs binary search
import sys
from math import floor
from random import randint
from time import perf_counter


MAXNUM = 65536
SEARCH_TIMES = 1000


def build_random_list(num_items, maxnum=MAXNUM):
    """ takes num_items and builds a list of random numbers """
    return [randint(0,maxnum) for i in range(num_items)]


def python_sort(items):
    """ use python libary to sort items, broke this out
        to see about possibly adding in binary insert
    """
    return sorted(items)


def get_pivot(begin, end):
    """ takes begin, end, and finds the 'middle' """
    return int(floor((begin + end)/2))


def binary_search(items, search_value):
    """ using binary search methodolgy to search items
    :param items: items to be searched
    :type items: list
    :param search_value: value we are querying from items
    :type search_value: int (in this case)
    """
    start = 0
    end = len(items)
    pivot = get_pivot(start, end)
    is_found = False
    while not is_found  and start < end:
        if items[pivot] == search_value:
            is_found = True
            break
        if (search_value < items[pivot]):
            end = pivot - 1
        else:
            start = pivot + 1
        pivot = get_pivot(start, end)
    return is_found


def python_search(items, search_value):
    """ quick and dirty python library for searching
    :param items: items to be searched
    :type items: list
    :param search_value: value we are quering from items
    :type search_value: int (in this case)
    """
    if search_value in items:
        return True
    else:
        return False


def main():
    """ party """
    print('Binary vs Python Search')
    item_sets = [10, 1000, 1000000]
    for num_items in item_sets:
        print('Testing with {0} random numbers, 0-{1}'.format(num_items, MAXNUM))
        tic = perf_counter()
        items = python_sort(build_random_list(num_items))
        toc = perf_counter()
        print('  - Build time: {0:0.4f}s'.format(toc-tic))
        tic = toc = 0
        print('  - Binary: ',)
        tic = perf_counter()
        count_true = 0
        count_false = 0
        for num in range(SEARCH_TIMES):
            query = int(randint(0,MAXNUM))
            if binary_search(items, query):
                count_true += 1
            else:
                count_false += 1
        toc = perf_counter()
        print('True: {0}; False: {1}; Time: {2:0.4f}s'.format(
            count_true,
            count_false,
            toc-tic)
        )
        print('  - Python: ',)
        tic = perf_counter()
        count_true = 0
        count_false = 0
        for num in range(SEARCH_TIMES):
            query = int(randint(0,MAXNUM))
            if python_search(items, query):
                count_true += 1
            else:
                count_false += 1
        toc = perf_counter()
        print('True: {0}; False: {1}; Time: {2:0.4f}s'.format(
            count_true,
            count_false,
            toc-tic)
        )
    return 0


if __name__ == '__main__':
    sys.exit(int(main()))
