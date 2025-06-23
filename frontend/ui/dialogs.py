"""Dialog windows for the VCS application."""

import customtkinter as ctk
import difflib
from tkinter import messagebox

class DiffDialog:
    """Dialog for showing file differences."""
    
    def __init__(self, parent, repo_name, filename, file_service):
        self.parent = parent
        self.repo_name = repo_name
        self.filename = filename
        self.file_service = file_service
        self.window = None
    
    def show(self):
        """Show the diff dialog."""
        current_content = self.get_current_content()
        committed_content = self.get_committed_content()
        
        if committed_content is None:
            messagebox.showinfo("No Commit", "No committed version found for this file.")
            return
        
        diff_text = self.generate_diff(committed_content, current_content)
        self.create_dialog(diff_text)
    
    def get_current_content(self):
        """Get current file content."""
        file_path = f"{self.repo_name}/{self.filename}"
        if self.file_service.file_exists(file_path):
            return self.file_service.read_file_content(file_path).splitlines()
        return []
    
    def get_committed_content(self):
        """Get the latest committed version content."""
        timestamps = self.file_service.get_timestamps_for_file(self.repo_name, self.filename)
        if not timestamps:
            return None
        
        latest_timestamp = timestamps[-1]
        commit_file_path = f"{self.repo_name}/commits/{self.filename}.{latest_timestamp}"
        
        if self.file_service.file_exists(commit_file_path):
            return self.file_service.read_file_content(commit_file_path).splitlines()
        return None
    
    def generate_diff(self, old_content, new_content):
        """Generate diff text between two content versions."""
        diff = difflib.ndiff(old_content, new_content)
        diff_lines = []
        
        for line in diff:
            if line.startswith('- '):
                diff_lines.append(f"Removed: {line[2:]}")
            elif line.startswith('+ '):
                diff_lines.append(f"Added: {line[2:]}")
            elif line.startswith('? '):
                continue  # Skip hint lines
            else:
                diff_lines.append(f"Unchanged: {line[2:]}")
        
        if not any(line.startswith(('Removed:', 'Added:')) for line in diff_lines):
            return "No differences found."
        
        return "\n".join(diff_lines)
    
    def create_dialog(self, diff_text):
        """Create and show the diff dialog window."""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title(f"Diff: {self.filename} (Committed vs Current)")
        self.window.geometry("700x400")
        
        # Make dialog modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Create diff textbox
        diff_box = ctk.CTkTextbox(self.window, width=680, height=350)
        diff_box.pack(padx=10, pady=10, fill="both", expand=True)
        diff_box.insert("1.0", diff_text)
        diff_box.configure(state="disabled")
        
        # Close button
        close_btn = ctk.CTkButton(
            self.window, 
            text="Close", 
            command=self.close_dialog,
            width=100
        )
        close_btn.pack(pady=10)
        
        # Center the dialog
        self.center_dialog()
    
    def center_dialog(self):
        """Center the dialog on the parent window."""
        self.window.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.window.winfo_width()
        dialog_height = self.window.winfo_height()
        
        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.window.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def close_dialog(self):
        """Close the dialog."""
        if self.window:
            self.window.destroy()
