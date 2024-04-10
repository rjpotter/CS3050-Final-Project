"""
Jack Mahoney, Ryan Potter, Ethan Rowland, Cooper Zion
Stratego: Graphics
CS 3050 - Software Engineering
3/6/2024
"""

import arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Stratego"

TEXTURE_IMAGE_WIDTH = 1430  # the x width of the image of the pieces in pixels
TEXTURE_IMAGE_HEIGHT = 794  # the y height of the image of the pieces in pixels
PIECE_WIDTH = int(TEXTURE_IMAGE_WIDTH / 6)
PIECE_HEIGHT = int(TEXTURE_IMAGE_HEIGHT / 2)


# index map for pieces and their textures
# Pieces:        | 10 | 9 | 8 | 7| 6| -1 (flag) | 5 | 4 | 3 | 2 | 1  | 11 (bomb) |
# Texture index: | 0  | 1 | 2 | 3| 4| 5         | 6 | 7 | 8 | 9 | 10 | 11        |

class Piece:
    def __init__(self, value, color, texture: arcade.texture, x, y):
        self.color = color
        self.value = value
        self.texture = texture
        self.x = x
        self.y = y


class MyGame(arcade.Window):
    """
    Graphics application class
    """

    def __init__(self, width, height, title):
        super().__init__(int(width / 1.5), int(height / 1.5), title, resizable=True)

        arcade.set_background_color(arcade.color.BLACK)

        # If we have sprite lists, we should create them here,
        # and set them to None
        self.red_piece_textures = []
        self.blue_piece_textures = []

        self.red_pieces = []
        self.blue_pieces = []

        self.screen_width = width
        self.screen_height = height

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        self.screen_width = width
        self.screen_height = height
        super().on_resize(width, height)

    def setup(self):
        """
        Set up the game variables. Call to re-start the game.
        """
        # Create the list of coordinates to make the textures of the pieces
        # format is x, y, width, height. 0,0 is the top left of the image, positive x is right, positive y is down
        texture_map_cords = []
        for ii in range(2):
            for jj in range(6):
                texture_map_cords.append([PIECE_WIDTH * jj, PIECE_HEIGHT * ii, PIECE_WIDTH, PIECE_HEIGHT])

        # Create sprites and sprite lists here
        self.red_piece_textures = arcade.load_textures(
            "img/red_pieces.png",
            texture_map_cords,
            False,
            False,
            "Simple",
            4.5
        )

        # 40 total pieces for each player
        # 1 Marshal
        self.red_pieces.append(Piece(10, "red", self.red_piece_textures[0], self.width / 2, self.height / 2))
        # 1 General
        self.red_pieces.append(Piece(9, "red", self.red_piece_textures[1], self.width / 2, self.height / 2))
        # 2 Colonels
        self.red_pieces.append(Piece(8, "red", self.red_piece_textures[2], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(8, "red", self.red_piece_textures[2], self.width / 2, self.height / 2))
        # 3 Majors
        self.red_pieces.append(Piece(7, "red", self.red_piece_textures[3], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(7, "red", self.red_piece_textures[3], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(7, "red", self.red_piece_textures[3], self.width / 2, self.height / 2))
        # 4 Captains
        self.red_pieces.append(Piece(6, "red", self.red_piece_textures[4], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(6, "red", self.red_piece_textures[4], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(6, "red", self.red_piece_textures[4], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(6, "red", self.red_piece_textures[4], self.width / 2, self.height / 2))
        # 4 Lieutenants
        self.red_pieces.append(Piece(5, "red", self.red_piece_textures[6], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(5, "red", self.red_piece_textures[6], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(5, "red", self.red_piece_textures[6], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(5, "red", self.red_piece_textures[6], self.width / 2, self.height / 2))
        # 4 Sergeants
        self.red_pieces.append(Piece(4, "red", self.red_piece_textures[7], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(4, "red", self.red_piece_textures[7], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(4, "red", self.red_piece_textures[7], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(4, "red", self.red_piece_textures[7], self.width / 2, self.height / 2))
        # 5 Miners
        self.red_pieces.append(Piece(3, "red", self.red_piece_textures[8], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(3, "red", self.red_piece_textures[8], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(3, "red", self.red_piece_textures[8], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(3, "red", self.red_piece_textures[8], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(3, "red", self.red_piece_textures[8], self.width / 2, self.height / 2))
        # 8 Scouts
        self.red_pieces.append(Piece(2, "red", self.red_piece_textures[9], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(2, "red", self.red_piece_textures[9], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(2, "red", self.red_piece_textures[9], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(2, "red", self.red_piece_textures[9], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(2, "red", self.red_piece_textures[9], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(2, "red", self.red_piece_textures[9], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(2, "red", self.red_piece_textures[9], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(2, "red", self.red_piece_textures[9], self.width / 2, self.height / 2))
        # 1 Spy
        self.red_pieces.append(Piece(1, "red", self.red_piece_textures[10], self.width / 2, self.height / 2))
        # 1 Flag
        self.red_pieces.append(Piece(-1, "red", self.red_piece_textures[5], self.width / 2, self.height / 2))
        # 6 Bombs
        self.red_pieces.append(Piece(11, "red", self.red_piece_textures[11], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(11, "red", self.red_piece_textures[11], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(11, "red", self.red_piece_textures[11], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(11, "red", self.red_piece_textures[11], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(11, "red", self.red_piece_textures[11], self.width / 2, self.height / 2))
        self.red_pieces.append(Piece(11, "red", self.red_piece_textures[11], self.width / 2, self.height / 2))

        self.blue_piece_textures = arcade.load_textures(
            "img/blue_pieces.png",  # filename
            texture_map_cords,
            False,
            False,
            "Simple",
            4.5
        )

        # 1 Marshal
        self.blue_pieces.append(Piece(10, "blue", self.blue_piece_textures[0], self.width / 2, self.height / 2))
        # 1 General
        self.blue_pieces.append(Piece(9, "blue", self.blue_piece_textures[1], self.width / 2, self.height / 2))
        # 2 Colonels
        self.blue_pieces.append(Piece(8, "blue", self.blue_piece_textures[2], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(8, "blue", self.blue_piece_textures[2], self.width / 2, self.height / 2))
        # 3 Majors
        self.blue_pieces.append(Piece(7, "blue", self.blue_piece_textures[3], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(7, "blue", self.blue_piece_textures[3], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(7, "blue", self.blue_piece_textures[3], self.width / 2, self.height / 2))
        # 4 Captains
        self.blue_pieces.append(Piece(6, "blue", self.blue_piece_textures[4], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(6, "blue", self.blue_piece_textures[4], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(6, "blue", self.blue_piece_textures[4], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(6, "blue", self.blue_piece_textures[4], self.width / 2, self.height / 2))
        # 4 Lieutenants
        self.blue_pieces.append(Piece(5, "blue", self.blue_piece_textures[6], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(5, "blue", self.blue_piece_textures[6], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(5, "blue", self.blue_piece_textures[6], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(5, "blue", self.blue_piece_textures[6], self.width / 2, self.height / 2))
        # 4 Sergeants
        self.blue_pieces.append(Piece(4, "blue", self.blue_piece_textures[7], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(4, "blue", self.blue_piece_textures[7], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(4, "blue", self.blue_piece_textures[7], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(4, "blue", self.blue_piece_textures[7], self.width / 2, self.height / 2))
        # 5 Miners
        self.blue_pieces.append(Piece(3, "blue", self.blue_piece_textures[8], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(3, "blue", self.blue_piece_textures[8], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(3, "blue", self.blue_piece_textures[8], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(3, "blue", self.blue_piece_textures[8], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(3, "blue", self.blue_piece_textures[8], self.width / 2, self.height / 2))
        # 8 Scouts
        self.blue_pieces.append(Piece(2, "blue", self.blue_piece_textures[9], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(2, "blue", self.blue_piece_textures[9], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(2, "blue", self.blue_piece_textures[9], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(2, "blue", self.blue_piece_textures[9], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(2, "blue", self.blue_piece_textures[9], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(2, "blue", self.blue_piece_textures[9], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(2, "blue", self.blue_piece_textures[9], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(2, "blue", self.blue_piece_textures[9], self.width / 2, self.height / 2))
        # 1 Spy
        self.blue_pieces.append(Piece(1, "blue", self.blue_piece_textures[10], self.width / 2, self.height / 2))
        # 1 Flag
        self.blue_pieces.append(Piece(-1, "blue", self.blue_piece_textures[5], self.width / 2, self.height / 2))
        # 6 Bombs
        self.blue_pieces.append(Piece(11, "blue", self.blue_piece_textures[11], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(11, "blue", self.blue_piece_textures[11], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(11, "blue", self.blue_piece_textures[11], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(11, "blue", self.blue_piece_textures[11], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(11, "blue", self.blue_piece_textures[11], self.width / 2, self.height / 2))
        self.blue_pieces.append(Piece(11, "blue", self.blue_piece_textures[11], self.width / 2, self.height / 2))

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        jj = 0
        for ii in range(40):
            arcade.draw_texture_rectangle(
                # x, y, width, height, texture, angle, alpha
                self.red_pieces[ii].x + (PIECE_WIDTH / 4) * (ii % 10),
                self.red_pieces[ii].y + jj * (PIECE_HEIGHT / 4),
                PIECE_WIDTH / 4,
                PIECE_HEIGHT / 4,
                self.red_pieces[ii].texture,
                0,
                255
            )
            if ii % 10 == 9:
                jj += 1

        jj = 0
        for ii in range(40):
            arcade.draw_texture_rectangle(
                # x, y, width, height, texture, angle, alpha
                self.blue_pieces[ii].x + PIECE_WIDTH / 4 * (ii % 10) - 600,
                self.blue_pieces[ii].y + jj * PIECE_HEIGHT / 4,
                PIECE_WIDTH / 4,
                PIECE_HEIGHT / 4,
                self.blue_pieces[ii].texture,
                0,
                255
            )
            if ii % 10 == 9:
                jj += 1

    def on_update(self, delta_time):
        """
        All the logic for moving and the game logic goes here.
        Call update() on the sprite lists that need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == 65307:
            arcade.close_window()
        elif key == 114 and key_modifiers == 2:
            self.setup()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
