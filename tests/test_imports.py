"""
Generic import tests for all example scripts.

These tests only verify that each example file can be imported as a module
without executing its main loop. This helps catch syntax errors and accidental
top-level side effects.

We load modules by file path because many filenames start with digits and
aren't valid Python identifiers.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
import importlib


ROOT = Path(__file__).resolve().parents[1]
ARCADE_AVAILABLE = importlib.util.find_spec("arcade") is not None


def load_module_from_path(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


@unittest.skipUnless(ARCADE_AVAILABLE, "Arcade not installed; skipping import tests")
class TestExampleImports(unittest.TestCase):
    def test_import_all_examples(self):
        # Find all example scripts like '00_*.py', '01_*.py', etc. in repo root
        example_files = sorted(
            [p for p in ROOT.iterdir() if p.is_file() and p.name[:2].isdigit() and p.suffix == ".py"]
        )
        self.assertGreater(len(example_files), 0, "No example scripts found")

        for path in example_files:
            with self.subTest(script=path.name):
                mod = load_module_from_path(path)
                # Optional sanity: most examples expose GameView class
                self.assertTrue(hasattr(mod, "GameView"), f"{path.name} should define GameView")
