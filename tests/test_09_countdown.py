"""
Countdown behavior tests for 09_countdown.py.
No window is opened; we only test timer logic and basic state transitions.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
import importlib
import os
import platform


ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "09_countdown.py"
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
@unittest.skipUnless(ARCADE_AVAILABLE, "Arcade not installed; skipping 09 countdown tests")
class TestCountdown09(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module(MOD_PATH)

    def test_timer_reaches_zero_and_game_over(self):
        arcade = __import__("arcade")
        GameView = self.mod.GameView
        window = arcade.Window(10, 10, "test")
        try:
            game = GameView()
            # Advance time beyond game duration in one update
            game.on_update(self.mod.GAME_DURATION + 1.0)
            self.assertEqual(game.time_remaining, 0)
            self.assertTrue(game.game_over)
        finally:
            window.close()
