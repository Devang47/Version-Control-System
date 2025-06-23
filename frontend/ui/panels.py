"""UI panels for the VCS application."""

import customtkinter as ctk
from tkinter import messagebox, Listbox
from ..config import Config
from ..utils import IconLoader

class LeftPanel:
    """Left panel containing history information."""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.create_widgets()
    
    def create_widgets(self):
        """Create the left panel widgets."""
        self.frame = ctk.CTkFrame(self.parent, width=180)
        self.frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Title
        ctk.CTkLabel(
            self.frame, 
            text="VCS", 
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=(10, 20))
        
        # History label
        ctk.CTkLabel(
            self.frame, 
            text="History", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10)
        
        # History textbox
        self.history_box = ctk.CTkTextbox(
            self.frame, 
            width=150, 
            height=250, 
            state="disabled"
        )
        self.history_box.pack(padx=10, pady=10)
    
    def update_history(self):
        """Update the history display."""
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        
        commits = self.main_window.file_service.get_commit_files(
            self.main_window.current_repo.get()
        )
        
        for commit in commits:
            self.history_box.insert("end", commit + "\n")
        
        self.history_box.configure(state="disabled")

class FilePanel:
    """Right panel containing repository and file listings."""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.create_widgets()
    
    def create_widgets(self):
        """Create the file panel widgets."""
        self.frame = ctk.CTkFrame(self.parent, width=200)
        self.frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Repositories section
        ctk.CTkLabel(
            self.frame, 
            text="Repositories", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 0))
        
        self.repo_listbox = Listbox(
            self.frame,
            height=5,
            width=25,
            bg=Config.BACKGROUND_COLOR,
            fg="white",
            font=("Arial", 14, "bold"),
            selectbackground=Config.SELECT_COLOR,
            selectforeground="white",
            borderwidth=2,
            relief="solid",
            highlightthickness=0
        )
        self.repo_listbox.pack(padx=10, pady=(0, 10), fill="x")
        self.repo_listbox.bind("<<ListboxSelect>>", self.on_repo_select)
        
        # Current repository label
        self.repo_label = ctk.CTkLabel(
            self.frame, 
            text=f"Repository: {self.main_window.current_repo.get()}", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.repo_label.pack(pady=(0, 10))
        
        # Files section
        ctk.CTkLabel(
            self.frame, 
            text="Files in Repo", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack()
        
        self.file_listbox = Listbox(
            self.frame,
            height=15,
            width=25,
            bg=Config.BACKGROUND_COLOR,
            fg="white",
            font=("Arial", 16, "bold"),
            selectbackground=Config.SELECT_COLOR,
            selectforeground="white",
            borderwidth=2,
            relief="solid",
            highlightthickness=0
        )
        self.file_listbox.pack(padx=10, pady=(0, 10), fill="y", expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)
    
    def update_panels(self):
        """Update both repository and file listings."""
        self.update_repo_list()
        self.update_file_list()
        self.repo_label.configure(
            text=f"Repository: {self.main_window.current_repo.get()}"
        )
    
    def update_repo_list(self):
        """Update the repository list."""
        self.repo_listbox.delete(0, "end")
        repos = self.main_window.file_service.get_repositories()
        
        for repo in repos:
            self.repo_listbox.insert("end", repo)
        
        # Select current repository
        current_repo = self.main_window.current_repo.get()
        for idx, repo in enumerate(repos):
            if repo == current_repo:
                self.repo_listbox.selection_clear(0, "end")
                self.repo_listbox.selection_set(idx)
                self.repo_listbox.see(idx)
                break
    
    def update_file_list(self):
        """Update the file list for current repository."""
        self.file_listbox.delete(0, "end")
        files = self.main_window.file_service.get_files_in_repo(
            self.main_window.current_repo.get()
        )
        
        for file in files:
            self.file_listbox.insert("end", file)
    
    def select_file_in_panel(self, filename):
        """Select a specific file in the file list."""
        files = self.file_listbox.get(0, "end")
        for idx, fname in enumerate(files):
            if fname == filename:
                self.file_listbox.selection_clear(0, "end")
                self.file_listbox.selection_set(idx)
                self.file_listbox.see(idx)
                break
    
    def on_repo_select(self, event):
        """Handle repository selection."""
        selection = self.repo_listbox.curselection()
        if selection:
            repo = self.repo_listbox.get(selection[0])
            self.main_window.current_repo.set(repo)
            self.main_window.update_all_panels()
    
    def on_file_select(self, event):
        """Handle file selection."""
        selection = self.file_listbox.curselection()
        if selection:
            filename = self.file_listbox.get(selection[0])
            self.main_window.right_panel.file_entry.delete(0, "end")
            self.main_window.right_panel.file_entry.insert(0, filename)
            self.main_window.right_panel.load_file_content()
            self.main_window.update_timestamps()
            self.main_window.update_suggestion()

class RightPanel:
    """Main panel containing file operations and workspace."""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.icon_loader = IconLoader()
        self.create_widgets()
    
    def create_widgets(self):
        """Create the right panel widgets."""
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.create_file_controls()
        self.create_timestamp_controls()
        self.create_workspace()
        self.create_action_buttons()
        self.create_suggestion_label()
    
    def create_file_controls(self):
        """Create file name entry and add/update buttons."""
        file_row = ctk.CTkFrame(self.frame, fg_color="transparent")
        file_row.pack(pady=(10, 5), anchor="nw")
        
        self.file_entry = ctk.CTkEntry(
            file_row, 
            placeholder_text="File name", 
            width=200
        )
        self.file_entry.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            file_row, 
            text="Add File", 
            command=self.add_file
        ).pack(side="left")
        
        ctk.CTkButton(
            file_row, 
            text="Update Content", 
            command=self.update_content
        ).pack(side="left", padx=(10, 0))
    
    def create_timestamp_controls(self):
        """Create timestamp selection and revert button."""
        ts_row = ctk.CTkFrame(self.frame, fg_color="transparent")
        ts_row.pack(pady=(5, 5), anchor="nw")
        
        self.timestamp_menu = ctk.CTkComboBox(ts_row, values=[], width=200)
        self.timestamp_menu.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            ts_row, 
            text="Revert", 
            command=self.revert_file
        ).pack(side="left")
    
    def create_workspace(self):
        """Create the main workspace text area."""
        self.workspace = ctk.CTkTextbox(self.frame, height=150, width=350)
        self.workspace.pack(pady=10, fill="both", expand=True)
    
    def create_action_buttons(self):
        """Create the main action buttons."""
        # Commit button
        commit_btn = ctk.CTkButton(
            self.frame, 
            text="Commit", 
            image=self.icon_loader.get_icon("commit"),
            command=self.commit_file, 
            width=350, 
            height=40, 
            compound="left"
        )
        commit_btn.pack(pady=(10, 0))
        
        # Voice command button
        voice_btn = ctk.CTkButton(
            self.frame, 
            text="Voice Command", 
            image=self.icon_loader.get_icon("voice"),
            command=self.main_window.handle_voice_command, 
            width=350, 
            height=40, 
            compound="left"
        )
        voice_btn.pack(pady=(10, 0))
        
        # Show diff button
        diff_btn = ctk.CTkButton(
            self.frame, 
            text="Show Diff", 
            image=self.icon_loader.get_icon("diff"),
            command=self.main_window.show_diff_dialog, 
            width=350, 
            height=40, 
            compound="left"
        )
        diff_btn.pack(pady=(10, 0))
    
    def create_suggestion_label(self):
        """Create the suggestion label."""
        self.suggestion_label = ctk.CTkLabel(
            self.frame, 
            text="", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            text_color=Config.SUGGESTION_COLOR
        )
        self.suggestion_label.pack(pady=(0, 5), anchor="nw")
    
    def add_file(self):
        """Add a file to the repository."""
        filename = self.file_entry.get()
        if not filename:
            messagebox.showwarning("Input Required", "Please enter a file name.")
            return
        
        repo_name = self.main_window.current_repo.get()
        repo_file_path = f"{repo_name}/{filename}"
        
        if not self.main_window.file_service.file_exists(repo_file_path):
            create = messagebox.askyesno(
                "File Not Found", 
                f"'{filename}' does not exist in repo. Create it?"
            )
            if create:
                # Create empty file and add to repo
                if self.main_window.file_service.write_file_content(filename, ""):
                    success, message = self.main_window.vcs_service.add_file(repo_name, filename)
                    if success:
                        messagebox.showinfo("Success", f"File '{filename}' created and added.")
                        self.workspace.delete("1.0", "end")
                        self.main_window.update_all_panels()
                    else:
                        messagebox.showerror("Error", message)
        else:
            # Update existing file
            content = self.workspace.get("1.0", "end-1c")
            if self.main_window.file_service.write_file_content(filename, content):
                success, message = self.main_window.vcs_service.add_file(repo_name, filename)
                if success:
                    messagebox.showinfo("Success", f"File '{filename}' updated.")
                    self.main_window.update_all_panels()
                else:
                    messagebox.showerror("Error", message)
    
    def update_content(self):
        """Update file content in repository."""
        filename = self.file_entry.get()
        if not filename:
            messagebox.showwarning("Input Required", "Please enter a file name.")
            return
        
        repo_name = self.main_window.current_repo.get()
        repo_file_path = f"{repo_name}/{filename}"
        
        if not self.main_window.file_service.file_exists(repo_file_path):
            messagebox.showwarning("File Not Found", f"'{filename}' not found in repository.")
            return
        
        content = self.workspace.get("1.0", "end-1c")
        if self.main_window.file_service.write_file_content(filename, content):
            success, message = self.main_window.vcs_service.add_file(repo_name, filename)
            if success:
                messagebox.showinfo("Success", f"Content of '{filename}' updated.")
                self.main_window.update_all_panels()
            else:
                messagebox.showerror("Error", message)
    
    def load_file_content(self):
        """Load file content into workspace."""
        filename = self.file_entry.get()
        if not filename:
            self.workspace.delete("1.0", "end")
            return
        
        repo_name = self.main_window.current_repo.get()
        repo_file_path = f"{repo_name}/{filename}"
        
        if self.main_window.file_service.file_exists(repo_file_path):
            content = self.main_window.file_service.read_file_content(repo_file_path)
            self.workspace.delete("1.0", "end")
            self.workspace.insert("1.0", content)
        else:
            self.workspace.delete("1.0", "end")
    
    def commit_file(self):
        """Commit a file to the repository."""
        filename = self.file_entry.get()
        if not filename:
            messagebox.showwarning("Input Required", "Please enter a file name.")
            return
        
        content = self.workspace.get("1.0", "end-1c")
        if self.main_window.file_service.write_file_content(filename, content):
            repo_name = self.main_window.current_repo.get()
            success, message = self.main_window.vcs_service.commit_file(repo_name, filename)
            
            if success:
                messagebox.showinfo("Success", f"File '{filename}' committed.")
                self.main_window.update_all_panels()
                self.main_window.update_timestamps()
            else:
                messagebox.showerror("Error", message)
    
    def revert_file(self):
        """Revert a file to a specific version."""
        filename = self.file_entry.get()
        timestamp = self.timestamp_menu.get()
        
        if not filename:
            messagebox.showwarning("Input Required", "Please enter a file name.")
            return
        if not timestamp:
            messagebox.showwarning("Input Required", "Please select a timestamp.")
            return
        
        repo_name = self.main_window.current_repo.get()
        success, message = self.main_window.vcs_service.revert_file(
            repo_name, filename, timestamp
        )
        
        if success:
            messagebox.showinfo("Success", f"File '{filename}' reverted.")
            self.load_file_content()
            self.main_window.update_all_panels()
        else:
            messagebox.showerror("Error", message)
