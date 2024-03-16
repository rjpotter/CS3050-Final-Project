"""
Jack Mahoney, Ryan Potter, Ethan Rowland, Cooper Zion
Stratego: Classes
CS 3050 - Software Engineering
3/4/2024
"""


from enum import Enum
from dataclasses import dataclass
from random import randint


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


class Game_State(Enum):
    not_finished = -1
    capture_flag = 0
    no_moves = 1
    repeat_moves = 2


class Game:
    def __init__(self):
        self.human_player = Human_Player()
        self.computer_player = Computer_Player()
        self.board = []
        self.intialize_board()
        self.game_state = Game_State.not_finished

    def get_valid_moves(self, row: int, col: int) -> list[tuple[int, int]]:
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

    def game_end(self, winner, condition: Game_State) -> None:
        # do stuff to display the winner here, not sure what this will look like yet, largely graphics dependant
        self.game_state = condition
        pass

    def human_player_move(self, start_location: tuple[int, int], end_location: tuple[int, int]) -> bool:
        """
        human_player_move intakes a start and end location for a human piece and carries out the move
        This method detects the player capturing the flag
        This method DOES NOT detect if there are no valid human moves
        This method updates the board list of Cells, along with each list of tuples for each player storing that
        players' troop locations
        :param start_location: start location tuple of the human piece being moved
        :param end_location: end location tuple of the human piece being moved
        :return: boolean, true if the move was valid, false otherwise
        """
        # make sure piece in start_location is move-able (i.e. not a bomb or a flag, and is a human piece)
        if start_location not in self.human_player.troop_locations:  # piece is not a human's
            return False
        if not self.is_moveable_cell(start_location[0], start_location[1]):  # player tried to move one of their bombs or flag
            return False

        # make sure move is valid (to a neighbor square, not water, not occupied by own piece)
        if end_location not in get_neighbors(start_location[0], start_location[1]):  # moving to a non-neighbor square
            # TODO: change this conditional for special case of miners
            return False
        if end_location in self.human_player.troop_locations:  # human already has a piece in the destination cell
            return False
        if self.board[end_location[0]][end_location[1]] == Cell.water:  # human attempting to move to water
            return False

        # now we know that the piece is moveable and the move is valid, thus carry out comparison and the move
        surviving_locations = compare_units(self.board, start_location, end_location)

        # check for win
        if len(surviving_locations) == 1 and surviving_locations[0] == Cell.flag:  # human captured comp flag
            self.game_end("Human", Game_State.capture_flag)

        # no win, update troop lists and board list
        if len(surviving_locations) == 0:  # both troops died
            # update the troop location lists
            self.human_player.troop_locations.remove(start_location)
            self.computer_player.troop_locations.remove(end_location)
            # update the board cells
            self.board[start_location[0]][start_location[1]] = Cell.empty
            self.board[end_location[0]][end_location[1]] = Cell.empty

        if start_location in surviving_locations:  # human troop survived, act accordingly
            # update the board cells
            self.board[end_location[0]][end_location[1]] = self.board[start_location[0]][start_location[1]]  # do this before we loose the information
            self.board[start_location[0]][start_location[1]] = Cell.empty
            # update the troop location lists
            self.human_player.troop_locations.remove(start_location)
            self.human_player.troop_locations.append(end_location)
            self.computer_player.troop_locations.remove(end_location)

        if end_location in surviving_locations:  # computer troop survived, act accordingly
            # update the board cells
            self.board[start_location[0]][start_location[1]] = Cell.empty
            # update the troop location lists
            self.human_player.troop_locations.remove(start_location)

        return True


    def computer_player_move(self) -> None:
        """
        computer_player_move picks a random move able computer piece and makes a random valid move
        This method detects a situation where there are no possible computer moves (computer loses)
        This method detects the computer capturing the flag
        This method updates the board list of Cells, along with each list of tuples for each player storing that
        players' troop locations
        :return: nothing
        """

        comp_troop_locations_copy = self.computer_player.troop_locations.copy()

        found_move = False
        valid_moves: list[tuple[int, int]] = []
        while not found_move and len(comp_troop_locations_copy) > 0:
            troop_to_move_row, troop_to_move_col = comp_troop_locations_copy.pop(randint(0, len(comp_troop_locations_copy) - 1))
            while not self.is_moveable_cell(troop_to_move_row, troop_to_move_col):
                comp_troop_locations_copy.pop(randint(0, len(comp_troop_locations_copy) - 1))
            # we now know there is a move able troop at the row and col

            # now find out if the move able troop actually has a move
            # start by finding candidate squares
            possible_moves: list[tuple[int, int]] = get_neighbors(troop_to_move_row, troop_to_move_col)
            for possible_move in possible_moves:  # test to see if move is possible, lots of edge cases
                valid_move_bool = True
                # test if computer already has a piece there
                if possible_move in self.computer_player.troop_locations:
                    valid_move_bool = False
                # test if candidate move would move piece into lake
                possible_row, possible_col = possible_move
                if self.board[possible_row][possible_col] == Cell.water:
                    valid_move_bool = False

                # if we valid_move_bool = True, then we have a possible, valid move
                if valid_move_bool:
                    valid_moves.append(possible_move)
                    found_move = True

        # if we couldn't find a valid move, then the human won
        if not found_move:
            self.game_end('Human', Game_State.no_moves)
        else:
            # have potentially many moves in valid_moves, pick a random one
            selected_move = valid_moves.pop(randint(0, len(valid_moves) - 1))
            selected_troop_location = (troop_to_move_row, troop_to_move_col)  # to get here must have row and col

            # now must carry out the move. First step is to do the comparison between the troops
            surviving_locations: list[tuple[int, int]] = compare_units(selected_troop_location, selected_move)


            # check to see if the computer captured the flag, if so, end game
            if self.board[surviving_locations[0][0]][surviving_locations[0][1]] == Cell.flag:
                self.game_end("Computer", Game_State.capture_flag)

            # if computer troop survives, do things
            if selected_troop_location in surviving_locations:
                self.computer_player.troop_locations.append(selected_move)  # update computer troop locations
                # update board by copying enum from old location to new location
                self.board[selected_move[0]][selected_move[1]] = self.board[selected_troop_location[0]][selected_troop_location[1]]

            # deal with player troop, if applicable
            if selected_move not in surviving_locations:
                # remove player troop from list of player troop locations
                self.human_player.troop_locations.remove(selected_move)

            if len(surviving_locations) == 0: # both troops died, will always update board for comp later
                self.board[selected_move[0]][selected_move[1]] = Cell.empty

            # whatever happened, the moved troop will not be where it originally was (either died or was moved)
            self.computer_player.troop_locations.remove(selected_troop_location)  # update computer troop list
            self.board[selected_troop_location[0]][selected_troop_location[1]] = Cell.empty  # update board locations

    def is_moveable_cell(self, row: int, col: int) -> bool:
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


