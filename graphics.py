"""
Project by: Jack Mahoney, Ryan Potter, Ethan Rowland, Cooper Zion
Title: Stratego: Graphics
Course: CS 3050 - Software Engineering
Date: March 6, 2024
"""
import time

import arcade
from arcade import schedule
from classes import Game, Cell, Game_State

# Initialize screen dimensions and game title
MENU_BAR_HEIGHT = 50
SIDE_BAR_WIDTH = 50
TOTAL_SCREEN_WIDTH = 640 + (SIDE_BAR_WIDTH * 2)
TOTAL_SCREEN_HEIGHT = 640 + (MENU_BAR_HEIGHT * 2)
SCREEN_WIDTH = 640 #+ SIDE_BAR_WIDTH
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
        # Initialize turn tracker
        self.turn_tracker = 1
        self.play_again_button_x = TOTAL_SCREEN_WIDTH // 2
        self.play_again_button_y = TOTAL_SCREEN_HEIGHT // 2 - 75
        self.play_again_button_width = 200
        self.play_again_button_height = 50

    """
    def setup(self):
        # Calculate texture coordinates for slicing
        texture_map_cords = [
            [self.PIECE_WIDTH * jj, self.PIECE_HEIGHT * ii, self.PIECE_WIDTH, self.PIECE_HEIGHT]
            for ii in range(2) for jj in range(6)
        ]
        # Loading textures for pieces
        blue_textures = arcade.load_textures("img/blue_pieces.png", texture_map_cords, mirrored=False, flipped=False)
        red_textures = arcade.load_textures("img/red_pieces.png", texture_map_cords, mirrored=False, flipped=False)
    """

    def draw_board_pieces(self):
        # Drawing pieces on the board based on current game state
        for row in range(10):
            for col in range(10):
                cell = self.game.board[row][col]
                display_text = DISPLAY_DICT[cell]
                x = (col * SQUARE_SIZE + SQUARE_SIZE // 2) + SIDE_BAR_WIDTH
                y = (SCREEN_HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)) + MENU_BAR_HEIGHT
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
        arcade.draw_xywh_rectangle_filled(0, 0, TOTAL_SCREEN_WIDTH, TOTAL_SCREEN_HEIGHT, board_color)

        # Outlining board squares and drawing impassable terrain
        outline_color = arcade.color.BLACK
        for row in range(10):
            for col in range(10):
                x = (col * SQUARE_SIZE + SQUARE_SIZE // 2) + SIDE_BAR_WIDTH
                y = ((row * SQUARE_SIZE) + SQUARE_SIZE // 2) + MENU_BAR_HEIGHT
                arcade.draw_rectangle_outline(x, y, SQUARE_SIZE, SQUARE_SIZE, outline_color, 2)

        # Lake positions
        lake_color = arcade.color.AQUA
        lakes_positions = [(2, 4), (2, 5), (3, 4), (3, 5), (6, 4), (6, 5), (7, 4), (7, 5)]
        for pos in lakes_positions:
            x = (pos[0] * SQUARE_SIZE) + SIDE_BAR_WIDTH
            y = (pos[1] * SQUARE_SIZE) + MENU_BAR_HEIGHT
            arcade.draw_xywh_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, lake_color)

        # Red Menu Bar
        red_menu_color = arcade.color.RED
        arcade.draw_xywh_rectangle_filled(0, (TOTAL_SCREEN_HEIGHT - MENU_BAR_HEIGHT),
                                          TOTAL_SCREEN_WIDTH, MENU_BAR_HEIGHT, red_menu_color)

        # Blue Menu Bar
        blue_menu_color = arcade.color.BLUE
        arcade.draw_xywh_rectangle_filled(0, 0, TOTAL_SCREEN_WIDTH, MENU_BAR_HEIGHT, blue_menu_color)

        # Blue Team Side Bar
        blue_color = arcade.color.BLUE
        arcade.draw_xywh_rectangle_filled(0, 0, SIDE_BAR_WIDTH, (TOTAL_SCREEN_HEIGHT / 2), blue_color)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH + SIDE_BAR_WIDTH,
                                          0, SIDE_BAR_WIDTH, (TOTAL_SCREEN_HEIGHT / 2), blue_color)

        # Red Team Side Bar
        red_color = arcade.color.RED
        arcade.draw_xywh_rectangle_filled(0, (TOTAL_SCREEN_HEIGHT / 2),
                                          SIDE_BAR_WIDTH, (TOTAL_SCREEN_HEIGHT / 2), red_color)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH + SIDE_BAR_WIDTH,
                                          (TOTAL_SCREEN_HEIGHT / 2), SIDE_BAR_WIDTH, (TOTAL_SCREEN_HEIGHT / 2), red_color)

        # Displaying the turn tracker in the center of the Red Menu Bar
        current_player = "Player" if self.turn_tracker % 2 == 1 else "Computer"
        turn_text = f"Turn: {((self.turn_tracker + 1) // 2)} {current_player}"

        # Calculate the position for displaying the turn tracker text
        text_x = TOTAL_SCREEN_WIDTH / 2
        text_y = TOTAL_SCREEN_HEIGHT - MENU_BAR_HEIGHT / 2

        # Draw the turn tracker text
        arcade.draw_text(turn_text, text_x, text_y, arcade.color.WHITE, 14,
                         anchor_x="center", anchor_y="center")

        # Highlighting the selected square
        if self.highlighted_square:
            row, col = self.highlighted_square
            x = (col * SQUARE_SIZE + SQUARE_SIZE // 2) + SIDE_BAR_WIDTH
            y = (SCREEN_HEIGHT - (row * SQUARE_SIZE + (SQUARE_SIZE // 2))) + MENU_BAR_HEIGHT
            arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, self.highlight_color)
        # Drawing pieces on the board
        self.draw_board_pieces()

        # Draw the game over screen if the game state is not 'not_finished'
        if self.game.game_state != Game_State.not_finished:
            self.draw_game_over_screen()

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if the game is over and the "Play Again" button was clicked
        if (self.game.game_state != Game_State.not_finished and
                x > self.play_again_button_x - self.play_again_button_width // 2 and
                x < self.play_again_button_x + self.play_again_button_width // 2 and
                y > self.play_again_button_y - self.play_again_button_height // 2 and
                y < self.play_again_button_y + self.play_again_button_height // 2):
            self.reset_game()
            return
        # Handle piece selection and movement
        if button == arcade.MOUSE_BUTTON_LEFT:
            col = (x - SIDE_BAR_WIDTH) // SQUARE_SIZE
            row = 9 - ((y - MENU_BAR_HEIGHT) // SQUARE_SIZE)
            if self.selected_piece == (row, col):
                if (row, col) in self.game.human_player.troop_locations:
                    # Deselect the piece if it's already selected
                    self.selected_piece = None
                    self.highlight_color = arcade.color.WHITE
                    self.highlighted_square = None
                else:
                    self.highlight_square((row, col), arcade.color.RED, 0.5)

            elif self.selected_piece:
                start_row, start_col = self.selected_piece
                valid_move = self.game.human_player_move((start_row, start_col), (row, col))
                if valid_move:
                    # Move was valid, deselect the piece, and trigger computer move
                    self.selected_piece = None
                    self.highlight_color = arcade.color.WHITE
                    self.highlighted_square = None
                    self.turn_tracker += 1  # Advance turn after human move
                    self.game.computer_player_move()
                    self.turn_tracker += 1  # Advance turn after computer move
                else:
                    # Invalid move, highlight in red
                    self.highlight_square(start_row, start_col, arcade.color.RED, 0.5)
            else:
                if (row, col) in self.game.human_player.troop_locations:
                    # New piece selected
                    self.selected_piece = (row, col)
                    self.highlight_square(row, col, arcade.color.YELLOW)

    def advance_turn(self):
        """Advances to the next turn."""
        self.turn_tracker += 1


    def draw_game_over_screen(self):
        # Semi-transparent gray overlay
        game_over_overlay_color = (128, 128, 128, 128)  # RGBA for semi-transparent gray
        arcade.draw_xywh_rectangle_filled(0, 0, TOTAL_SCREEN_WIDTH, TOTAL_SCREEN_HEIGHT, game_over_overlay_color)

        # Determine win or loss
        if self.game.game_state == Game_State.capture_flag and self.game.last_human_move != (-1, -1):
            message = "YOU WIN!"
        else:
            message = "YOU LOST"

        # Display the message
        arcade.draw_text(message, TOTAL_SCREEN_WIDTH // 2, TOTAL_SCREEN_HEIGHT // 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")

        # Button dimensions and position
        arcade.draw_rectangle_filled(self.play_again_button_x, self.play_again_button_y,
                                     self.play_again_button_width, self.play_again_button_height,
                                     arcade.color.GRAY)
        arcade.draw_text("Play Again", self.play_again_button_x, self.play_again_button_y,
                         arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

    def reset_game(self):
        # Reinitialize the game logic
        self.game = Game()
        # Reset other necessary variables
        self.selected_piece = None
        self.turn_tracker = 1


def main():
    game = Game()  # Initialize game logic
    my_game_window = MyGame(TOTAL_SCREEN_WIDTH, TOTAL_SCREEN_HEIGHT, SCREEN_TITLE, game)
    #my_game_window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
