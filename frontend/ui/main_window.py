"""Main application window."""

import customtkinter as ctk
from tkinter import messagebox
from ..config import Config
from ..services import VCSService, FileService, VoiceService
from .panels import LeftPanel, RightPanel, FilePanel
from .dialogs import DiffDialog

class MainWindow:
    """Main application window class."""
    
    def __init__(self):
        self.setup_appearance()
        self.init_services()
        self.init_variables()
        self.create_window()
        self.create_widgets()
        self.setup_bindings()
        self.update_all_panels()
    
    def setup_appearance(self):
        """Setup application appearance."""
        ctk.set_appearance_mode(Config.APP_THEME)
        ctk.set_default_color_theme(Config.APP_COLOR_THEME)
    
    def init_services(self):
        """Initialize service instances."""
        self.vcs_service = VCSService()
        self.file_service = FileService()
        self.voice_service = VoiceService()
    
    def init_variables(self):
        """Initialize application variables."""
        self.current_repo = ctk.StringVar(value="MyRepo")
    
    def create_window(self):
        """Create the main window."""
        self.app = ctk.CTk()
        self.app.title(Config.APP_TITLE)
        self.app.geometry(Config.APP_GEOMETRY)
    
    def create_widgets(self):
        """Create and layout all widgets."""
        self.create_top_section()
        self.create_panels()
    
    def create_top_section(self):
        """Create the top section with repository controls."""
        self.repo_name_entry = ctk.CTkEntry(
            self.app, 
            placeholder_text="Repository name", 
            width=200
        )
        self.repo_name_entry.pack(side="top", padx=10, pady=(10, 0))
        
        self.repo_action_btn = ctk.CTkButton(
            self.app, 
            text="Open/Create Repository", 
            command=self.handle_repo_action
        )
        self.repo_action_btn.pack(side="top", padx=10, pady=(15, 10))
    
    def create_panels(self):
        """Create the main panels."""
        self.left_panel = LeftPanel(self.app, self)
        self.file_panel = FilePanel(self.app, self)
        self.right_panel = RightPanel(self.app, self)
    
    def setup_bindings(self):
        """Setup event bindings."""
        self.right_panel.file_entry.bind("<FocusOut>", self.on_file_entry_change)
        self.right_panel.file_entry.bind("<Return>", self.on_file_entry_change)
    
    def on_file_entry_change(self, event=None):
        """Handle file entry changes."""
        self.right_panel.load_file_content()
        self.update_timestamps()
        self.file_panel.select_file_in_panel(self.right_panel.file_entry.get())
        self.update_suggestion()
    
    def handle_repo_action(self):
        """Handle repository open/create action."""
        repo_name = self.repo_name_entry.get().strip()
        if not repo_name:
            messagebox.showwarning("Input Required", "Please enter a repository name.")
            return
        
        if self.file_service.repo_exists(repo_name):
            self.current_repo.set(repo_name)
            self.update_all_panels()
            messagebox.showinfo("Success", f"Repository '{repo_name}' opened successfully!")
        else:
            success, message = self.vcs_service.init_repository(repo_name)
            if success:
                self.current_repo.set(repo_name)
                self.update_all_panels()
                messagebox.showinfo("Success", f"Repository '{repo_name}' created successfully!")
            else:
                messagebox.showerror("Error", message)
        
        self.update_suggestion()
    
    def update_all_panels(self):
        """Update all panels with current data."""
        self.left_panel.update_history()
        self.file_panel.update_panels()
        self.right_panel.load_file_content()
        self.update_suggestion()
    
    def update_timestamps(self):
        """Update timestamps for the current file."""
        filename = self.right_panel.file_entry.get()
        if filename:
            timestamps = self.file_service.get_timestamps_for_file(
                self.current_repo.get(), filename
            )
            self.right_panel.timestamp_menu.configure(values=timestamps)
            if timestamps:
                self.right_panel.timestamp_menu.set(timestamps[-1])
            else:
                self.right_panel.timestamp_menu.set("")
    
    def update_suggestion(self):
        """Update the suggestion text."""
        repo_name = self.current_repo.get()
        filename = self.right_panel.file_entry.get()
        
        if not self.file_service.repo_exists(repo_name):
            suggestion = "Suggestion: Create or open a repository."
        elif not filename:
            suggestion = "Suggestion: Enter a file name and click 'Add File'."
        elif not self.file_service.file_exists(f"{repo_name}/{filename}"):
            suggestion = "Suggestion: Click 'Add File' to create and add this file."
        else:
            commits = self.file_service.get_commit_files(repo_name)
            if not any(f.startswith(filename + ".") for f in commits):
                suggestion = "Suggestion: Click 'Commit' to save a version."
            else:
                suggestion = "Suggestion: You can 'Commit' changes or 'Revert' to a previous version."
        
        self.right_panel.suggestion_label.configure(text=suggestion)
    
    def show_diff_dialog(self):
        """Show the diff dialog."""
        filename = self.right_panel.file_entry.get()
        if not filename:
            messagebox.showwarning("Input Required", "Please enter a file name.")
            return
        
        dialog = DiffDialog(self.app, self.current_repo.get(), filename, self.file_service)
        dialog.show()
    
    def handle_voice_command(self):
        """Handle voice command input."""
        if not self.voice_service.is_microphone_available():
            messagebox.showerror("Error", "Microphone not available.")
            return
        
        messagebox.showinfo("Voice Command", "Listening... Please speak your command.")
        
        success, result = self.voice_service.listen_for_command()
        if success:
            action, params = self.voice_service.parse_command(result)
            messagebox.showinfo("Recognized Command", f"You said: {result}")
            
            # Execute the recognized command
            if action == "init":
                self.handle_repo_action()
            elif action == "add":
                self.right_panel.add_file()
            elif action == "update":
                self.right_panel.update_content()
            elif action == "commit":
                self.right_panel.commit_file()
            elif action == "revert":
                self.right_panel.revert_file()
            else:
                messagebox.showwarning(
                    "Unknown Command", 
                    "Command not recognized. Try saying: init, add, update, commit, or revert."
                )
        else:
            messagebox.showerror("Error", result)
    
    def run(self):
        """Start the application."""
        self.app.mainloop()
