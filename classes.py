"""
Jack Mahoney, Ryan Potter, Ethan Rowland, Cooper Zion
Stratego: Classes
CS 3050 - Software Engineering
3/4/2024
"""


from enum import Enum
from dataclasses import dataclass


class Cell(Enum):
    # normal troops
    spy = 1
    scout = 2
    miner = 3
    sergeant = 4
    lieutenant = 5
    captain = 6
    major = 7
    colonel = 8
    general = 9
    marshal = 10
    # edge cases (subject to change)
    empty = 0
    bomb = 11
    flag = -1
    water = 12


class Game:
    def __init__(self):
        self.human_player = Human_Player()
        self.computer_player = Computer_Player()
        self.board = []
        self.intialize_board()

    def get_valid_moves(self, row: int, col: int) -> list[tuple[int,int]]:
        """
        get_valid_moves takes in a row and a col and returns a list of valid moves for the troop in that location
        :param row:
        :param col:
        :return:
        """
        valid_moves = []

        if not self.is_moveable_cell(row, col):
            return []

        neighbors = get_neighbors(row, col)
        for neighbor_cell in neighbors:
            if neighbor_cell == Cell.empty:
                valid_moves.append((row, col))
            elif neighbor_cell != Cell.water:
                valid_moves.append((row, col))







    def is_moveable_cell(self, row, col) -> bool:
        """
        is_moveable cell returns a bool depending on if there is a moveable unit at the location given by row,col
        :param row: row of potentially moveable unit
        :param col: col of potentially moveable unit
        :return: True if unit is moveable, false otw
        """
        if row not in range(1, 11):
            print('invalid row in is_moveable_cell')
            return False
        elif col not in range(1,11):
            print('invalid col in is_moveable_cell')
            return False
        # Know that we can safely index
        # get value of Cell enum at argument location
        # if value is a moveable piece value, return true, else return false
        if self.board[row][col].value in range(1, 11):
            return True
        else:
            return False

    def intialize_board(self):
        # append computer player rows
        self.board.append([Cell.flag, Cell.bomb, Cell.bomb, Cell.bomb, Cell.bomb, Cell.bomb, Cell.bomb, Cell.marshal, Cell.general, Cell.colonel])
        self.board.append([Cell.colonel, Cell.major, Cell.major, Cell.major, Cell.captain, Cell.captain, Cell.captain, Cell.captain, Cell.lieutenant, Cell.lieutenant])
        self.board.append([Cell.lieutenant, Cell.lieutenant, Cell.sergeant, Cell.sergeant, Cell.sergeant, Cell.sergeant, Cell.miner, Cell.miner, Cell.miner, Cell.miner])
        self.board.append([Cell.miner, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.spy])
        # 2 empty rows
        self.board.append([Cell.empty, Cell.empty, Cell.water, Cell.water, Cell.empty, Cell.empty, Cell.water, Cell.water, Cell.empty, Cell.empty])
        self.board.append([Cell.empty, Cell.empty, Cell.water, Cell.water, Cell.empty, Cell.empty, Cell.water, Cell.water, Cell.empty, Cell.empty])
        # 4 player rows
        self.board.append([Cell.miner, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.scout, Cell.spy])
        self.board.append([Cell.lieutenant, Cell.lieutenant, Cell.sergeant, Cell.sergeant, Cell.sergeant, Cell.sergeant, Cell.miner, Cell.miner, Cell.miner, Cell.miner])
        self.board.append([Cell.colonel, Cell.major, Cell.major, Cell.major, Cell.captain, Cell.captain, Cell.captain, Cell.captain, Cell.lieutenant, Cell.lieutenant])
        self.board.append([Cell.flag, Cell.bomb, Cell.bomb, Cell.bomb, Cell.bomb, Cell.bomb, Cell.bomb, Cell.marshal, Cell.general, Cell.colonel])






class Human_Player:
    def __init__(self):
        self.troop_locations: list[tuple[int, int]] = []
        self.initialize_locations()

    def initialize_locations(self):
        # human starts with troops in the bottom 4 rows of the board
        for row in range(6, 10):
            for col in range(10):
                self.troop_locations.append((row, col))


class Computer_Player:
    def __init__(self):
        self.troop_locations: list[tuple[int, int]] = []
        self.initialize_locations()

    def initialize_locations(self):
        # computer starts with troops in the top 4 rows of the board
        for row in range(0, 5):
            for col in range(10):
                self.troop_locations.append((row, col))


def compare_units(unit1: Cell, unit2: Cell) -> list[Cell]:
    """
    compare units takes in 2 units and returns a list of units that "survive"
    Example: if unit1 is a scout, unit2 is a major, then the return is [unit2]
             if both units are scouts, the return is []
    There are a lot of edge cases when dealing with this
    Unit1 is the unit that is moving, unit2 is the unit that is being moved on to
    :param unit1: first unit to be compared
    :param unit2: second unit to be compared
    :return: list of units that "survive" encounter
    """
    # lots of edge cases will eventually go in here
    # case where unit 1 is spy, unit 2 is marshal
    if unit1 == Cell.spy and unit2 == Cell.marshal:
        return [unit1]
    # case where miner is going onto bomb
    if unit1 == Cell.miner and unit2 == Cell.bomb:
        return [unit1]
    # case where flag is captured (game is won)
    if unit2 == Cell.flag:
        return [unit2]

    # VERY basic cases
    if unit1.value > unit2.value:
        return [unit1]
    elif unit2.value > unit1.value:
        return [unit2]
    else:
        return []


def get_neighbors(row: int, col: int) -> list[tuple[int,int]]:
    """
    get_neighbors returns a list of tuples specifying the list of valid neighbor location
    :param row: row of input location
    :param col: col of input location
    :return: list of tuples representing locations of valid neighbor cells
    """
    neighbors = []
    # if not on top row, get top neighbor
    if row > 1:
        neighbors.append((row - 1, col))
    # if not on bottom row, get bottom neighbor
    if row < 10:
        neighbors.append((row + 1, col))
    # if not on left col, get left neighbor
    if col > 1:
        neighbors.append((row, col - 1))
    # if not on right col, get right neighbor
    if col < 10:
        neighbors.append((row, col + 1))
    # return result
    return neighbors

