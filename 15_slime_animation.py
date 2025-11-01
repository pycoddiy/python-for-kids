"""
Slime Animation Demo (based on 06_geometry_awareness)

- Move the slime with Arrow Keys or WASD
- Uses frame-based animation for idle and walking (left/right)
- Demonstrates boundary/geometry awareness (keeps sprite inside window)
"""
import arcade
import glob
import os
from datetime import datetime
from typing import List

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Slime Sprite Animation"

# Movement and animation tuning
MOVE_SPEED = 3.5
ANIM_IDLE_FRAME_TIME = 0.20   # seconds per frame while idle
ANIM_IDLE_SLOW_FRAME_TIME = 0.22  # seconds per frame while resting
ANIM_TIRED_FRAME_TIME = 0.18  # seconds per frame while very tired
ANIM_IDLE_REST_DELAY = 5.0    # seconds idle before switching to resting
TIRED_WALK_DELAY = 15.0       # seconds of continuous walking to become very tired
ANIM_WALK_FRAME_TIME = 0.12   # seconds per frame while walking
SLIME_SCALE = 1.0             # Adjust if frames are too large/small
MOVE_BREAK_GRACE = 0.20       # brief stop under this time still counts as moving
TIRED_LOCK_DURATION = 10.0     # seconds to remain in very tired (no input) state

# Asset roots (individual frames)
ASSETS_ROOT = os.path.join("assets", "SLIME")
IDLE_DIR = os.path.join(ASSETS_ROOT, "IDLE", "Frame")
IDLE_SLOW_DIR = os.path.join(ASSETS_ROOT, "IDLE_SLOW", "Frame")
BONUS_DIR = os.path.join(ASSETS_ROOT, "BONUS", "Frame")
WALK_R_DIR = os.path.join(ASSETS_ROOT, "WALK_R", "Frame")
WALK_L_DIR = os.path.join(ASSETS_ROOT, "WALK_L", "Frame")


def load_textures_from(dir_path: str) -> List[arcade.Texture]:
    """Load all .png textures from a directory, sorted naturally by trailing number.

    This ensures frames like 5,6,7,8,9,10,11 sort in numeric order.
    """
    def key_numeric(path: str) -> tuple:
        base = os.path.basename(path)
        num = ''
        # Extract trailing digits
        for ch in reversed(base.split('.')[0]):
            if ch.isdigit():
                num = ch + num
            else:
                break
        return (base.rstrip('0123456789'), int(num) if num else -1)

    files = sorted(glob.glob(os.path.join(dir_path, "*.png")), key=key_numeric)
    return [arcade.load_texture(f) for f in files]


