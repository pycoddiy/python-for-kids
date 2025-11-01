"""
Maze Navigation Game with Countdown

A maze navigation game using arcade sprites.
The player controls a ball sprite and navigates through a maze made of stone walls,
collecting mushroom food and finding the exit before time runs out.

If Python and Arcade are installed, this example can be run from the command line with:
python 13_maze.py
"""
import arcade
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Maze Navigation with Countdown - Collect Food and Find Exit"

# Sprite scaling factors
CHARACTER_SCALING = 0.02  # Make character smaller
STONE_SCALING = 0.01      # Make stone walls smaller
MUSHROOM_SCALING = 0.01   # Make mushrooms smaller

# Movement speed
MOVEMENT_SPEED = 3

# Game duration
GAME_DURATION = 60.0  # Game duration in seconds (1 minute)

# UI Panel configuration
PANEL_HEIGHT = 90  # Height of the bottom game panel (reduced)
MAZE_AREA_HEIGHT = WINDOW_HEIGHT - PANEL_HEIGHT  # Available height for maze

# Maze configuration
MAZE_WIDTH = 40   # Number of tiles horizontally
MAZE_HEIGHT = 22  # Number of tiles vertically
TILE_SIZE = 28    # Size of each maze tile in pixels (adjusted to fit screen)

# Maze layout - '#' represents walls (stones), ' ' represents open space, 'M' represents food (mushrooms), 'S' represents start, 'E' represents exit
MAZE_LAYOUT = """
########################################
#S M               #                   #
# #### ########### # ################# #
# #  # #         # # #  M            # #
# #  # # ####### # # # ############# # #
# #  # # #     # # # # #           # # #
# #  # # # ### # # # # # ######### # # #
# #  # # # # # # # # # # #       # # # #
# #  # #M# # # # # # # # # ##### # # # #
# #  # # # ### # # # # # # # #   # # # #
# #  # # #     # # # # # # # # ### # # #
# #  # ######### # # # # # # # #   # # #
# #  #             # # # # # # # ### # #
# #  ############# # # # # # # # #   # #
# #              # # # # # # # # ### # #
# # ############ # # # # # # # #   # # #
# # #M         # # # # # # # # ### # # #
# # ########## # # # # # # # #   # # # #
# #            #   #   #   #   #   #M# #
#  ############### # # # # # # ####### #
#                                     E#
########################################
"""

# Global texture cache - load textures once and reuse them
TEXTURES = {}

def load_textures():
    """Load all textures once at startup."""
    global TEXTURES
    TEXTURES["character"] = arcade.load_texture("assets/ball.png")
    TEXTURES["stone"] = arcade.load_texture("assets/04.png")
    TEXTURES["mushroom"] = arcade.load_texture("assets/05.png")
    TEXTURES["exit"] = arcade.load_texture("assets/06.png")


class StoneSprite(arcade.Sprite):
    """Stone wall sprite class."""
    
    def __init__(self):
        super().__init__()
        
        # Use pre-loaded texture
        self.texture = TEXTURES["stone"]
        self.scale = STONE_SCALING


