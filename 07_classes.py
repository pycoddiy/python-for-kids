"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Object-Oriented Programming with Classes"

CHARACTER_SIZE = 30
FOOD_SIZE = 20
INITIAL_SQUARE_COUNT = 5


class Character:
    """Class to represent the player ball."""

    def __init__(self, x=100, y=100, size=CHARACTER_SIZE, color=arcade.color.AERO_BLUE):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    
    def update(self, key_pressed):
        """Update ball position based on key input."""
        if key_pressed == arcade.key.W or key_pressed == arcade.key.UP:
            self.y += 10
        elif key_pressed == arcade.key.S or key_pressed == arcade.key.DOWN:
            self.y -= 10
        elif key_pressed == arcade.key.A or key_pressed == arcade.key.LEFT:
            self.x -= 10
        elif key_pressed == arcade.key.D or key_pressed == arcade.key.RIGHT:
            self.x += 10
        
        # Keep the ball inside the window borders
        if self.x < 0:
            self.x = 0
        if self.x > WINDOW_WIDTH - self.size:
            self.x = WINDOW_WIDTH - self.size
        if self.y < 0:
            self.y = 0
        if self.y > WINDOW_HEIGHT - self.size:
            self.y = WINDOW_HEIGHT - self.size

    def draw(self):
        """Draw the ball."""
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.size, self.size, self.color)


class Food:
    """Class to represent a square object."""

    def __init__(self, x=None, y=None, size=FOOD_SIZE, color=None):
        # If no position provided, generate random position
        if x is None:
            self.x = random.randint(size, WINDOW_WIDTH - size)
        else:
            self.x = x
            
        if y is None:
            self.y = random.randint(size, WINDOW_HEIGHT - size)
        else:
            self.y = y
            
        self.size = size
        
        # If no color provided, choose random color
        if color is None:
            square_colors = [
                arcade.color.YELLOW,
                arcade.color.GOLD,
                arcade.color.ORANGE,
                arcade.color.WHITE,
                arcade.color.LIGHT_YELLOW
            ]
            self.color = random.choice(square_colors)
        else:
            self.color = color
    
    def draw(self):
        """Draw the square."""
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.size, self.size, self.color)


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.AMAZON
        self.key_pressed = None  # Track the currently pressed key

        # Create the player character
        self.character = Character()

        # List to store food objects
        self.food = []

        # Generate some initial food squares
        self.spawn_squares(INITIAL_SQUARE_COUNT)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def spawn_squares(self, count):
        """Spawn a specified number of square objects."""
        for _ in range(count):
            self.food.append(Food())

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

        # Draw all food items
        for food in self.food:
            food.draw()

        # Draw the player character
        self.character.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Update the character position based on key input
        self.character.update(self.key_pressed)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        self.key_pressed = key
        
        # Generate a food item when SPACE is pressed
        if key == arcade.key.SPACE:
            self.food.append(Food())

        # Clear all food items when C is pressed
        if key == arcade.key.C:
            self.food.clear()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == self.key_pressed:
            self.key_pressed = None

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