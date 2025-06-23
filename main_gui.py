"""Main entry point for the VCS GUI application."""

import sys
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from frontend.ui import MainWindow

def main():
    """Main function to start the VCS GUI application."""
    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
