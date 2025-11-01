"""
Focused tests for 08_collision.py's AABB collision logic.
These tests avoid opening any Arcade windows.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "08_collision.py"
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


@unittest.skipUnless(ARCADE_AVAILABLE, "Arcade not installed; skipping 08 collision tests")
class TestCollision08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module(MOD_PATH)

    def test_edge_overlap_collides(self):
        Character = self.mod.Character
        Food = self.mod.Food

        c = Character(x=10, y=10, size=20)
        # Overlaps on both axes
        f = Food(x=25, y=15, size=10, color=(255, 255, 255))
        hits = c.detect_collisions([f])
        self.assertEqual(len(hits), 1)

    def test_separated_no_collision(self):
        Character = self.mod.Character
        Food = self.mod.Food

        c = Character(x=0, y=0, size=20)
        # Separated on x
        f = Food(x=100, y=0, size=10, color=(255, 255, 255))
        hits = c.detect_collisions([f])
        self.assertEqual(len(hits), 0)

    def test_multiple_collisions(self):
        Character = self.mod.Character
        Food = self.mod.Food

        c = Character(x=50, y=50, size=30)
        items = [
            Food(x=60, y=60, size=10, color=(255, 255, 255)),  # hit
            Food(x=10, y=10, size=5, color=(255, 255, 255)),    # no hit
            Food(x=70, y=55, size=20, color=(255, 255, 255)),   # hit
        ]
        hits = c.detect_collisions(items)
        self.assertEqual({id(h) for h in hits}, {id(items[0]), id(items[2])})
