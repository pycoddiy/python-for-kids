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
WINDOW_TITLE = "Dynamic Obstacle Spawning"

SCREEN_BOTTOM = 50
GRAVITY = 200
JUMP_SPEED = 200
BONUS_ACCELERATIONS = 2

OBSTACLE_TIME_DELTA = 2.0  # Time in seconds between obstacles
OBSTACLE_SPEED = 100  # Speed at which obstacles move leftward

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BABY_BLUE_EYES

        self.player_sprite = arcade.Sprite("./assets/ball.png", scale=0.05)
        self.player_sprite.center_x = 150 
        self.player_sprite.center_y = WINDOW_HEIGHT // 2
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player_sprite)

        self.obstacle_textures = []
        for i in range(1, 14):
            self.obstacle_textures.append(arcade.load_texture(f"./assets/{i:02d}.png"))
        self.obstacle_timer = 0.0  # Timer to track obstacle spawning
        self.obstacle_sprites = arcade.SpriteList()

        self.key_pressed = None  # Track the currently pressed key
        self.bonus_acceleration = 0

        self.speed = 0  # Vertical velocity

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
        self.obstacle_sprites.draw()
        self.player_sprites.draw()

    def spawn_obstacle(self, delta_time):
        if self.obstacle_timer >= OBSTACLE_TIME_DELTA:
            self.obstacle_timer = 0.0  # Reset timer

            # Spawn a new obstacle
            obstacle_index = random.randint(0, len(self.obstacle_textures) - 1)
            obstacle = arcade.Sprite(self.obstacle_textures[obstacle_index], scale=0.04)
            obstacle.center_x = WINDOW_WIDTH + obstacle.width // 2
            obstacle.center_y = SCREEN_BOTTOM + obstacle.height // 2 - 20
            self.obstacle_sprites.append(obstacle)
        else:
            self.obstacle_timer += delta_time

    def move_obstacles(self, delta_time):
        for obstacle in self.obstacle_sprites:
            if obstacle.center_x < -obstacle.width // 2:
                self.obstacle_sprites.remove(obstacle)
            else:
                obstacle.center_x -= OBSTACLE_SPEED * delta_time

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

       # Handle obstacles
        self.spawn_obstacle(delta_time)
        self.move_obstacles(delta_time)

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