class ExitSprite(arcade.Sprite):
    """Exit sprite class."""
    
    def __init__(self):
        super().__init__()
        
        # Use pre-loaded texture
        self.texture = TEXTURES["exit"]
        self.scale = STONE_SCALING


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
    Main game class for maze navigation.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BLACK

        # Game score
        self.score = 0

        # Countdown timer
        self.time_remaining = GAME_DURATION
        self.game_over = False

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.mushroom_list = None
        self.exit_list = None
        
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
        self.wall_list = arcade.SpriteList()
        self.mushroom_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()
        
        # Create the maze from the layout string
        self.create_maze()

    def create_maze(self):
        """Create maze walls, food, and exit from the layout string."""
        lines = MAZE_LAYOUT.strip().split('\n')
        
        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line):
                # Calculate position (offset maze to account for bottom panel)
                x = col_index * TILE_SIZE + TILE_SIZE // 2
                y = MAZE_AREA_HEIGHT - (row_index * TILE_SIZE + TILE_SIZE // 2) + PANEL_HEIGHT
                
                if char == '#':
                    # Create wall (stone) sprite
                    wall = StoneSprite()
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
                elif char == 'M':
                    # Create food (mushroom) sprite
                    mushroom = MushroomSprite()
                    mushroom.center_x = x
                    mushroom.center_y = y
                    self.mushroom_list.append(mushroom)
                elif char == 'S':
                    # Create player sprite at start position
                    self.player_sprite = CharacterSprite()
                    self.player_sprite.center_x = x
                    self.player_sprite.center_y = y
                    self.player_list.append(self.player_sprite)
                elif char == 'E':
                    # Create exit sprite
                    exit_sprite = ExitSprite()
                    exit_sprite.center_x = x
                    exit_sprite.center_y = y
                    self.exit_list.append(exit_sprite)

    def spawn_mushrooms(self, count):
        """Spawn a specified number of mushroom sprites."""
        for _ in range(count):
            mushroom = MushroomSprite()
            self.mushroom_list.append(mushroom)

    def on_draw(self):
        """Render the screen."""
        
        # Clear the screen
        self.clear()
        
        # Draw all sprite lists
        self.wall_list.draw()
        self.exit_list.draw()
        self.mushroom_list.draw()
        self.player_list.draw()
        
        # Draw the game panel at the bottom
        self.draw_game_panel()
        
        # Draw game over/victory overlays if needed
        self.draw_game_state_overlays()

    def draw_game_panel(self):
        """Draw the game information panel at the bottom of the screen."""
        # Draw panel background
        arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, PANEL_HEIGHT, (40, 40, 40))
        
        # Draw separator line
        arcade.draw_line(0, PANEL_HEIGHT, WINDOW_WIDTH, PANEL_HEIGHT, arcade.color.WHITE, 2)
        
        # Draw score (left side)
        arcade.draw_text(f"Score: {self.score}", 20, PANEL_HEIGHT - 35, 
                        arcade.color.WHITE, 24)
        
        # Draw timer (right side)
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(time_text, WINDOW_WIDTH - 180, PANEL_HEIGHT - 35, 
                        arcade.color.WHITE, 24)

    def draw_game_state_overlays(self):
        """Draw victory or game over overlays."""
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        
        # Draw victory message if all mushrooms collected AND reached exit
        if len(self.mushroom_list) == 0 and self.game_over and self.time_remaining > 0:
            # Draw semi-transparent black overlay covering the entire screen
            arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))
            
            # Draw victory text
            arcade.draw_text("VICTORY!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                           arcade.color.GREEN, 48, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                           arcade.color.WHITE, 32, anchor_x="center")
            arcade.draw_text(f"Time Remaining: {minutes:02d}:{seconds:02d}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30,
                           arcade.color.WHITE, 24, anchor_x="center")
            arcade.draw_text("You collected all food and escaped! Press R to restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60,
                           arcade.color.WHITE, 18, anchor_x="center")

        # Draw game over message if time is up
        elif self.game_over and self.time_remaining <= 0:
            # Draw semi-transparent black overlay covering the entire screen
            arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))
            
            # Draw game over text
            arcade.draw_text("GAME OVER!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                           arcade.color.RED, 48, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                           arcade.color.WHITE, 32, anchor_x="center")
            arcade.draw_text("Time's up! Press R to restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
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
            
            # Store the original position
            original_x = self.player_sprite.center_x
            original_y = self.player_sprite.center_y
            
            # Update sprites
            self.player_list.update()
            
            # Check for collisions with walls
            wall_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
            
            if wall_collision_list:
                # If collision with wall, restore original position
                self.player_sprite.center_x = original_x
                self.player_sprite.center_y = original_y
            
            # Check for collisions between player and mushrooms (food)
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.mushroom_list)
            
            # Process collisions with mushrooms (eating food)
            for mushroom in hit_list:
                # Remove the mushroom (eat the food)
                mushroom.remove_from_sprite_lists()
                # Increase score
                self.score += 1
            
            # Check for collision with exit (only if all food is collected)
            if len(self.mushroom_list) == 0:
                exit_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.exit_list)
                if exit_collision_list:
                    # Player reached the exit with all food collected - Victory!
                    self.game_over = True  # This will trigger victory screen
            
            # Spawn new mushrooms if all are collected
            if len(self.mushroom_list) == 0:
                # In maze mode, don't spawn new mushrooms - player should find exit
                pass

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
        
        # Clear and recreate the maze (this will recreate player, mushrooms/food and exit)
        self.wall_list.clear()
        self.mushroom_list.clear()
        self.exit_list.clear()
        self.player_list.clear()
        self.create_maze()


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
