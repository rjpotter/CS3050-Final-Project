"""
Jack Mahoney, Ryan Potter, Ethan Rowland, Cooper Zion
Stratego: Graphics
CS 3050 - Software Engineering
3/6/2024
"""

import arcade
import arcade.gui
from enum import Enum

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Stratego"

TEXTURE_IMAGE_WIDTH = 1430  # the x width of the image of the pieces in pixels
TEXTURE_IMAGE_HEIGHT = 794  # the y height of the image of the pieces in pixels
PIECE_WIDTH = int(TEXTURE_IMAGE_WIDTH / 6)
PIECE_HEIGHT = int(TEXTURE_IMAGE_HEIGHT / 2)

REG_OUTLINE = arcade.color.BLACK
HIGHLIGHT_OUTLINE = arcade.color.RED
LAKE_COLOR = arcade.color.SILVER_LAKE_BLUE
BACKGROUND = arcade.color.AUROMETALSAURUS
BOARD = arcade.color.FERN_GREEN
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20


# index map for pieces and their textures
# Pieces:        | 10 | 9 | 8 | 7| 6| -1 (flag) | 5 | 4 | 3 | 2 | 1  | 11 (bomb) |
# Texture index: | 0  | 1 | 2 | 3| 4| 5         | 6 | 7 | 8 | 9 | 10 | 11        |


class GameState(Enum):
    RULES = -1
    INTRO = 0
    SETUP = 1
    PLAYING = 2
    WAITING = 3
    OVER = 4


class Piece:
    def __init__(self, value, color, sprite_index):
        self.color = color
        self.value = value
        self.sprite_index = sprite_index


