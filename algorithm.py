from algorithm_data import *
import extra_functions as ex_fun
from typing import List, Tuple
import random
import matplotlib.pyplot as plt
from copy import deepcopy


class Individual:
    """Class containing individual chromosome and rating"""

    def __init__(self, ch_t_: List[int], ch_p_: List[int], prob_: float = 0):
        """
        :param ch_t_: part dedicated to showing which truck goes where
        :param ch_p_: part representing which package goes to which truck
        :param prob_: probability of choosing this individual
        """

        self.ch_t = ch_t_
        self.ch_p = ch_p_

        self.obj_fcn = 0
        self.prob = prob_

    def __str__(self):
        return str(self.ch_t) + ' ' + str(self.ch_p) + ' ' + str(self.prob) + ' ' + str(self.obj_fcn) + ' ' + \
               str(len(self.ch_p))


def genetic_alg(data: MainStorage, it_num: int, pop_size: int, cross: float, mut: float, div: List[int],
                debug: bool = False, plot: bool = False, desc: str = ""):
    """Implementation of genetic algorithm
    :return: printed solutions for each iteration and its plots"""

    av_sol_vec = []
    best_sol_vec = []

    pop = init_pop(data, pop_size)
    pop, best_sol, best_val, av_sol = fitness(data, pop)

    av_sol_vec.append(av_sol)
    best_sol_vec.append(best_sol.obj_fcn)

    pop = selection(data, pop)

    print_pop(pop, "Populacja po inicjalizacji:", debug)

    i = 1

    while i <= it_num:
        pop = cross_pop(data, pop, div, cross)

        pop = mutation(data, pop, mut)

        pop, it_best_sol, it_best_val, av_sol = fitness(data, pop)

        if it_best_sol.obj_fcn < best_sol.obj_fcn:
            best_sol = deepcopy(it_best_sol)

        av_sol_vec.append(av_sol)
        best_sol_vec.append(best_sol.obj_fcn)

        pop = selection(data, pop)

        print_pop(pop, "Populacja po iteracji: {}".format(i), debug)

        i += 1

    if plot:
        plt.plot(range(len(av_sol_vec)), av_sol_vec, label='średnia')
        plt.title("Średnia wartość funkcji celu dla {}".format(desc))
        plt.ylabel("wartość")
        plt.xlabel("iteracje")
        plt.show()
        plt.plot(range(len(best_sol_vec)), best_sol_vec, label='rozwiązania')
        plt.title("Wartość najlepszego rozwiązania {}".format(desc))
        plt.ylabel("wartość")
        plt.xlabel("iteracje")
        plt.show()

    return best_sol, best_sol_vec, av_sol_vec
