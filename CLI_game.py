from classes import Cell
from classes import Game
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
    display_board(game)
    turn_tracker = 1
    # use the Game_State enum to determine if another turn should be played
    while Game_State.not_finished:
        # if turn tracker is odd, human is moving
        if turn_tracker % 2 == 1:
            player_move = get_player_move()
            start_row = player_move[0][0]
            start_col = player_move[0][1]
            end_row = player_move[1][0]
            end_col = player_move[1][1]
            game.human_player_move((start_row, start_col), (end_row, end_col))
        # if turn tracker is odd computer is moving
        else:
            # game.computer_player_move()
            pass
        turn_tracker += 1
        display_board(game)



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






def display_board(game: Game):
    # print top row
    print('  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9')
    print('-------------------------------------------')
    #print body of board
    for row in range(0, 10):
        if row == 10:
            to_print = str(row) + '|'
        else:
            to_print = str(row) + ' |'
        for col in range(0, 10):
            if (row, col) in game.human_player.troop_locations:
                to_print += "H"
            elif (row, col) in game.computer_player.troop_locations:
                to_print += "C"
            else:
                to_print += " "
            to_print += DISPLAY_DICT[game.board[row][col]]
            to_print += "|"
        print(to_print)
        print('-------------------------------------------')
    print('\n\n')


run_game()
