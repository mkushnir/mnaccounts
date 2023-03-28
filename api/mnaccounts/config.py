"""Primitive singleton config."""

class _Config:
    _instance = None
    def __call__(self):
        if self._instance is None:
            from .app import app
            self._instance = app.config
        return self._instance

Config = _Config()
