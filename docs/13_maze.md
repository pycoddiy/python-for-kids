# 13 Maze

![Screenshot](../screenshots/13_maze.jpg)

Script: `13_maze.py`

Navigate a grid-based maze, collect all the food, and reach the exit before time runs out. This one focuses on navigation, collisions, and a countdown.

## Run

```bash
python 13_maze.py
```

## Controls

- Arrow keys or WASD

## Key features

- Level encoded as a fixed-width multiline string (consistent row lengths)
- Bottom info panel so text doesn’t obscure the maze
- Collectible food items placed by the layout
- Reach the exit only after all food is collected
- Clear overlays: victory when you escape in time, or game over when time runs out
- Tunable constants: tile size, panel height, movement speed, game duration

## Ideas to try

- Change the maze layout and verify it still has a valid path
- Add more food or open extra escape corridors
- Add a timer bonus for collecting all food quickly
