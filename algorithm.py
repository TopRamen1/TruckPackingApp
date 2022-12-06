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


def print_sol(data: MainStorage, best_sol):
    """Prints best solution"""

    p_to_t = {}

    for i in range(0, len(best_sol.ch_p)):
        if best_sol.ch_p[i] in p_to_t.keys():
            p_to_t[best_sol.ch_p[i]].append(i)
        else:
            p_to_t[best_sol.ch_p[i]] = [i]

    print("Koszt: ", best_sol.obj_fcn)

    for k, v in p_to_t.items():
        sum = 0
        for e in v:
            sum += data.list_of_packages[e].weight

        print(k, "ladowność: ", data.list_of_trucks[k].load, ", paczki: ", v, " suma wag: ", sum, " adres: ",
              data.list_of_packages[v[0]].address)

    return p_to_t


def obj_fcn(data_mst: MainStorage, data_ind: Individual) -> float:
    """Calculate function which describes our problem
       :return: value of above function"""

    act_truck_pos = [i for i, m in enumerate(data_ind.ch_t) if m != -1]  # truck's id who has defined storage
    act_package_pos = [j for j, p in enumerate(data_ind.ch_p)]  # package's id
    sum_1, sum_2, sum_3 = 0, 0, 0

    # Sum_1:
    for i in act_truck_pos:
        sum_1 += data_mst.list_of_trucks[i].exp_cost

    # Sum_2:
    for i in act_truck_pos:
        sum_2 += data_mst.list_of_storages[data_ind.ch_t[i]].distance / 100 * data_mst.k * \
                 data_mst.list_of_trucks[i].min_fuel_use

    # Sum_3:
    for i in act_truck_pos:
        sum_packages = 0
        for j in act_package_pos:
            if i == data_ind.ch_p[j]:
                sum_packages += data_mst.list_of_packages[j].weight
        sum_3 += data_mst.list_of_storages[data_ind.ch_t[i]].distance / 100 * data_mst.k * \
                 (data_mst.list_of_trucks[i].max_fuel_use - data_mst.list_of_trucks[i].min_fuel_use) * \
                 (sum_packages / data_mst.list_of_trucks[i].load)

    final_result = sum_1 + sum_2 + sum_3

    return final_result


class Exception1(Exception):
    def __init__(self, message="Przekroczono pierwszy warunek ograniczający"):
        self.message = message
        super().__init__(self.message)


class Exception2(Exception):
    def __init__(self, message="Przekroczono drugi warunek ograniczający"):
        self.message = message
        super().__init__(self.message)


class Exception3(Exception):
    def __init__(self, message="Przekroczono trzeci warunek ograniczający"):
        self.message = message
        super().__init__(self.message)


def check_lims(data_mst: MainStorage, data_ind: Individual):
    """Checks limits and raises exceptions"""

    act_package_pos = [j for j, p in enumerate(data_ind.ch_p)]
    act_truck_pos = [i for i, m in enumerate(data_ind.ch_t) if m != -1]
    sum_weights = 0

    """ Checking the first limit """
    for i in data_mst.list_of_packages:
        sum_weights += i.weight
    sum_loads = 0
    for j in data_mst.list_of_trucks:
        sum_loads += j.load
    if sum_weights > sum_loads:
        raise Exception1

    """ Checking the second limit """
    for i in act_truck_pos:
        sum_weights = 0
        for j in act_package_pos:
            if i == data_ind.ch_p[j]:
                sum_weights += data_mst.list_of_packages[j].weight
        if sum_weights > data_mst.list_of_trucks[i].load:
            raise Exception2

    """ Checking the third limit """
    for i in data_ind.ch_p:
        if i == -1:
            raise Exception3

def random_chromosome(data: MainStorage):
    """Generates a random Chromosome for individual
    :return: random chromosome"""

    # Id lists for calculations
    storage_ids = list(range(0, len(data.list_of_storages)))
    truck_ids = list(range(0, len(data.list_of_trucks)))
    package_ids = list(range(0, len(data.list_of_packages)))

    # Init chromosome
    ch_t = [-1] * len(data.list_of_trucks)
    ch_p = [-1] * len(data.list_of_packages)

    # Sorted packages by address
    ids_by_address = [[] for i in range(len(storage_ids))]
    for p_id in package_ids:
        ids_by_address[data.list_of_packages[p_id].address].append(p_id)

    while package_ids:
        for p_to_add in ids_by_address:
            while p_to_add:
                if not truck_ids:
                    print("to many packages error")
                    return [0], [0]

                t = data.list_of_trucks[random.choice(truck_ids)]  # Random truck
                truck_ids.remove(t.id)

                p = data.list_of_packages[random.choice(p_to_add)]  # Random package

                ch_t[t.id] = p.address  # Adding truck address to chromosome

                weight_sum = 0
                while t.load >= weight_sum + p.weight:
                    weight_sum += p.weight

                    ch_p[p.id] = t.id  # Adding truck id for package in chromosome

                    package_ids.remove(p.id)
                    p_to_add.remove(p.id)

                    if p_to_add:
                        p = data.list_of_packages[random.choice(p_to_add)]
                    else:
                        break

    return ch_t, ch_p
