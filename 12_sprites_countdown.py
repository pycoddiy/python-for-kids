"""
Sprite Collision Detection

A collision detection game using arcade sprites.
The player controls a ball sprite and collects mushroom sprites.

If Python and Arcade are installed, this example can be run from the command line with:
python 11_sprite_collision.py
"""
import arcade
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Sprite Collision with Countdown - Collect Mushrooms in 60 Seconds"

# Sprite scaling factors
CHARACTER_SCALING = 0.05  # Make character smaller
MUSHROOM_SCALING = 0.015   # Make mushrooms smaller

# Movement speed
MOVEMENT_SPEED = 5

# Game duration
GAME_DURATION = 60.0  # Game duration in seconds (1 minute)

# Global texture cache - load textures once and reuse them
TEXTURES = {}

def load_textures():
    """Load all textures once at startup."""
    global TEXTURES
    TEXTURES["character"] = arcade.load_texture("assets/ball.png")
    TEXTURES["mushroom"] = arcade.load_texture("assets/05.png")


class CharacterSprite(arcade.Sprite):
    """Player character sprite class."""
    
    def __init__(self):
        super().__init__()
        
        # Use pre-loaded texture
        self.texture = TEXTURES["character"]
        self.scale = CHARACTER_SCALING
    
    def update(self, delta_time=None):
        """Update the sprite position."""
        # Call the parent update to handle movement
        super().update(delta_time=delta_time)
        
        # Keep the sprite on screen
        if self.left < 0:
            self.left = 0
        elif self.right > WINDOW_WIDTH:
            self.right = WINDOW_WIDTH
            
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > WINDOW_HEIGHT:
            self.top = WINDOW_HEIGHT


class MushroomSprite(arcade.Sprite):
    """Mushroom food sprite class."""
    
    def __init__(self):
        super().__init__()
        
        # Use pre-loaded texture
        self.texture = TEXTURES["mushroom"]
        self.scale = MUSHROOM_SCALING
        
        # Set random position
        self.center_x = random.randint(50, WINDOW_WIDTH - 50)
        self.center_y = random.randint(50, WINDOW_HEIGHT - 50)


class GameView(arcade.View):
    """
    Main game class using sprites.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.AMAZON

        # Game score
        self.score = 0

        # Countdown timer
        self.time_remaining = GAME_DURATION
        self.game_over = False

        # Sprite lists
        self.player_list = None
        self.mushroom_list = None
        
        # Player sprite
        self.player_sprite = None
        
        # Track keys for movement
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        """Set up the game and initialize variables."""
        
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.mushroom_list = arcade.SpriteList()
        
        # Create player sprite
        self.player_sprite = CharacterSprite()
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)
        
        # Create mushroom sprites
        for _ in range(5):
            mushroom = MushroomSprite()
            self.mushroom_list.append(mushroom)

    def on_draw(self):
        """Render the screen."""
        
        # Clear the screen
        self.clear()
        
        # Draw all sprite lists
        self.mushroom_list.draw()
        self.player_list.draw()
        
        # Draw the score
        arcade.draw_text(f"Score: {self.score}", 10, WINDOW_HEIGHT - 40, 
                        arcade.color.WHITE, 24)

        # Draw the countdown timer
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(time_text, 10, WINDOW_HEIGHT - 80, 
                        arcade.color.WHITE, 24)
        
        # Draw instructions
        arcade.draw_text("Use WASD or Arrow Keys to move", 10, WINDOW_HEIGHT - 120, 
                        arcade.color.WHITE, 16)
        arcade.draw_text("Collect all mushrooms! Press SPACE to add more", 10, WINDOW_HEIGHT - 140, 
                        arcade.color.WHITE, 16)

        # Draw game over message if time is up
        if self.game_over:
            # Draw semi-transparent black overlay covering the entire screen
            arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))
            
            # Draw game over text
            arcade.draw_text("GAME OVER!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                           arcade.color.RED, 48, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                           arcade.color.WHITE, 32, anchor_x="center")
            arcade.draw_text("Press R to restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
                           arcade.color.WHITE, 24, anchor_x="center")

    def on_update(self, delta_time):
        """Movement and game logic."""
        
        # Only update game logic if game is not over
        if not self.game_over:
            # Update countdown timer
            self.time_remaining -= delta_time
            
            # Check if time is up
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                return  # Stop updating game logic
            
            # Calculate movement based on key presses
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif self.right_pressed and not self.left_pressed:
                self.player_sprite.change_x = MOVEMENT_SPEED
                
            if self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif self.down_pressed and not self.up_pressed:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            
            # Update sprites
            self.player_list.update()
            
            # Check for collisions between player and mushrooms
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.mushroom_list)
            
            # Process collisions
            for mushroom in hit_list:
                # Remove the mushroom
                mushroom.remove_from_sprite_lists()
                # Increase score
                self.score += 1
            
            # Spawn new mushrooms if all are collected
            if len(self.mushroom_list) == 0:
                for _ in range(5):
                    mushroom = MushroomSprite()
                    self.mushroom_list.append(mushroom)
        if len(self.mushroom_list) == 0:
            for _ in range(5):
                mushroom = MushroomSprite()
                self.mushroom_list.append(mushroom)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        
        # Movement keys (only work if game is not over)
        if not self.game_over:
            if key == arcade.key.UP or key == arcade.key.W:
                self.up_pressed = True
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.down_pressed = True
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.left_pressed = True
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.right_pressed = True
            elif key == arcade.key.SPACE:
                # Add a new mushroom
                mushroom = MushroomSprite()
                self.mushroom_list.append(mushroom)
        
        # Reset game (works anytime)
        if key == arcade.key.R:
            self.reset_game()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        
        # Only handle key release if game is not over
        if not self.game_over:
            if key == arcade.key.UP or key == arcade.key.W:
                self.up_pressed = False
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.down_pressed = False
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.left_pressed = False
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.right_pressed = False

    def reset_game(self):
        """Reset the game to initial state."""
        # Reset score and timer
        self.score = 0
        self.time_remaining = GAME_DURATION
        self.game_over = False
        
        # Reset key states
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        
        # Reset player position
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        
        # Clear and recreate mushrooms
        self.mushroom_list.clear()
        for _ in range(5):
            mushroom = MushroomSprite()
            self.mushroom_list.append(mushroom)


def main():
    """Main function"""
    # Load all textures once at startup
    load_textures()
    
    # Create a window
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the game view
    game_view = GameView()
    window.show_view(game_view)
    game_view.setup()

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
