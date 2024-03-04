from enum import Enum


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
        self.board = [[]]


class Human_Player:
    def __init__(self):
        self.troop_locations = [()]


class Computer_Player:
    def __init__(self):
        self.troop_locations = [()]


def compare_troops(unit1: Unit, unit2: Unit) -> Unit:
    # lots of edge cases will eventually go in here
    if unit1.value > unit2.value:
        return unit1
    elif unit2.value > unit1.value:
        return unit2
    else:
        return Unit.equal_flag
