"""
Maze layout consistency tests for 13_maze.py.
Avoids creating windows or loading textures; only validates the layout data.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "13_maze.py"
try:
    import arcade  # noqa: F401
    ARCADE_AVAILABLE = True
except Exception:
    ARCADE_AVAILABLE = False


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


@unittest.skipUnless(ARCADE_AVAILABLE, "Arcade not installed; skipping 13 maze tests")
class TestMaze13(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module(MOD_PATH)

    def test_layout_is_rectangle(self):
        layout = self.mod.MAZE_LAYOUT.strip("\n")
        lines = layout.splitlines()
        self.assertGreater(len(lines), 0)
        width = len(lines[0])
        for i, line in enumerate(lines):
            self.assertEqual(
                len(line), width, f"Row {i} length {len(line)} != {width}"
            )

    def test_layout_has_start_and_exit(self):
        layout = self.mod.MAZE_LAYOUT
        self.assertEqual(layout.count("S"), 1, "Maze should have exactly one start 'S'")
        self.assertEqual(layout.count("E"), 1, "Maze should have exactly one exit 'E'")

    def test_layout_has_food(self):
        layout = self.mod.MAZE_LAYOUT
        self.assertGreater(layout.count("M"), 0, "Maze should have at least one food 'M'")
