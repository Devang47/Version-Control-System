"""Configuration settings for the VCS GUI application."""

import os
from pathlib import Path

class Config:
    """Application configuration settings."""
    
    # Application settings
    APP_TITLE = "VCS - Version Control System"
    APP_GEOMETRY = "1100x500"
    APP_THEME = "dark"
    APP_COLOR_THEME = "blue"
    
    # UI Colors
    SUGGESTION_COLOR = "#00BFFF"
    BACKGROUND_COLOR = "#23272f"
    SELECT_COLOR = "#2563eb"
    
    # Icon paths
    ICONS_DIR = Path("icons")
    ICON_COMMIT = ICONS_DIR / "icons8-page-64.png"
    ICON_VOICE = ICONS_DIR / "icons8-voice-50.png"
    ICON_DIFF = ICONS_DIR / "icons8-change.gif"
    
    # VCS executable
    VCS_EXECUTABLE = "./myvcs"
    
    # File patterns to ignore
    IGNORE_PATTERNS = ["__pycache__", ".git", ".vscode", "node_modules"]
    
    @classmethod
    def get_icon_path(cls, icon_name):
        """Get the full path for an icon."""
        return cls.ICONS_DIR / icon_name
    
    @classmethod
    def should_ignore_file(cls, filename):
        """Check if a file should be ignored."""
        return any(pattern in filename for pattern in cls.IGNORE_PATTERNS)
