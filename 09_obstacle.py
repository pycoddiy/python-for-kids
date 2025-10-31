"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Starting Template"

SCREEN_BOTTOM = 50
GRAVITY = 200
JUMP_SPEED = 200
BONUS_ACCELERATIONS = 2

OBSTACLE_TIME_DELTA = 2.0  # Time in seconds between obstacles

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

        self.player_sprite = arcade.Sprite("./assets/ball.png", scale=0.05)
        self.player_sprite.center_x = 150 
        self.player_sprite.center_y = WINDOW_HEIGHT // 2

        self.obstacles = arcade.SpriteList()
        for i in range(13):
            s = f"./assets/{i + 1:02d}.png"
            obstacle = arcade.Sprite(s, scale=0.04)
            obstacle.center_x = 100 + i * 90
            obstacle.center_y = SCREEN_BOTTOM + obstacle.height // 2 - 20
            self.obstacles.append(obstacle)

        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player_sprite)
        
        self.key_pressed = None  # Track the currently pressed key
        self.bonus_acceleration = 0

        self.speed = 0  # Vertical velocity

        self.obstacle_timer = 0.0  # Timer to track obstacle spawning
        self.obstacle_x_position = WINDOW_WIDTH  # Initial x position for obstacles

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
        arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, SCREEN_BOTTOM, arcade.color.DARK_BROWN)
        self.all_sprites.draw()
        self.obstacles.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.key_pressed == arcade.key.W or self.key_pressed == arcade.key.UP:
            if self.player_sprite.center_y <= SCREEN_BOTTOM + self.player_sprite.height // 2 + 5:
                self.bonus_acceleration = 0  # Reset bonus acceleration when on the ground
                
            if self.bonus_acceleration < BONUS_ACCELERATIONS:
                self.bonus_acceleration += 1
                self.speed = JUMP_SPEED
                self.key_pressed = None  # Reset key to avoid continuous jumping

        # Update sprite positions
        self.player_sprite.center_y += self.speed * delta_time

        # Update speed
        self.speed -= GRAVITY * delta_time

        # Keep the player inside the window borders
        if self.player_sprite.center_y < SCREEN_BOTTOM + self.player_sprite.height // 2:
            self.player_sprite.center_y = SCREEN_BOTTOM + self.player_sprite.height // 2
        if self.player_sprite.center_y > WINDOW_HEIGHT - self.player_sprite.height // 2:
            self.player_sprite.center_y = WINDOW_HEIGHT - self.player_sprite.height // 2

        

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        self.key_pressed = key

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