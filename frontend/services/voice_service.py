"""Voice recognition service."""

import speech_recognition as sr
from typing import Optional, Tuple

class VoiceService:
    """Service for voice recognition operations."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception:
            pass  # Continue without adjustment if microphone is not available
    
    def listen_for_command(self, timeout: int = 5) -> Tuple[bool, str]:
        """Listen for a voice command and return recognized text."""
        try:
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            # Recognize speech using Google's speech recognition
            command = self.recognizer.recognize_google(audio).lower()
            return True, command
            
        except sr.WaitTimeoutError:
            return False, "Listening timeout - no speech detected"
        except sr.UnknownValueError:
            return False, "Could not understand audio"
        except sr.RequestError as e:
            return False, f"Could not request results from speech recognition service: {e}"
        except Exception as e:
            return False, f"Error during voice recognition: {e}"
    
    def parse_command(self, command: str) -> Tuple[str, dict]:
        """Parse a voice command and extract action and parameters."""
        command = command.lower().strip()
        
        # Define command mappings
        command_mappings = {
            'init': ['init', 'initialize', 'create repository'],
            'add': ['add', 'add file'],
            'update': ['update', 'update content', 'save'],
            'commit': ['commit', 'commit file', 'save version'],
            'revert': ['revert', 'restore', 'rollback'],
            'status': ['status', 'show status'],
            'log': ['log', 'history', 'show log']
        }
        
        # Find matching command
        for action, keywords in command_mappings.items():
            if any(keyword in command for keyword in keywords):
                return action, {'original_command': command}
        
        return 'unknown', {'original_command': command}
    
    @staticmethod
    def is_microphone_available() -> bool:
        """Check if microphone is available."""
        try:
            mic = sr.Microphone()
            with mic as source:
                pass
            return True
        except Exception:
            return False
