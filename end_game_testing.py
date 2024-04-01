from classes import Game
from classes import Cell
from classes import Game_State

DISPLAY_DICT = {
    Cell.spy: ' 1',
    Cell.scout: ' 2',
    Cell.miner: ' 3',
    Cell.sergeant: ' 4',
    Cell.lieutenant: ' 5',
    Cell.captain: ' 6',
    Cell.major: ' 7',
    Cell.colonel: ' 8',
    Cell.general: ' 9',
    Cell.marshal: '10',

    Cell.empty: '  ',
    Cell.bomb: ' B',
    Cell.flag: ' F',
    Cell.water: 'W '
}


def run_game():
    # set up game
    game = Game()
    turn_tracker = 1
    display_board(game, turn_tracker)
    # force board into end state
    game.board[4][0] = Cell.bomb
    game.board[4][1] = Cell.bomb
    game.board[4][4] = Cell.bomb
    game.board[4][5] = Cell.bomb
    game.board[4][8] = Cell.bomb
    game.board[4][9] = Cell.bomb
    display_board(game, turn_tracker)

    # use the Game_State enum to determine if another turn should be played
    while game.game_state == Game_State.not_finished:
        # if turn tracker is odd, human is moving
        if turn_tracker % 2 == 1:
            player_move = get_player_move()
            start_row = player_move[0][0]
            start_col = player_move[0][1]
            end_row = player_move[1][0]
            end_col = player_move[1][1]
            game.human_player_move((start_row, start_col), (end_row, end_col))
        # if turn tracker is even computer is moving
        else:
            game.computer_player_move()

        turn_tracker += 1
        display_board(game, turn_tracker)
        print()



    '''
    print(game.human_player.troop_locations)
    print((6, 4) in game.human_player.troop_locations)
    print(game.human_player_move((6, 4), (5, 4)))
    display_board(game)
    game.human_player_move((5,4), (4,4))
    display_board(game)
    game.human_player_move((4,4), (3,4))
    display_board(game)
    '''
def get_player_move() -> tuple[tuple[int, int], tuple[int, int]]:
    # take user row and columns as inputs and cast them as ints
    print("Input the location of the piece you want to move:")
    start_row = input("Row:")
    start_row = int(start_row)
    start_col = input("Column:")
    start_col = int(start_col)
    start_tuple = (start_row, start_col)
    print("Enter where you want to move the piece:")
    end_row = input("Row:")
    end_row = int(end_row)
    end_col = input("Column:")
    end_col = int(end_col)
    end_tuple = (end_row, end_col)
    # return a tuple of tuples of ints containing start and end location data
    player_move = (start_tuple, end_tuple)
    return player_move



def display_board(game: Game, turn_tracker: int):
    # Display turn number, make every 2 turns display as 1 (human & computer on same turn)
    if turn_tracker % 2 == 1:
        # Human turn
        print(f"\nTurn: {(turn_tracker//2) + 1} Player\n")
    else:
        # Computer turn
        print(f"\nTurn: {((turn_tracker - 1)//2) + 1} Computer\n")
    # print top row
    print('  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9')
    print('-------------------------------------------')
    #print body of board
    for row in range(0, 10):
        if row == 10:
            to_print = str(row) + '|'
        else:
            to_print = str(row) + ' |'
        for col in range(10):
            # Determine if this cell is the last move of human or computer
            color_code = ""
            if (row, col) == game.last_human_move:
                color_code = "\033[92m"  # Green for human
            elif (row, col) == game.last_computer_move:
                color_code = "\033[91m"  # Red for computer

            if (row, col) in game.human_player.troop_locations:
                cell_owner = "H"
            elif (row, col) in game.computer_player.troop_locations:
                cell_owner = "C"
            else:
                cell_owner = " "

            cell_display = DISPLAY_DICT[game.board[row][col]]
            # Print move with color (for last piece moved)
            to_print += f"{color_code}{cell_owner}{cell_display}\033[0m|"  # Reset color after each cell

        print(to_print)
        print('-------------------------------------------')


run_game()