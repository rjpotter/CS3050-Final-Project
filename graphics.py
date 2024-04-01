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

TEXTURE_IMAGE_WIDTH = 1430   # the x width of the image of the pieces in pixels
TEXTURE_IMAGE_HEIGHT = 794   # the y height of the image of the pieces in pixels
PIECE_WIDTH = int(TEXTURE_IMAGE_WIDTH / 6)
PIECE_HEIGHT = int(TEXTURE_IMAGE_HEIGHT / 2)

# index map for pieces and their textures
# Pieces:        | 10 | 9 | 8 | 7| 6| flag | 5 | 4 | 3 | 2 | 1  | bomb |
# Texture index: | 0  | 1 | 2 | 3| 4| 5    | 6 | 7 | 8 | 9 | 10 | 11   |


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
        self.blue_piece_sprites = arcade.SpriteList()
        self.red_piece_sprites = arcade.SpriteList()

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
        self.blue_piece_textures = arcade.load_textures(
            "img/blue_pieces.png",     # filename
            texture_map_cords,
            False,
            False,
            "Simple",
            4.5
        )

        self.red_piece_textures = arcade.load_textures(
            "img/red_pieces.png",
            texture_map_cords,
            False,
            False,
            "Simple",
            4.5
        )

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        arcade.draw_texture_rectangle(
            # x, y, width, height, texture, angle, alpha
            500,     # random temp value
            500,     # random temp value
            PIECE_WIDTH * 2,
            PIECE_HEIGHT * 2,
            self.blue_piece_textures[0],
            0,
            255
        )

        # Call draw() on all the sprites here

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
        pass

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
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
