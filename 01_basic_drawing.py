"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Basic Drawing Shapes"


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = (150, 255, 150)  # My custom background color
        # If you have sprite lists, you should create them here,
        # and set them to None

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        arcade.draw_text("Hello, Arcade!", 500, 500, arcade.color.BLACK, 24)
        arcade.draw_circle_filled(300, 300, 50, arcade.color.AERO_BLUE)
        arcade.draw_lrbt_rectangle_filled(600, 700, 100, 200, arcade.color.ALMOND)
        arcade.draw_triangle_filled(800, 200, 900, 400, 700, 400, arcade.color.AMBER) # (x1, y1, x2, y2, x3, y3)
        arcade.draw_line(100, 100, 200, 200, arcade.color.AMETHYST, 5)
        arcade.draw_ellipse_filled(400, 100, 80, 40, arcade.color.ANDROID_GREEN)
        arcade.draw_polygon_filled([[100, 300], [150, 350], [200, 300], [175, 250], [125, 250]], arcade.color.ANTIQUE_BRONZE)
        arcade.draw_arc_filled(500, 300, 100, 50, arcade.color.AQUA, 0, 180) # (center_x, center_y, width, height, color, start_angle, end_angle)
        arcade.draw_parabola_filled(900, 100, 1000, 200, arcade.color.AQUAMARINE, 5) # (start_x, start_y, end_x, end_y, color, border_width)

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
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
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()