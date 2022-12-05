"""Additional file to define auxiliary functions"""
from typing import List, Tuple, Dict
import random
from graphviz import Digraph


def flat_list(org_list_: List[List[int]]) -> List[int]:
    """Flattened function to do List from List of Lists"""

    flat_lst = []
    for sublist in org_list_:
        if isinstance(sublist, list):
            for item in sublist:
                flat_lst.append(item)
        else:
            flat_lst.append(sublist)

    return flat_lst


def ge_rand(list_divisors_: List[List[int]], num_cross_points_: List[int]) -> Tuple[List[List[int]], List[List[int]]]:
    """Generate lists which tells you which genes to take from a particular parent (used in function: crossover)"""

    rand_lst1 = []  # Shows which part of divided chromosome stay from parent 1
    rand_lst2 = []  # Shows which part of divided chromosome stay from parent 2
    for i, j in enumerate(list_divisors_):
        temp = random.sample(range(len(j)), int(num_cross_points_[i] / 2))
        rand_lst1.append(temp)
        temp2 = []
        for p, k in enumerate(j):
            if p not in temp:
                temp2.append(p)
        rand_lst2.append(temp2)
    del temp, temp2

    tup_of_rand_lst = (rand_lst1, rand_lst2)

    return tup_of_rand_lst