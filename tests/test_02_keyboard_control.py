"""
Basic behavior tests for 02_keyboard_control.py without opening a window.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
import os


ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "02_keyboard_control.py"
os.environ.setdefault("PYGLET_HEADLESS", "true")
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


@unittest.skipUnless(ARCADE_AVAILABLE, "Arcade not installed; skipping 02 keyboard tests")
class TestKeyboard02(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module(MOD_PATH)

    def test_movement_key_updates_message(self):
        arcade = __import__("arcade")
        GameView = self.mod.GameView
        window = arcade.Window(10, 10, "test")
        try:
            view = GameView()
            view.on_key_press(arcade.key.W, 0)
            self.assertIn("movement", view.message)
            self.assertIn("up", view.message)
        finally:
            window.close()
