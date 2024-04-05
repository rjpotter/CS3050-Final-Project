"""
Project by: Jack Mahoney, Ryan Potter, Ethan Rowland, Cooper Zion
Title: Stratego: Graphics
Course: CS 3050 - Software Engineering
Date: March 6, 2024
"""

import arcade
from classes import Game, Cell, Game_State

# Initialize screen dimensions and game title
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Stratego"
SQUARE_SIZE = 64  # Each square size on the board

# Mapping game pieces to their symbols for display
DISPLAY_DICT = {
    Cell.spy: '1', Cell.scout: '2', Cell.miner: '3',
    Cell.sergeant: '4', Cell.lieutenant: '5', Cell.captain: '6',
    Cell.major: '7', Cell.colonel: '8', Cell.general: '9',
    Cell.marshal: '10', Cell.empty: ' ', Cell.bomb: 'B',
    Cell.flag: 'F', Cell.water: 'W'
}

class MyGame(arcade.Window):
    def __init__(self, width, height, title, game):
        super().__init__(width, height, title)
        # Game logic holder
        self.game = game
        # Selected piece tracker
        self.selected_piece = None
        # Background color setup
        arcade.set_background_color(arcade.color.AMAZON)
        # Piece dimensions based on texture size
        self.TEXTURE_IMAGE_WIDTH = 1430
        self.TEXTURE_IMAGE_HEIGHT = 794
        self.PIECE_WIDTH = int(self.TEXTURE_IMAGE_WIDTH / 6)
        self.PIECE_HEIGHT = int(self.TEXTURE_IMAGE_HEIGHT / 2)
        # Highlight tracking
        self.highlighted_square = None
        self.highlight_color = arcade.color.WHITE  # Default highlight color
        # Sprites placeholders
        self.blue_sprites = arcade.SpriteList()
        self.red_sprites = arcade.SpriteList()

    def setup(self):
        # Calculate texture coordinates for slicing
        texture_map_cords = [
            [self.PIECE_WIDTH * jj, self.PIECE_HEIGHT * ii, self.PIECE_WIDTH, self.PIECE_HEIGHT]
            for ii in range(2) for jj in range(6)
        ]
        # Loading textures for pieces
        blue_textures = arcade.load_textures("img/blue_pieces.png", texture_map_cords, mirrored=False, flipped=False)
        red_textures = arcade.load_textures("img/red_pieces.png", texture_map_cords, mirrored=False, flipped=False)

    def draw_board_pieces(self):
        # Drawing pieces on the board based on current game state
        for row in range(10):
            for col in range(10):
                cell = self.game.board[row][col]
                display_text = DISPLAY_DICT[cell]
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = SCREEN_HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)
                text_color = arcade.color.BLACK  # Default color
                if (row, col) == self.game.last_human_move:
                    text_color = arcade.color.GREEN
                elif (row, col) == self.game.last_computer_move:
                    text_color = arcade.color.RED
                arcade.draw_text(display_text, x, y, text_color, 12, anchor_x="center", anchor_y="center")

    def highlight_square(self, row, col, color=arcade.color.YELLOW, duration=0):
        # Highlight a square temporarily for invalid moves, or maintain highlight for selection
        if color == arcade.color.RED:
            temporary_highlight = (row, col)
            arcade.schedule(lambda delta_time: self.reset_temporary_highlight(temporary_highlight), duration)
        else:
            self.highlighted_square = (row, col)
        self.highlight_color = color

    def reset_temporary_highlight(self, square):
        # Revert temporary highlight color
        if self.highlighted_square == square:
            self.highlight_color = arcade.color.YELLOW

    def on_draw(self):
        arcade.start_render()  # Prepare for drawing
        # Drawing game board background
        board_color = arcade.color.DARK_OLIVE_GREEN
        arcade.draw_xywh_rectangle_filled(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, board_color)
        # Outlining board squares and drawing impassable terrain
        outline_color = arcade.color.BLACK
        for row in range(10):
            for col in range(10):
                x = (col * SQUARE_SIZE) + SQUARE_SIZE // 2
                y = (row * SQUARE_SIZE) + SQUARE_SIZE // 2
                arcade.draw_rectangle_outline(x, y, SQUARE_SIZE, SQUARE_SIZE, outline_color, 2)
        # Lake positions
        lake_color = arcade.color.BLUE
        lakes_positions = [(2, 4), (2, 5), (3, 4), (3, 5), (6, 4), (6, 5), (7, 4), (7, 5)]
        for pos in lakes_positions:
            x = pos[0] * SQUARE_SIZE
            y = pos[1] * SQUARE_SIZE
            arcade.draw_xywh_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, lake_color)
        # Highlighting the selected square
        if self.highlighted_square:
            row, col = self.highlighted_square
            x = (col * SQUARE_SIZE) + (SQUARE_SIZE // 2)
            y = SCREEN_HEIGHT - (row * SQUARE_SIZE + (SQUARE_SIZE // 2))
            arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, self.highlight_color)
        # Drawing pieces on the board
        self.draw_board_pieces()

    def on_mouse_press(self, x, y, button, modifiers):
        # Handle piece selection and movement
        if button == arcade.MOUSE_BUTTON_LEFT:
            col = x // SQUARE_SIZE
            row = 9 - (y // SQUARE_SIZE)
            if self.selected_piece == (row, col):
                # Deselect the piece if it's already selected
                self.selected_piece = None
                self.highlight_color = arcade.color.WHITE
                self.highlighted_square = None
            elif self.selected_piece:
                start_row, start_col = self.selected_piece
                valid_move = self.game.human_player_move((start_row, start_col), (row, col))
                if valid_move:
                    self.selected_piece = None
                    self.highlight_color = arcade.color.WHITE
                    self.highlighted_square = None
                    self.game.computer_player_move()
                else:
                    self.highlight_square(start_row, start_col, arcade.color.RED, 0.5)
            else:
                self.selected_piece = (row, col)
                self.highlight_square(row, col, arcade.color.YELLOW)


def main():
    game = Game()  # Initialize game logic
    my_game_window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, game)
    my_game_window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
