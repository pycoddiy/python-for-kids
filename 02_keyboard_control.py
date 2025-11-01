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
WINDOW_TITLE = "Keyboard Control Demo"

key_map = {
    arcade.key.W: "up",
    arcade.key.S: "down",
    arcade.key.A: "left",
    arcade.key.D: "right",
    arcade.key.UP: "up",
    arcade.key.DOWN: "down",
    arcade.key.LEFT: "left",
    arcade.key.RIGHT: "right",
}


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.message = "Press a key"
        self.background_color = arcade.color.AMAZON

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
        arcade.draw_text(self.message, 500, 500, arcade.color.BLACK, 24)

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
        if key  in (arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D, arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.message = f"You pressed a movement key {key_map[key]}!"  
        else:
            self.message = f"You pressed a non-movement key {key_map[key]}!"

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key in (arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D, arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.message = f"You released a movement key {key_map[key]}!"
        else:
            self.message = f"You released a non-movement key {key_map[key]}!"

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