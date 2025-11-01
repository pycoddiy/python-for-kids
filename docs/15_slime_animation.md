# 15 Slime Animation

![Screenshot](../screenshots/15_slime_animation.jpg)

Script: `15_slime_animation.py`

A richer sprite animation state machine using Slime frames (IDLE, IDLE_SLOW, WALK_L, WALK_R, BONUS as "very tired").

## Run

```bash
python 15_slime_animation.py
```

## Controls

- Arrow keys or WASD to move
- Press `P` to save a screenshot into `./screenshots/`

## States and rules

- Idle — not moving
- Slow idle — after ~2 seconds of being idle
- Moving — walk-left/walk-right based on horizontal direction
- Micro-pause grace — short breaks (< 0.2s) still count as moving
- Very tired lock — after ~15s of continuous walking:
  - Switch to BONUS frames (very tired)
  - Ignore input and stop for 5 seconds
  - Then return to idle

## Tweakable constants

- `MOVE_SPEED`, `ANIM_IDLE_FRAME_TIME`, `ANIM_IDLE_SLOW_FRAME_TIME`, `ANIM_WALK_FRAME_TIME`
- `TIRED_WALK_DELAY`, `TIRED_LOCK_DURATION`, `MOVE_BREAK_GRACE`

## Ideas to try

- Display a tiny label when resting or very tired
- Add a small dust puff when starting/stopping movement
