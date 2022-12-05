from typing import List, Tuple, Dict
import os
import random
import pandas as pd
import numpy as np


class DataFromFile:
    """Class needed for work with files (.txt), which contains class function to return data from specific .txt file"""

    def __init__(self, filename_p: str, filename_t: str, filename_s: str, id_dataset_: int):
        """
        :param filename_p: filename with information about packages
        :param filename_t: filename with information about trucks
        :param filename_s: filename with information about storages
        :param id_dataset_: dataset id
        """
        self.filename1 = filename_p
        self.filename2 = filename_t
        self.filename3 = filename_s
        self.id_dataset = id_dataset_

    def __str__(self) -> str:
        return f"ID of dataset: {self.id_dataset} -> Names: '{self.filename1},'{self.filename2}','{self.filename3}'" \
            .format(self=self)

    def get_package_data(self) -> List[Tuple[int, int, float]]:
        """Extract data from .txt file into list of tuples, tuples contain information about packages: ID,
           address and weight """

        data_package = []
        with open(self.filename1, "r") as reader:
            id_p = 0
            for line in reader.readlines():
                data_temp = line.strip()
                address, weight = data_temp.split(':')
                package_tuple = id_p, int(address), float(weight)
                data_package.append(package_tuple)
                id_p += 1
        return data_package

    def get_truck_data(self) -> List[Tuple[int, str, float, float, float, float]]:
        """Extract data from .txt file into list of tuples, tuples contain information about trucks: ID, type, load,
           exploitation, minimal combustion, maximum combustion"""

        truck_package = []
        with open(self.filename2, "r") as reader:
            id_t = 0
            for line in reader.readlines():
                data_temp = line.strip()
                type_t, load, exp_cost, min_fuel_use, max_fuel_use = data_temp.split(':')
                truck_tuple = id_t, type_t, float(load), float(exp_cost), float(min_fuel_use), float(max_fuel_use)
                truck_package.append(truck_tuple)
                id_t += 1
        return truck_package

    def get_storage_data(self) -> List[Tuple[int, int, float]]:
        """Extract data from .txt file into list of tuples, tuples contain information about storages: ID, address,
           distance from main storage"""

        storage_package = []
        with open(self.filename3, "r") as reader:
            id_s = 0
            for line in reader.readlines():
                data_temp = line.strip()
                address, distance = data_temp.split(':')
                storage_tuple = id_s, int(address), float(distance)
                storage_package.append(storage_tuple)
                id_s += 1
        return storage_package

class Package:
    """Class needed for create packages and information about them"""

    pass

class Truck:
    """Class needed for create trucks and information about them"""

    pass

class Storage:
    """Class needed for create storages and information about them"""

    pass

class MainStorage:
    """Class needed for create main storage and all information about other smaller storages, trucks and packages"""

    pass
