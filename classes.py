from enum import Enum
from dataclasses import dataclass


class Unit(Enum):
    # normal troops
    spy = 1
    scout = 2
    miner = 3
    sergeant = 4
    lieutenant = 5
    captain = 6
    major = 7
    colonel = 8
    marshal = 10
    # edge cases (subject to change)
    flag = 0
    bomb = 11
    water = -1
    equal_flag = -2



class Game:
    def __init__(self):
        self.human_player = Human_Player()
        self.computer_player = Computer_Player()
        self.board: list[list[Unit]] = [[]]


class Human_Player:
    def __init__(self):
        self.troop_locations: list[tuple]

    def initialize_locations(self):
        # will eventually initialize troop locations here
        pass


class Computer_Player:
    def __init__(self):
        self.troop_locations = [()]


def compare_units(unit1: Unit, unit2: Unit) -> list[Unit]:
    """
    compare units takes in 2 units and returns a list of units that "survive"
    Example: if unit1 is a scout, unit2 is a major, then the return is [unit2]
             if both units are scouts, the return is []
    There are a lot of edge cases when dealing with this
    :param unit1: first unit to be compared
    :param unit2: second unit to be compared
    :return: list of units that "survive" encounter
    """
    # lots of edge cases will eventually go in here
    # VERY basic cases
    if unit1.value > unit2.value:
        return [unit1]
    elif unit2.value > unit1.value:
        return [unit2]
    else:
        return []
