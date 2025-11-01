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
WINDOW_TITLE = "Collision Detection - Eat the Food Within 1 Minute"

CHARACTER_SIZE = 30
FOOD_SIZE = 20
GAME_DURATION = 60.0  # Game duration in seconds (1 minute)
INITIAL_FOOD_COUNT = 5


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

    def detect_collisions(self, food_list):
        """
        Detect collisions with food items.
        
        Args:
            food_list: List of Food objects to check for collisions
            
        Returns:
            List of Food objects that intersect with this character, or empty list if no collisions
        """
        collided_food = []
        
        for food in food_list:
            # Check if rectangles overlap using AABB (Axis-Aligned Bounding Box) collision detection
            # Character bounds (drawn from bottom-left corner)
            char_left = self.x
            char_right = self.x + self.size
            char_bottom = self.y
            char_top = self.y + self.size
            
            # Food bounds (also drawn from bottom-left corner)
            food_left = food.x
            food_right = food.x + food.size
            food_bottom = food.y
            food_top = food.y + food.size
            
            # Check for overlap - rectangles overlap if they overlap on both x and y axes
            if (char_left < food_right and 
                char_right > food_left and 
                char_bottom < food_top and 
                char_top > food_bottom):
                collided_food.append(food)
        
        return collided_food


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

        # Game score
        self.score = 0

        # Countdown timer
        self.time_remaining = GAME_DURATION
        self.game_over = False

        # Create the player character
        self.character = Character()

        # List to store food objects
        self.food = []

        # Generate some initial food squares
        self.spawn_food(INITIAL_FOOD_COUNT)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def spawn_food(self, count):
        """Spawn a specified number of food objects."""
        for _ in range(count):
            self.food.append(Food())

    def reset(self):
        """Reset the game to the initial state."""
        # Reset score
        self.score = 0
        
        # Reset timer
        self.time_remaining = GAME_DURATION
        self.game_over = False
        
        # Clear existing food and create new food items
        self.food.clear()
        self.spawn_food(INITIAL_FOOD_COUNT)
        
        # Reset character position
        self.character.x = 100
        self.character.y = 100

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

        # Draw the score
        arcade.draw_text(f"Score: {self.score}", 10, WINDOW_HEIGHT - 40, 
                        arcade.color.WHITE, 24)

        # Draw the countdown timer
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(time_text, 10, WINDOW_HEIGHT - 80, 
                        arcade.color.WHITE, 24)

        # Draw game over message if time is up
        if self.game_over:
            # Draw semi-transparent black overlay covering the entire screen
            # arcade.draw_lbwh_rectangle_filled(0, 0, 
                                    # WINDOW_WIDTH, WINDOW_HEIGHT, 
                                    # (0, 0, 0, 128))  # Black with 50% transparency

            arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))

            # Draw game over text
            arcade.draw_text("GAME OVER!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                           arcade.color.RED, 48, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                           arcade.color.WHITE, 32, anchor_x="center")
            arcade.draw_text("Press R to restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
                           arcade.color.WHITE, 24, anchor_x="center")

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Only update game logic if game is not over
        if not self.game_over:
            # Update countdown timer
            self.time_remaining -= delta_time
            
            # Check if time is up
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                return  # Stop updating game logic
            
            # Update the character position based on key input
            self.character.update(self.key_pressed)
            
            # Check for collisions with food
            collided_food = self.character.detect_collisions(self.food)
            
            # Process collisions: remove eaten food and update score
            for eaten_food in collided_food:
                if eaten_food in self.food:
                    self.food.remove(eaten_food)
                    self.score += 1  # Increment score for each food item eaten
            
            # Optionally: spawn new food when all food is eaten
            if len(self.food) == 0:
                # Spawn new food items
                self.spawn_food(INITIAL_FOOD_COUNT)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        self.key_pressed = key
        
        # Generate a food item when SPACE is pressed (only if game is not over)
        if key == arcade.key.SPACE and not self.game_over:
            self.food.append(Food())

        # Clear all food items when C is pressed (only if game is not over)
        if key == arcade.key.C and not self.game_over:
            self.food.clear()
        
        # Reset the game when R is pressed (works anytime)
        if key == arcade.key.R:
            self.reset()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # Only handle key release if game is not over
        if key == self.key_pressed and not self.game_over:
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