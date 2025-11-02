"""
Boundary clamping tests for 06_geometry_awareness.py.
These tests simulate key presses and on_update without opening a window.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
import importlib
import os
import platform


ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "06_geometry_awareness.py"
ARCADE_AVAILABLE = importlib.util.find_spec("arcade") is not None
CI = os.environ.get("CI") == "true"
IS_LINUX = platform.system() == "Linux"
WINDOW_TESTS = os.environ.get("WINDOW_TESTS") == "1"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


@unittest.skipIf(CI and not (IS_LINUX and WINDOW_TESTS), "Skip GUI window tests in CI except Linux with Xvfb")
@unittest.skipUnless(ARCADE_AVAILABLE, "Arcade not installed; skipping 06 geometry tests")
class TestGeometry06(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module(MOD_PATH)

    def test_clamp_right_edge(self):
        arcade = __import__("arcade")
        GameView = self.mod.GameView
        SQUARE_SIZE = self.mod.SQUARE_SIZE
        WINDOW_WIDTH = self.mod.WINDOW_WIDTH

        window = arcade.Window(10, 10, "test")
        try:
            view = GameView()
            view.x = WINDOW_WIDTH  # way beyond
            view.on_update(0.016)
            self.assertEqual(view.x, WINDOW_WIDTH - SQUARE_SIZE)
        finally:
            window.close()

    def test_move_and_clamp_bottom(self):
        arcade = __import__("arcade")
        GameView = self.mod.GameView
        WINDOW_HEIGHT = self.mod.WINDOW_HEIGHT

        window = arcade.Window(10, 10, "test")
        try:
            view = GameView()
            view.y = 0
            view.on_key_press(arcade.key.S, 0)
            view.on_update(0.016)
            self.assertEqual(view.y, 0)
        finally:
            window.close()
