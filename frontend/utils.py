"""Utility functions for the frontend."""

from PIL import Image, ImageTk
from pathlib import Path
from .config import Config

class IconLoader:
    """Utility class for loading and managing icons."""
    
    def __init__(self):
        self.icons = {}
        self.icon_size = (20, 20)
    
    def get_icon(self, icon_name):
        """Get an icon by name, loading it if necessary."""
        if icon_name not in self.icons:
            self.load_icon(icon_name)
        return self.icons.get(icon_name)
    
    def load_icon(self, icon_name):
        """Load an icon from file."""
        try:
            if icon_name == "commit":
                icon_path = Config.ICON_COMMIT
            elif icon_name == "voice":
                icon_path = Config.ICON_VOICE
            elif icon_name == "diff":
                icon_path = Config.ICON_DIFF
            else:
                return None
            
            if Path(icon_path).exists():
                image = Image.open(icon_path).resize(self.icon_size)
                self.icons[icon_name] = ImageTk.PhotoImage(image)
            else:
                self.icons[icon_name] = None
                
        except Exception as e:
            print(f"Warning: Could not load icon {icon_name}: {e}")
            self.icons[icon_name] = None
    
    def load_all_icons(self):
        """Preload all icons."""
        for icon_name in ["commit", "voice", "diff"]:
            self.load_icon(icon_name)

class ValidationHelper:
    """Helper class for input validation."""
    
    @staticmethod
    def validate_filename(filename):
        """Validate a filename."""
        if not filename or not filename.strip():
            return False, "Filename cannot be empty"
        
        invalid_chars = '<>:"/\\|?*'
        if any(char in filename for char in invalid_chars):
            return False, f"Filename contains invalid characters: {invalid_chars}"
        
        if filename.startswith('.'):
            return False, "Filename cannot start with a dot"
        
        return True, ""
    
    @staticmethod
    def validate_repo_name(repo_name):
        """Validate a repository name."""
        if not repo_name or not repo_name.strip():
            return False, "Repository name cannot be empty"
        
        invalid_chars = '<>:"/\\|?*'
        if any(char in repo_name for char in invalid_chars):
            return False, f"Repository name contains invalid characters: {invalid_chars}"
        
        if repo_name.startswith('.'):
            return False, "Repository name cannot start with a dot"
        
        return True, ""
