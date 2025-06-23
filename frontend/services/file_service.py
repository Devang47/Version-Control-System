"""File system operations service."""

import os
from pathlib import Path
from typing import List, Optional
from ..config import Config

class FileService:
    """Service for file system operations."""
    
    @staticmethod
    def get_repositories() -> List[str]:
        """Get list of available repositories."""
        current_dir = Path.cwd()
        repos = []
        
        for item in current_dir.iterdir():
            if (item.is_dir() and 
                not Config.should_ignore_file(item.name) and
                not item.name.startswith('.')):
                repos.append(item.name)
        
        return sorted(repos)
    
    @staticmethod
    def get_files_in_repo(repo_path: str) -> List[str]:
        """Get list of files in a repository."""
        files = []
        repo_dir = Path(repo_path)
        
        if not repo_dir.exists():
            return files
        
        for item in repo_dir.iterdir():
            if (item.is_file() and 
                item.name != "config.txt" and
                not Config.should_ignore_file(item.name)):
                files.append(item.name)
        
        return sorted(files)
    
    @staticmethod
    def get_commit_files(repo_path: str) -> List[str]:
        """Get list of commit files."""
        commits_dir = Path(repo_path) / "commits"
        files = []
        
        if not commits_dir.exists():
            return files
        
        for item in commits_dir.iterdir():
            if item.is_file() and not item.name.endswith('.msg'):
                files.append(item.name)
        
        return sorted(files)
    
    @staticmethod
    def get_timestamps_for_file(repo_path: str, filename: str) -> List[str]:
        """Get available timestamps for a specific file."""
        commits_dir = Path(repo_path) / "commits"
        timestamps = []
        
        if not commits_dir.exists():
            return timestamps
        
        for item in commits_dir.iterdir():
            if (item.is_file() and 
                item.name.startswith(f"{filename}.") and
                not item.name.endswith('.msg')):
                parts = item.name.split('.')
                if len(parts) >= 2:
                    timestamps.append(parts[-1])
        
        return sorted(timestamps)
    
    @staticmethod
    def read_file_content(file_path: str) -> str:
        """Read content from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    
    @staticmethod
    def write_file_content(file_path: str, content: str) -> bool:
        """Write content to a file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()
    
    @staticmethod
    def repo_exists(repo_path: str) -> bool:
        """Check if a repository exists."""
        repo_dir = Path(repo_path)
        return (repo_dir.exists() and 
                (repo_dir / "config.txt").exists() and
                (repo_dir / "commits").exists())