def compare_units(board: list[list[Cell]], unit1_location: tuple[int, int], unit2_location: tuple[int, int]) -> list[tuple[int, int]]:
    """
    compare units takes in 2 units and returns a list of units that "survive"
    Example: if unit1 is a scout, unit2 is a major, then the return is [unit2]
             if both units are scouts, the return is []
    There are a lot of edge cases when dealing with this
    Unit1 is the unit that is moving, unit2 is the unit that is being moved on to
    :param board: board to be doing comparison on
    :param unit1_location: first unit location to be compared
    :param unit2_location: second unit location to be compared
    :return: list of units that "survive" encounter
    """
    # extract unit types
    unit1 = board[unit1_location[0]][unit1_location[1]]
    unit2 = board[unit2_location[0]][unit2_location[1]]
    # lots of edge cases will eventually go in here
    # case where unit 1 is spy, unit 2 is marshal
    if unit1 == Cell.spy and unit2 == Cell.marshal:
        return [unit1_location]
    # case where miner is going onto bomb
    if unit1 == Cell.miner and unit2 == Cell.bomb:
        return [unit1_location]
    # case where flag is captured (game is won)
    if unit2 == Cell.flag:
        return [unit2_location]

    # VERY basic cases
    if unit1.value > unit2.value:
        return [unit1_location]
    elif unit2.value > unit1.value:
        return [unit2_location]
    else:
        return []


def get_neighbors(row: int, col: int) -> list[tuple[int, int]]:
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

