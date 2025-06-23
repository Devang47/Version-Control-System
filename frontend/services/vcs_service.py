"""Service layer for VCS operations."""

import os
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from ..config import Config

class VCSService:
    """Service class for handling VCS operations."""
    
    def __init__(self):
        self.executable = Config.VCS_EXECUTABLE
    
    def run_command(self, command: str) -> Tuple[str, str]:
        """Execute a VCS command and return stdout and stderr."""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            return result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return "", "Command timed out"
        except Exception as e:
            return "", str(e)
    
    def init_repository(self, repo_name: str) -> Tuple[bool, str]:
        """Initialize a new repository."""
        if not repo_name.strip():
            return False, "Repository name cannot be empty"
        
        out, err = self.run_command(f"{self.executable} init {repo_name}")
        success = "Initialized empty VCS repository" in out
        message = out if success else err or "Failed to create repository"
        return success, message
    
    def add_file(self, repo_name: str, filename: str) -> Tuple[bool, str]:
        """Add a file to the repository."""
        out, err = self.run_command(f"{self.executable} add {repo_name} {filename}")
        success = "added to repository" in out
        message = out if success else err or "Failed to add file"
        return success, message
    
    def commit_file(self, repo_name: str, filename: str, message: str = "") -> Tuple[bool, str]:
        """Commit a file to the repository."""
        cmd = f"{self.executable} commit {repo_name} {filename}"
        if message:
            cmd += f' "{message}"'
        
        out, err = self.run_command(cmd)
        success = "committed" in out
        msg = out if success else err or "Failed to commit file"
        return success, msg
    
    def revert_file(self, repo_name: str, filename: str, timestamp: str = "") -> Tuple[bool, str]:
        """Revert a file to a specific version."""
        cmd = f"{self.executable} revert {repo_name} {filename}"
        if timestamp:
            cmd += f" {timestamp}"
        
        out, err = self.run_command(cmd)
        success = "reverted" in out
        message = out if success else err or "Failed to revert file"
        return success, message
    
    def get_status(self, repo_name: str) -> str:
        """Get repository status."""
        out, err = self.run_command(f"{self.executable} status {repo_name}")
        return out if out else err
    
    def get_log(self, repo_name: str, filename: str = "") -> str:
        """Get commit log for repository or specific file."""
        cmd = f"{self.executable} log {repo_name}"
        if filename:
            cmd += f" {filename}"
        
        out, err = self.run_command(cmd)
        return out if out else err