class MyGame(arcade.Window):
    """
    Graphics application class
    """

    def __init__(self, width, height, title):
        super().__init__(int(width / 1.5), int(height / 1.5), title, resizable=True)

        arcade.set_background_color(BACKGROUND)

        # If we have sprite lists, we should create them here,
        # and set them to None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        self.red_pieces = []
        self.blue_pieces = []

        self.red_sprites = arcade.SpriteList()
        self.blue_sprites = arcade.SpriteList()

        red_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "font_weight": "Bold",
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.BARN_RED,
        }

        start_button = arcade.gui.UIFlatButton(text="Click Here or Press Space Start", width=400, height=100,
                                               style=red_style)
        start_button.on_click = self.on_start_button_click
        self.v_box.add(start_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        self.held_piece = None

        self.screen_width = width
        self.screen_height = height

        self.size_board = width if width < height else height
        self.size_square = int(self.size_board / 10)

        self.game_state = GameState.INTRO

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        self.screen_width = width
        self.screen_height = height
        self.size_board = width if width < height else height
        self.size_square = int(self.size_board / 10)
        super().on_resize(width, height)

    def setup(self):
        """
        Set up the game variables. Call to re-start the game.
        """
        # Create the list of coordinates to make the textures of the pieces
        # format is x, y, width, height. 0,0 is the top left of the image, positive x is right, positive y is down
        self.game_state = GameState.INTRO

        texture_map_cords = []
        for ii in range(2):
            for jj in range(6):
                texture_map_cords.append([PIECE_WIDTH * jj, PIECE_HEIGHT * ii, PIECE_WIDTH, PIECE_HEIGHT])

        # Create sprites and sprite lists here
        red_piece_textures = arcade.load_textures(
            "img/red_pieces.png",
            texture_map_cords,
            False,
            False,
            "Simple",
            4.5
        )

        blue_piece_textures = arcade.load_textures(
            "img/blue_pieces.png",  # filename
            texture_map_cords,
            False,
            False,
            "Simple",
            4.5
        )

        # 80 total pieces, 40 for each player
        # 1 Marshal
        sprite = arcade.Sprite(texture=red_piece_textures[0], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(10, "red", 0))

        # 1 General
        sprite = arcade.Sprite(texture=red_piece_textures[1], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(9, "red", 1))

        # 2 Colonels
        sprite = arcade.Sprite(texture=red_piece_textures[2], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(8, "red", 2))
        sprite = arcade.Sprite(texture=red_piece_textures[2], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(8, "red", 3))

        # 3 Majors
        sprite = arcade.Sprite(texture=red_piece_textures[3], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(7, "red", 4))
        sprite = arcade.Sprite(texture=red_piece_textures[3], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(7, "red", 5))
        sprite = arcade.Sprite(texture=red_piece_textures[3], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(7, "red", 6))

        # 4 Captains
        sprite = arcade.Sprite(texture=red_piece_textures[4], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(6, "red", 7))
        sprite = arcade.Sprite(texture=red_piece_textures[4], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(6, "red", 8))
        sprite = arcade.Sprite(texture=red_piece_textures[4], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(6, "red", 9))
        sprite = arcade.Sprite(texture=red_piece_textures[4], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(6, "red", 10))

        # 4 Lieutenants
        sprite = arcade.Sprite(texture=red_piece_textures[6], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(5, "red", 11))
        sprite = arcade.Sprite(texture=red_piece_textures[6], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(5, "red", 12))
        sprite = arcade.Sprite(texture=red_piece_textures[6], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(5, "red", 13))
        sprite = arcade.Sprite(texture=red_piece_textures[6], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(5, "red", 14))

        # 4 Sergeants
        sprite = arcade.Sprite(texture=red_piece_textures[7], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(4, "red", 15))
        sprite = arcade.Sprite(texture=red_piece_textures[7], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(4, "red", 16))
        sprite = arcade.Sprite(texture=red_piece_textures[7], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(4, "red", 17))
        sprite = arcade.Sprite(texture=red_piece_textures[7], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(4, "red", 18))

        # 5 Miners
        sprite = arcade.Sprite(texture=red_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(3, "red", 19))
        sprite = arcade.Sprite(texture=red_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(3, "red", 20))
        sprite = arcade.Sprite(texture=red_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(3, "red", 21))
        sprite = arcade.Sprite(texture=red_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(3, "red", 22))
        sprite = arcade.Sprite(texture=red_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(3, "red", 23))

        # 8 Scouts
        sprite = arcade.Sprite(texture=red_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(2, "red", 24))
        sprite = arcade.Sprite(texture=red_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(2, "red", 25))
        sprite = arcade.Sprite(texture=red_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(2, "red", 26))
        sprite = arcade.Sprite(texture=red_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(2, "red", 27))
        sprite = arcade.Sprite(texture=red_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(2, "red", 28))
        sprite = arcade.Sprite(texture=red_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(2, "red", 29))
        sprite = arcade.Sprite(texture=red_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(2, "red", 30))
        sprite = arcade.Sprite(texture=red_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(2, "red", 31))

        # 1 Spy
        sprite = arcade.Sprite(texture=red_piece_textures[10], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(1, "red", 32))

        # 1 Flag
        sprite = arcade.Sprite(texture=red_piece_textures[5], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(-1, "red", 33))

        # 6 Bombs
        sprite = arcade.Sprite(texture=red_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(11, "red", 34))
        sprite = arcade.Sprite(texture=red_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(11, "red", 35))
        sprite = arcade.Sprite(texture=red_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(11, "red", 36))
        sprite = arcade.Sprite(texture=red_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(11, "red", 37))
        sprite = arcade.Sprite(texture=red_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(11, "red", 38))
        sprite = arcade.Sprite(texture=red_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.red_sprites.append(sprite)
        self.red_pieces.append(Piece(11, "red", 39))

        # Blue pieces
        # 1 Marshal
        sprite = arcade.Sprite(texture=blue_piece_textures[0], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(10, "blue", 0))

        # 1 General
        sprite = arcade.Sprite(texture=blue_piece_textures[1], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(9, "blue", 1))

        # 2 Colonels
        sprite = arcade.Sprite(texture=blue_piece_textures[2], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(8, "blue", 2))
        sprite = arcade.Sprite(texture=blue_piece_textures[2], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(8, "blue", 3))

        # 3 Majors
        sprite = arcade.Sprite(texture=blue_piece_textures[3], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(7, "blue", 4))
        sprite = arcade.Sprite(texture=blue_piece_textures[3], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(7, "blue", 5))
        sprite = arcade.Sprite(texture=blue_piece_textures[3], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(7, "blue", 6))

        # 4 Captains
        sprite = arcade.Sprite(texture=blue_piece_textures[4], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(6, "blue", 7))
        sprite = arcade.Sprite(texture=blue_piece_textures[4], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(6, "blue", 8))
        sprite = arcade.Sprite(texture=blue_piece_textures[4], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(6, "blue", 9))
        sprite = arcade.Sprite(texture=blue_piece_textures[4], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(6, "blue", 10))

        # 4 Lieutenants
        sprite = arcade.Sprite(texture=blue_piece_textures[6], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(5, "blue", 11))
        sprite = arcade.Sprite(texture=blue_piece_textures[6], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(5, "blue", 12))
        sprite = arcade.Sprite(texture=blue_piece_textures[6], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(5, "blue", 13))
        sprite = arcade.Sprite(texture=blue_piece_textures[6], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(5, "blue", 14))

        # 4 Sergeants
        sprite = arcade.Sprite(texture=blue_piece_textures[7], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(4, "blue", 15))
        sprite = arcade.Sprite(texture=blue_piece_textures[7], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(4, "blue", 16))
        sprite = arcade.Sprite(texture=blue_piece_textures[7], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(4, "blue", 17))
        sprite = arcade.Sprite(texture=blue_piece_textures[7], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(4, "blue", 18))

        # 5 Miners
        sprite = arcade.Sprite(texture=blue_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(3, "blue", 19))
        sprite = arcade.Sprite(texture=blue_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(3, "blue", 20))
        sprite = arcade.Sprite(texture=blue_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(3, "blue", 21))
        sprite = arcade.Sprite(texture=blue_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(3, "blue", 22))
        sprite = arcade.Sprite(texture=blue_piece_textures[8], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(3, "blue", 23))

        # 8 Scouts
        sprite = arcade.Sprite(texture=blue_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(2, "blue", 24))
        sprite = arcade.Sprite(texture=blue_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(2, "blue", 25))
        sprite = arcade.Sprite(texture=blue_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(2, "blue", 26))
        sprite = arcade.Sprite(texture=blue_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(2, "blue", 27))
        sprite = arcade.Sprite(texture=blue_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(2, "blue", 28))
        sprite = arcade.Sprite(texture=blue_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(2, "blue", 29))
        sprite = arcade.Sprite(texture=blue_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(2, "blue", 30))
        sprite = arcade.Sprite(texture=blue_piece_textures[9], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(2, "blue", 31))

        # 1 Spy
        sprite = arcade.Sprite(texture=blue_piece_textures[10], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(1, "blue", 32))

        # 1 Flag
        sprite = arcade.Sprite(texture=blue_piece_textures[5], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(-1, "blue", 33))

        # 6 Bombs
        sprite = arcade.Sprite(texture=blue_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(11, "blue", 34))
        sprite = arcade.Sprite(texture=blue_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(11, "blue", 35))
        sprite = arcade.Sprite(texture=blue_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(11, "blue", 36))
        sprite = arcade.Sprite(texture=blue_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(11, "blue", 37))
        sprite = arcade.Sprite(texture=blue_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(11, "blue", 38))
        sprite = arcade.Sprite(texture=blue_piece_textures[11], center_x=self.width / 2, center_y=self.height / 2)
        self.blue_sprites.append(sprite)
        self.blue_pieces.append(Piece(11, "blue", 39))

        for ii in range(10):
            for jj in range(4):
                self.red_sprites[jj * 10 + ii].center_x += (PIECE_WIDTH / 4) * ii
                self.red_sprites[jj * 10 + ii].center_y += jj * PIECE_HEIGHT / 4
                self.red_sprites[jj * 10 + ii].scale = 0.25
                self.blue_sprites[jj * 10 + ii].center_x += (PIECE_WIDTH / 4) * ii - 600
                self.blue_sprites[jj * 10 + ii].center_y += jj * PIECE_HEIGHT / 4
                self.blue_sprites[jj * 10 + ii].scale = 0.25

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        arcade.start_render()

        match self.game_state:
            case GameState.INTRO:
                # Set a themed background
                arcade.set_background_color(arcade.color.DARK_GREEN)

                # Centering calculations for text
                start_x = (self.screen_width / 2)
                start_y = self.screen_height - DEFAULT_LINE_HEIGHT * 3
                anchor_x = 'center'

                # Draw game title with a shadow effect for depth
                arcade.draw_text("STRATEGO", start_x + 2, start_y - 2,
                                 arcade.color.BLACK, 100,
                                 font_name="Kenney Mini Square", anchor_x=anchor_x)
                arcade.draw_text("STRATEGO", start_x, start_y,
                                 arcade.color.BARN_RED, 100, bold=True,
                                 font_name="Kenney Mini Square", anchor_x=anchor_x)

                # Draw decorative elements
                # Place flags at top corners
                # Unicode character for a flag
                flag_symbol = "⚑"

                # Top left corner
                arcade.draw_text(flag_symbol, self.screen_width * 0.1, self.screen_height * 0.8, arcade.color.RED, 100,
                                 anchor_x="center")
                # Top right corner
                arcade.draw_text(flag_symbol, self.screen_width * 0.9, self.screen_height * 0.8, arcade.color.BLUE, 100,
                                 anchor_x="center")

                # Credits at the bottom
                credits_text = "Developed by: Jack Mahoney, Ryan Potter, Ethan Rowland, Cooper Zion"
                arcade.draw_text(credits_text, self.screen_width / 2, 30,
                                 arcade.color.LIGHT_GRAY, 12, anchor_x="center", anchor_y="center")

                # Render UI elements
                self.manager.draw()

            case GameState.RULES:
                # Centering calculations for text
                start_x = (self.screen_width / 2)
                start_y = self.screen_height * 0.9
                anchor_x = 'center'

                # Draw game title with a shadow effect for depth
                arcade.draw_text("STRATEGO", start_x + 2, start_y - 2,
                                 arcade.color.BLACK, 50,
                                 font_name="Kenney Mini Square", anchor_x=anchor_x)
                arcade.draw_text("STRATEGO", start_x, start_y,
                                 arcade.color.BARN_RED, 50, bold=True,
                                 font_name="Kenney Mini Square", anchor_x=anchor_x)

                # Draw decorative elements
                # Place flags at top corners
                # Unicode character for a flag
                flag_symbol = "⚑"

                # Top left corner
                arcade.draw_text(flag_symbol, self.screen_width * 0.3, self.screen_height * 0.9, arcade.color.RED, 50,
                                 anchor_x="center")
                # Top right corner
                arcade.draw_text(flag_symbol, self.screen_width * 0.7, self.screen_height * 0.9, arcade.color.BLUE, 50,
                                 anchor_x="center")

                # Columns setup
                column1_start_x = self.screen_width * 0.35
                column2_start_x = self.screen_width * 0.4
                row_start_y = self.screen_height * 0.8
                line_height = 30

                # Define the pieces and their descriptions or actions
                game_elements = {
                    "Piece, Rank": "Description",
                    "Marshal, 1": "Highest rank but defeated by the Spy",
                    "General, 2": "Normal Piece",
                    "Colonel, 3": "Normal Piece",
                    "Major, 4": "Normal Piece",
                    "Captain, 5": "Normal Piece",
                    "Lieutenant, 6": "Normal Piece",
                    "Sergent, 7": "Normal Piece",
                    "Miner, 8": "Only piece that can defuse bombs",
                    "Scout, 9": "Can move any number of spaces in a straight line",
                    "Flag, F": "Can be captured but cannot move",
                    "Spy, S": "Can defeat the Marshal or be defeated by any other",
                    "Bomb, B": "Destroys any attacker except the Miner",
                    "": "",
                    "Keybind": "Description",
                    "ESC": "Quit Game",
                    "\\": "View the rules",
                    "SPACE": "Continue to setup",
                    "ENTER": "Continue to playing",
                }

                # Draw the columns
                for key, value in game_elements.items():
                    arcade.draw_text(key, column1_start_x, row_start_y, arcade.color.WHITE, 20, anchor_x="right")
                    arcade.draw_text(value, column2_start_x, row_start_y, arcade.color.LIGHT_GRAY, 20, anchor_x="left")
                    row_start_y -= line_height  # Move to the next line

                pass
            case GameState.SETUP:
                # Centering calculations for text
                start_x = (self.screen_width / 2)
                start_y = self.screen_height - DEFAULT_LINE_HEIGHT * 3
                anchor_x = 'center'
                arcade.draw_text("Setup Page", start_x + 2, start_y - 2,
                                 arcade.color.BLACK, 50,
                                 font_name="Kenney Mini Square", anchor_x=anchor_x)
                # TODO: LOW PRIORITY: build setup sidebar?
                pass
            case GameState.WAITING:
                # unneeded?
                for ii in range(10):
                    for jj in range(10):
                        x = (ii * self.size_square + self.size_square // 2) + (
                            (self.width / 2 - (5 * self.size_square)) if self.width > self.height else 0)
                        y = ((jj * self.size_square) + self.size_square // 2) + (
                            (self.height / 2 - (5 * self.size_square)) if self.height > self.width else 0)

                        if jj < 4:
                            self.red_sprites[jj * 10 + ii].center_x = x
                            self.red_sprites[jj * 10 + ii].center_y = y
                            self.red_sprites[jj * 10 + ii].scale = 0.00014 * max(self.width, self.height)
                        if jj > 5:
                            self.blue_sprites[(jj - 6) * 10 + ii].center_x = x
                            self.blue_sprites[(jj - 6) * 10 + ii].center_y = y
                            self.blue_sprites[(jj - 6) * 10 + ii].scale = 0.00014 * max(self.width, self.height)

                        if (ii == 2 or ii == 3 or ii == 6 or ii == 7) and (jj == 4 or jj == 5):
                            arcade.draw_rectangle_filled(x, y, self.size_square, self.size_square, LAKE_COLOR)
                        else:
                            arcade.draw_rectangle_filled(x, y, self.size_square, self.size_square, BOARD)
                        arcade.draw_rectangle_outline(x, y, self.size_square, self.size_square, REG_OUTLINE, 2)

                        self.blue_sprites.draw()
                        self.red_sprites.draw()
                pass
            case GameState.PLAYING:
                for ii in range(10):
                    for jj in range(10):
                        x = (ii * self.size_square + self.size_square // 2) + (
                            (self.width / 2 - (5 * self.size_square)) if self.width > self.height else 0)
                        y = ((jj * self.size_square) + self.size_square // 2) + (
                            (self.height / 2 - (5 * self.size_square)) if self.height > self.width else 0)

                        if jj < 4:
                            self.red_sprites[jj * 10 + ii].center_x = x
                            self.red_sprites[jj * 10 + ii].center_y = y
                            self.red_sprites[jj * 10 + ii].scale = 0.00014 * max(self.width, self.height)
                        if jj > 5:
                            self.blue_sprites[(jj - 6) * 10 + ii].center_x = x
                            self.blue_sprites[(jj - 6) * 10 + ii].center_y = y
                            self.blue_sprites[(jj - 6) * 10 + ii].scale = 0.00014 * max(self.width, self.height)

                        if (ii == 2 or ii == 3 or ii == 6 or ii == 7) and (jj == 4 or jj == 5):
                            arcade.draw_rectangle_filled(x, y, self.size_square, self.size_square, LAKE_COLOR)
                        else:
                            arcade.draw_rectangle_filled(x, y, self.size_square, self.size_square, BOARD)
                        arcade.draw_rectangle_outline(x, y, self.size_square, self.size_square, REG_OUTLINE, 2)

                        self.blue_sprites.draw()
                        self.red_sprites.draw()
            case GameState.OVER:
                # TODO: Add over screen
                pass

    def on_update(self, delta_time):
        """
        All the logic for moving and the game logic goes here.
        Call update() on the sprite lists that need it.
        """

        # case waiting, get computer move from backend
        # case playing, proces registered user moves

        pass

    def on_start_button_click(self, event):
        self.game_state = GameState.RULES

    def on_rules_button_click(self, event):
        self.game_state = GameState.SETUP

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # Escape
        if key == 65307:
            arcade.close_window()
        # Ctrl + R
        elif key == 114 and key_modifiers == 2:
            self.setup()

        match self.game_state:
            case GameState.INTRO:
                # Space
                if key == 32:
                    self.game_state = GameState.RULES
            case GameState.RULES:
                # Space
                if key == 32:
                    self.game_state = GameState.SETUP
                # Enter
                if key == 65293:
                    self.game_state = GameState.PLAYING
            case GameState.SETUP:
                # Enter
                if key == 65293:
                    self.game_state = GameState.PLAYING
                # \
                if key == 92:
                    self.game_state = GameState.RULES
            case GameState.PLAYING:
                # \
                if key == 92:
                    self.game_state = GameState.RULES


    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        match self.GameState:
            case GameState.PLAYING:
                piece = arcade.get_sprites_at_point((x, y), self.red_sprites)
                if piece is not None:
                    self.held_piece = piece

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        match self.GameState:
            case GameState.PLAYING:
                if self.held_piece is not None:
                    if arcade.get_sprites_at_point((x, y), self.blue_sprites) is not None:
                        attack_target_sprite = arcade.get_sprites_at_point((x, y), self.blue_sprites)
                    # elif arcade.get_sprites_at_point((x, y), self.red_sprites) is None and :


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()