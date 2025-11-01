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
ENEMY_SCALING = 0.02      # Enemy size (same as character)

# Movement speed
MOVEMENT_SPEED = 3
ENEMY_SPEED = 2.6  # Enemy chase speed
ENEMY_RECALC_INTERVAL = 0.15  # Seconds between enemy path recalculations

# Game duration
GAME_DURATION = 120.0  # Game duration in seconds (1 minute)

# UI Panel configuration
PANEL_HEIGHT = 60  # Height of the bottom game panel
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
# #  # # # ##### # # # # # # # #   # # #
# #  #             # # # # # # # ### # #
# #  ###### ###### # # # # # # # #   # #
# #              # # # # # # # # ### # #
# # ###### ##### # # # # # # # #   # # #
# # #M         # # # # # # # # ### # # #
# # ##### #### # # # # # # # #   # # # #
# #            #   #   #   #   #   #M# #
#  ####### ####### # # # # # # ##### # #
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


class EnemySprite(arcade.Sprite):
    """Enemy that chases the player.

    Behavior
    - Visual: uses the same ball texture as the player, tinted red, scaled by ENEMY_SCALING.
    - Spawn: created at the Exit ('E') tile by default (falls back to 'S' if exit is missing).
    - Pathfinding: grid-based BFS over MAZE_LAYOUT; passable cells are any non-`#` characters.
    - Recalculation: path to the player is recomputed roughly every 0.25 seconds.
    - Movement: steps toward the center of the next grid cell at ENEMY_SPEED pixels per frame.
    - Game over: if the enemy collides with the player, the game ends with a "CAUGHT!" overlay.
    """
    def __init__(self):
        super().__init__()
        self.texture = TEXTURES["character"]
        self.scale = ENEMY_SCALING
        # Tint enemy to red to distinguish from player
        self.color = arcade.color.RED
        # Movement target (world coordinates)
        self.target_x = None
        self.target_y = None


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
        self.won = False

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.mushroom_list = None
        self.exit_list = None
        self.enemy_list = None
        
        # Player sprite
        self.player_sprite = None
        self.enemy_sprite = None

        # Grid (list of strings) used for pathfinding
        self.grid_lines = []

        # Enemy pathfinding state
        self.enemy_path = []  # list of (row, col)
        self.enemy_recalc_timer = 0.0
        self.caught_by_enemy = False
        
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
        self.enemy_list = arcade.SpriteList()
        
        # Create the maze from the layout string
        self.create_maze()

    def create_maze(self):
        """Create all level sprites from MAZE_LAYOUT.

        Builds:
        - Walls ('#') as StoneSprite tiles
        - Mushrooms ('M') as food items
        - Player at 'S' start tile
        - Exit at 'E' tile

        Enemy spawn:
        - Spawns the EnemySprite at the exit tile so it starts away from the player.
        - If the exit is missing (shouldn't happen), spawns at 'S' as a fallback.
        - Also caches the layout lines into self.grid_lines for pathfinding.
        """
        lines = MAZE_LAYOUT.strip().split('\n')
        self.grid_lines = lines[:]  # store for pathfinding
        enemy_spawn = None
        
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
                    enemy_spawn = (row_index, col_index)

        # Create enemy at exit position (or fallback to start if missing)
        if enemy_spawn is None:
            # Fallback: spawn at player's start tile
            for r, line in enumerate(self.grid_lines):
                c = line.find('S')
                if c != -1:
                    enemy_spawn = (r, c)
                    break
        if enemy_spawn is not None:
            erow, ecol = enemy_spawn
            ex, ey = self.grid_to_world(erow, ecol)
            self.enemy_sprite = EnemySprite()
            self.enemy_sprite.center_x = ex
            self.enemy_sprite.center_y = ey
            self.enemy_list.append(self.enemy_sprite)

    # -------- Grid helpers and pathfinding --------
    def grid_to_world(self, row: int, col: int):
        """Convert a maze grid cell (row, col) to world-space (x, y) in pixels.

        Centers the sprite within the tile and translates for the bottom UI panel.
        """
        x = col * TILE_SIZE + TILE_SIZE // 2
        y = MAZE_AREA_HEIGHT - (row * TILE_SIZE + TILE_SIZE // 2) + PANEL_HEIGHT
        return x, y

    def world_to_grid(self, x: float, y: float):
        """Convert a world-space (x, y) position to a maze grid (row, col).

        Takes into account tile size, inverted y-axis for rows, and the bottom panel offset.
        Values are clamped to the valid grid bounds.
        """
        col = int(x // TILE_SIZE)
        # Invert Y back to row index
        row = int((MAZE_AREA_HEIGHT - (y - PANEL_HEIGHT) - TILE_SIZE // 2) // TILE_SIZE)
        # Clamp to grid
        row = max(0, min(MAZE_HEIGHT - 1, row))
        col = max(0, min(MAZE_WIDTH - 1, col))
        return row, col

    def is_passable(self, row: int, col: int):
        """Return True if the grid cell is passable for pathfinding (not a wall '#')."""
        ch = self.grid_lines[row][col]
        return ch != '#'

    def find_path_bfs(self, start, goal):
        """Find a shortest path on the grid from start to goal using BFS.

        Args:
            start: (row, col) start cell
            goal: (row, col) goal cell

        Returns:
            A list of (row, col) cells including start and goal. If no path exists, returns [].
        """
        from collections import deque
        if start == goal:
            return [start]
        q = deque([start])
        prev = {start: None}
        while q:
            r, c = q.popleft()
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < MAZE_HEIGHT and 0 <= nc < MAZE_WIDTH:
                    if (nr, nc) not in prev and self.is_passable(nr, nc):
                        prev[(nr, nc)] = (r, c)
                        if (nr, nc) == goal:
                            # reconstruct
                            path = [(nr, nc)]
                            while path[-1] is not None:
                                path.append(prev[path[-1]])
                            path.pop()  # remove None
                            path.reverse()
                            return path
                        q.append((nr, nc))
        return []

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
        self.enemy_list.draw()
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
        """Draw state overlays.

        Order of precedence:
        1) Victory when won == True (all food + exit)
        2) Caught-by-enemy when caught_by_enemy == True
        3) Time up when time_remaining <= 0
        """
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)

        if self.game_over and getattr(self, "won", False):
            arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))
            arcade.draw_text("VICTORY!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                             arcade.color.GREEN, 48, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.WHITE, 32, anchor_x="center")
            arcade.draw_text(f"Time Remaining: {minutes:02d}:{seconds:02d}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30,
                             arcade.color.WHITE, 24, anchor_x="center")
            arcade.draw_text("You collected all food and escaped! Press R to restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60,
                             arcade.color.WHITE, 18, anchor_x="center")

        elif self.game_over and getattr(self, "caught_by_enemy", False):
            arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))
            arcade.draw_text("CAUGHT!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                             arcade.color.ORANGE_RED, 48, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.WHITE, 32, anchor_x="center")
            arcade.draw_text("The enemy caught you. Press R to restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
                             arcade.color.WHITE, 24, anchor_x="center")

        elif self.game_over and self.time_remaining <= 0:
            arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))
            arcade.draw_text("GAME OVER!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                             arcade.color.RED, 48, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.WHITE, 32, anchor_x="center")
            arcade.draw_text("Time's up! Press R to restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
                             arcade.color.WHITE, 24, anchor_x="center")

    def on_update(self, delta_time):
        """Movement and game logic.

                - Updates the countdown timer and handles player movement/collisions.
                - Checks for food collection and exit reach to set the win state.
                - Enemy logic: every ~0.25s recalculates a BFS path to the player's grid cell and
                    moves toward the next step at ENEMY_SPEED. If the enemy collides with the player,
                    sets game_over with a caught-by-enemy overlay.
                """
        
        # Only update game logic if game is not over
        if not self.game_over:
            # Update countdown timer
            self.time_remaining -= delta_time
            
            # Check if time is up
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                self.won = False
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
                    self.game_over = True
                    self.won = True  # Mark as victory
            
            # Spawn new mushrooms if all are collected
            if len(self.mushroom_list) == 0:
                # In maze mode, don't spawn new mushrooms - player should find exit
                pass

            # Enemy pathfinding and movement
            if self.enemy_sprite is not None:
                self.enemy_recalc_timer -= delta_time
                if self.enemy_recalc_timer <= 0:
                    enemy_cell = self.world_to_grid(self.enemy_sprite.center_x, self.enemy_sprite.center_y)
                    player_cell = self.world_to_grid(self.player_sprite.center_x, self.player_sprite.center_y)
                    self.enemy_path = self.find_path_bfs(enemy_cell, player_cell)
                    self.enemy_recalc_timer = ENEMY_RECALC_INTERVAL

                if self.enemy_path and len(self.enemy_path) >= 2:
                    next_cell = self.enemy_path[1]
                    tx, ty = self.grid_to_world(*next_cell)
                    dx = tx - self.enemy_sprite.center_x
                    dy = ty - self.enemy_sprite.center_y
                    dist = (dx * dx + dy * dy) ** 0.5
                    if dist > 1e-3:
                        step = min(ENEMY_SPEED, dist)
                        self.enemy_sprite.center_x += dx / dist * step
                        self.enemy_sprite.center_y += dy / dist * step
                    else:
                        self.enemy_sprite.center_x = tx
                        self.enemy_sprite.center_y = ty

                # Collision with player ends game
                if arcade.check_for_collision(self.player_sprite, self.enemy_sprite):
                    self.game_over = True
                    self.caught_by_enemy = True
                    self.won = False

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
        self.won = False
        self.caught_by_enemy = False
        self.enemy_path = []
        self.enemy_recalc_timer = 0.0
        
        # Reset key states
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        
        # Clear and recreate the maze (this will recreate player, mushrooms/food and exit)
        self.wall_list.clear()
        self.mushroom_list.clear()
        self.exit_list.clear()
        self.enemy_list.clear()
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
