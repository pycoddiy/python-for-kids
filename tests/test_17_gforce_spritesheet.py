import importlib.util
import pathlib
import sys
import pytest


def load_module_from_path(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def test_17_module_imports_and_textures_load():
    # Resolve repo root and module path
    root = pathlib.Path(__file__).resolve().parents[1]
    mod_path = root / "17_gforce_spritesheet.py"
    assert mod_path.exists(), f"Missing file: {mod_path}"

    try:
        import arcade  # noqa: F401
    except Exception as e:  # pragma: no cover - environment specific
        pytest.skip(f"arcade not available: {e}")

    mod = load_module_from_path(mod_path)

    # Basic contract
    assert hasattr(mod, "GameView")

    # Texture loading should work without a window
    idle_tex = mod.load_strip_spritesheet(mod.IDLE_SHEET)
    jump_tex = mod.load_strip_spritesheet(mod.JUMP_SHEET)
    assert isinstance(idle_tex, list) and len(idle_tex) > 0
    assert isinstance(jump_tex, list) and len(jump_tex) > 0
