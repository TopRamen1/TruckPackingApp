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