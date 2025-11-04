"""
Gravity + Sprite Sheet Animation (based on 16_gforce)

Jump with W/Up. Uses two sprite sheets for animation:
- Idle:  assets/Blue Idle - no slime/Blue Idle - no slime.png
- Jump:  assets/Blue Idle - no slime/Blue Jump - no slime.png

Assumptions:
- Each sheet is a single horizontal strip of square frames (frame_width == image_height).
- Frames are cropped automatically using that rule.

Art credit: "cactusturtle" — CC BY 4.0 (see assets/Blue Idle - no slime/LICENSE.txt)
"""
from __future__ import annotations

import arcade
from PIL import Image
from typing import List

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Gravity + Sprite Sheet Animation"

SCREEN_BOTTOM = 50
GRAVITY = 200.0
JUMP_SPEED = 200.0
MAX_JUMPS = 2  # allow up to double-jump (like in 16_gforce)

# Sprite sheet paths
IDLE_SHEET = "assets/Blue Idle - no slime/Blue Idle - no slime.png"
JUMP_SHEET = "assets/Blue Idle - no slime/Blue Jump - no slime.png"

# Animation tuning
IDLE_FRAME_TIME = 0.12
JUMP_FRAME_TIME = 0.09
CHAR_SCALE = 2.0


def load_strip_spritesheet(path: str, texture_width: int, texture_height: int) -> List[arcade.Texture]:
    """Load textures from a horizontal strip sprite sheet of square frames.

    Rule: frame_size = image_height, columns = image_width // image_height
    """
    img = Image.open(path)
    width, height = img.size
    columns = max(1, width // texture_width)
    rows = max(1, height // texture_height)
    total_textures = columns * rows

    # Use arcade.load_spritesheet to get a SpriteSheet object, then slice textures
    # https://api.arcade.academy/en/3.3.2/api/api_docs/api/texture.html#arcade.load_spritesheet
    sprite_sheet = arcade.load_spritesheet(file_name=path)
    
    # Slice individual textures from the sprite sheet
    textures = sprite_sheet.get_texture_grid((texture_width, texture_height), columns, total_textures)
    
    return textures


class AnimatedCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_textures = load_strip_spritesheet(IDLE_SHEET, 32, 32)
        self.jump_textures = load_strip_spritesheet(JUMP_SHEET, 32, 32)

        # Start idle
        self.textures = self.idle_textures or []
        if self.textures:
            self.texture = self.textures[0]
        self.scale = CHAR_SCALE

        # Animation state
        self.elapsed = 0.0
        self.frame_index = 0
        self.frame_duration = IDLE_FRAME_TIME

        # Physics state provided by GameView
        self.vertical_speed = 0.0
        self.on_ground = False

    def set_anim_state(self):
        # Choose textures based on grounded state / motion
        if self.on_ground and abs(self.vertical_speed) < 1.0:
            self.textures = self.idle_textures or []
            self.frame_duration = IDLE_FRAME_TIME
        else:
            # In air: play jump textures
            self.textures = self.jump_textures or self.idle_textures
            self.frame_duration = JUMP_FRAME_TIME
        if self.textures:
            self.frame_index %= len(self.textures)
            self.texture = self.textures[self.frame_index]

    def update_animation(self, delta_time: float = 1/60):
        self.set_anim_state()
        if not self.textures:
            return
        self.elapsed += delta_time
        if self.elapsed >= self.frame_duration:
            self.elapsed = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.textures)
            self.texture = self.textures[self.frame_index]


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AMAZON

        # Ground strip for reference
        self.ground_y = SCREEN_BOTTOM

        # Character
        self.player = AnimatedCharacter()
        self.player.center_x = WINDOW_WIDTH // 2
        self.player.center_y = self.ground_y + 120  # start slightly above ground

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Input / physics
        self.pending_jumps = 0  # track jumps taken since last grounded

    def on_draw(self):
        self.clear()
        # Ground
        arcade.draw_lbwh_rectangle_filled(0, 0, WINDOW_WIDTH, self.ground_y, arcade.color.DARK_BROWN)
        # Sprites
        self.player_list.draw()

        # UI text
        arcade.draw_text("Jump: W / Up (double-jump)", 10, WINDOW_HEIGHT - 30, arcade.color.WHITE, 14)

    def on_update(self, delta_time: float):
        # Apply gravity
        self.player.vertical_speed -= GRAVITY * delta_time
        self.player.center_y += self.player.vertical_speed * delta_time

        # Ground collision
        ground_top = self.ground_y + (0)  # lbwh rectangle, top equals ground_y
        foot = self.player.bottom
        if foot <= self.ground_y:
            # Clamp to ground
            dy = self.ground_y - foot
            self.player.center_y += dy
            self.player.vertical_speed = 0.0
            self.player.on_ground = True
            self.pending_jumps = 0
        else:
            self.player.on_ground = False

        # Keep inside window top
        if self.player.top > WINDOW_HEIGHT:
            self.player.top = WINDOW_HEIGHT
            if self.player.vertical_speed > 0:
                self.player.vertical_speed = 0

        # Animate
        self.player_list.update_animation(delta_time)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.UP):
            # Grounded -> jump; In air -> allow up to MAX_JUMPS - 1 extra jumps
            if self.player.on_ground or self.pending_jumps < (MAX_JUMPS - 1):
                self.player.vertical_speed = JUMP_SPEED
                if not self.player.on_ground:
                    self.pending_jumps += 1


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