class AnimatedSlime(arcade.Sprite):
    """A simple animated sprite using separate frame lists.

    Animation states:
    - idle_textures: loops when not moving
    - walk_left_textures: loops when moving left
    - walk_right_textures: loops when moving right

    update_animation() advances frames based on elapsed time and current state.
    """
    def __init__(self):
        super().__init__()
        # Load textures
        self.idle_textures = load_textures_from(IDLE_DIR)
        self.idle_slow_textures = load_textures_from(IDLE_SLOW_DIR)
        # BONUS frames represent a very tired animation in our demo
        self.tired_textures = load_textures_from(BONUS_DIR)
        self.walk_right_textures = load_textures_from(WALK_R_DIR)
        self.walk_left_textures = load_textures_from(WALK_L_DIR)

        # Start in resting (slow idle) if available
        if self.idle_slow_textures:
            self.textures = self.idle_slow_textures
        else:
            self.textures = self.idle_textures
        self.texture = self.textures[0] if self.textures else None
        self.scale = SLIME_SCALE

        # Animation timing
        self.elapsed = 0.0
        self.frame_index = 0
        if self.textures is self.idle_slow_textures:
            self.frame_duration = ANIM_IDLE_SLOW_FRAME_TIME
        else:
            self.frame_duration = ANIM_IDLE_FRAME_TIME
        # Treat as already resting so the state machine keeps slow idle until you move
        self.idle_time = ANIM_IDLE_REST_DELAY
        self.moving_time = 0.0  # time spent moving (walking)
        self.since_stop = MOVE_BREAK_GRACE  # time since last non-moving; start beyond grace

        # Exhaustion lock (very tired)
        self.is_tired_active = False
        self.tired_time_left = 0.0

        # State
        self.is_moving = False
        self.facing = "right"  # or "left"

    def set_state_from_velocity(self, delta_time: float):
        """Pick texture set and frame timing from current velocity, idle, and walking time.

    - After ANIM_IDLE_REST_DELAY of not moving, switch to idle_slow animations.
    - After TIRED_WALK_DELAY of continuous walking, enter very tired lock (BONUS frames) for TIRED_LOCK_DURATION.
    - During very tired lock, ignore input (no movement) and show tired animation.
    - Short breaks under MOVE_BREAK_GRACE keep the slime in moving state.
        """
        # If currently exhausted, stay in tired lock
        if self.is_tired_active:
            self.is_moving = False
            if self.tired_textures:
                self.textures = self.tired_textures
                self.frame_duration = ANIM_TIRED_FRAME_TIME
            else:
                self.textures = self.idle_textures
                self.frame_duration = ANIM_IDLE_FRAME_TIME
            self.tired_time_left -= delta_time
            if self.tired_time_left <= 0:
                # Exit tired lock into normal idle state
                self.is_tired_active = False
                self.tired_time_left = 0.0
                self.idle_time = 0.0
                self.moving_time = 0.0
                self.since_stop = MOVE_BREAK_GRACE
            # Ensure frame index is valid for current textures
            if self.textures:
                self.frame_index %= len(self.textures)
                self.texture = self.textures[self.frame_index]
            return

        raw_moving = abs(self.change_x) > 0.01 or abs(self.change_y) > 0.01
        # Update stop-grace timer
        if raw_moving:
            self.since_stop = 0.0
        else:
            self.since_stop += delta_time

        effective_moving = raw_moving or (self.since_stop < MOVE_BREAK_GRACE)

        if effective_moving:
            # Pick by horizontal direction; if none, keep last facing
            if self.change_x < -0.01:
                self.facing = "left"
            elif self.change_x > 0.01:
                self.facing = "right"
            self.is_moving = True
            # After long walking, enter very tired lock; otherwise walk
            if self.moving_time >= TIRED_WALK_DELAY and self.tired_textures:
                self.is_tired_active = True
                self.tired_time_left = TIRED_LOCK_DURATION
                # Immediately switch to tired visuals
                self.textures = self.tired_textures
                self.frame_duration = ANIM_TIRED_FRAME_TIME
            else:
                self.textures = self.walk_left_textures if self.facing == "left" else self.walk_right_textures
                self.frame_duration = ANIM_WALK_FRAME_TIME
            self.idle_time = 0.0
        else:
            self.is_moving = False
            # when idle: slow idle after rest, else normal idle
            if self.idle_time >= ANIM_IDLE_REST_DELAY and self.idle_slow_textures:
                self.textures = self.idle_slow_textures
                self.frame_duration = ANIM_IDLE_SLOW_FRAME_TIME
            else:
                self.textures = self.idle_textures
                self.frame_duration = ANIM_IDLE_FRAME_TIME

        # Keep current frame index within new list
        if self.textures:
            self.frame_index %= len(self.textures)
            self.texture = self.textures[self.frame_index]

    def update_animation(self, delta_time: float = 1/60):
        # Update the state from current velocity (with short-break grace)
        self.set_state_from_velocity(delta_time)
        if not self.textures:
            return
        # Track idle vs moving durations
        if self.is_tired_active:
            # While exhausted, don't accumulate idle or moving timers
            self.idle_time = 0.0
            self.moving_time = 0.0
        elif not self.is_moving:
            self.idle_time += delta_time
            self.moving_time = 0.0
        else:
            self.idle_time = 0.0
            self.moving_time += delta_time
        self.elapsed += delta_time
        if self.elapsed >= self.frame_duration:
            self.elapsed = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.textures)
            self.texture = self.textures[self.frame_index]


class GameView(arcade.View):
    """Main application with geometry awareness + slime animation."""

    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AMAZON

        # Input state
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Sprites
        self.player_list: arcade.SpriteList | None = None
        self.player: AnimatedSlime | None = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = AnimatedSlime()
        # Place at center
        self.player.center_x = WINDOW_WIDTH // 2
        self.player.center_y = WINDOW_HEIGHT // 2
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        if self.player_list:
            self.player_list.draw()

        # Optional: simple UI text
        arcade.draw_text(
            "Move: Arrow Keys / WASD", 10, WINDOW_HEIGHT - 30, arcade.color.WHITE, 14
        )

    def on_update(self, delta_time: float):
        if not self.player:
            return
        # Movement from input
        self.player.change_x = 0
        self.player.change_y = 0
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVE_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVE_SPEED
        if self.up_pressed and not self.down_pressed:
            self.player.change_y = MOVE_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -MOVE_SPEED

        # If player is in very tired lock, ignore movement (no response to keys)
        if self.player.is_tired_active:
            self.player.change_x = 0
            self.player.change_y = 0

        # Update sprite (position + animation)
        self.player_list.update()
        self.player_list.update_animation(delta_time)

        # Keep the player inside the window borders
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > WINDOW_WIDTH:
            self.player.right = WINDOW_WIDTH
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.top > WINDOW_HEIGHT:
            self.player.top = WINDOW_HEIGHT

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.LEFT):
            self.left_pressed = True
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.right_pressed = True
        elif key in (arcade.key.W, arcade.key.UP):
            self.up_pressed = True
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.down_pressed = True
        elif key == arcade.key.P:
            # Save a screenshot to ./screenshots
            try:
                os.makedirs("screenshots", exist_ok=True)
                image = arcade.get_image()
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                path = os.path.join("screenshots", f"slime_{timestamp}.png")
                image.save(path)
                print(f"Saved screenshot: {path}")
            except Exception as e:
                print(f"Failed to save screenshot: {e}")

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.LEFT):
            self.left_pressed = False
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.right_pressed = False
        elif key in (arcade.key.W, arcade.key.UP):
            self.up_pressed = False
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.down_pressed = False


def main():
    # Create a window and start the view
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game_view = GameView()
    window.show_view(game_view)
    game_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
