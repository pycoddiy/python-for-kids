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
WINDOW_TITLE = "Sprite Collision Detection - Collect Mushrooms"

# Sprite scaling factors
CHARACTER_SCALING = 0.05  # Make character smaller
MUSHROOM_SCALING = 0.015   # Make mushrooms smaller

# Movement speed
MOVEMENT_SPEED = 5

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
        
        # Draw instructions
        arcade.draw_text("Use WASD or Arrow Keys to move", 10, WINDOW_HEIGHT - 80, 
                        arcade.color.WHITE, 16)
        arcade.draw_text("Collect all mushrooms! Press SPACE to add more", 10, WINDOW_HEIGHT - 100, 
                        arcade.color.WHITE, 16)

    def on_update(self, delta_time):
        """Movement and game logic."""
        
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

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        
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

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False


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
