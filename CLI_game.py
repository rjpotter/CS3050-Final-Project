from classes import Cell
from classes import Game

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
    # while loop
    display_board(game)
    print(game.human_player.troop_locations)
    print((6, 4) in game.human_player.troop_locations)
    print(game.human_player_move((6, 4), (5, 4)))
    display_board(game)
    game.human_player_move((5,4), (4,4))
    display_board(game)
    game.human_player_move((4,4), (3,4))
    display_board(game)





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
