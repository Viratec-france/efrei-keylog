"""
Screenshot Capture Module - Capture aléatoire de l'écran
Module subsidiaire pour documentation du contexte d'utilisation
"""

import os
import json
import logging
import time
import random
from datetime import datetime
from pathlib import Path
from threading import Thread, Lock
from PIL import ImageGrab
from typing import Optional


class ScreenshotCapture:
    """
    Capture aléatoire d'écran pour documentation de contexte.
    Utile pour comprendre le comportement utilisateur et valider les logs.
    """
    
    def __init__(self, output_dir: str = "~/.cache/system_logs",
                 interval_min: int = 300,
                 interval_max: int = 900,
                 max_screenshots: int = 100):
        """
        Initialize le capteur d'écran.
        
        Args:
            output_dir: Répertoire de stockage
            interval_min: Délai minimum entre captures (secondes)
            interval_max: Délai maximum entre captures (secondes)
            max_screenshots: Nombre max avant suppression des anciennes
        """
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.screenshot_dir = self.output_dir / "screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)
        
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.max_screenshots = max_screenshots
        
        self.is_running = False
        self.thread = None
        self.lock = Lock()
        self.capture_count = 0
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure le logging interne."""
        log_file = self.output_dir / "screenshot_debug.log"
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        logger = logging.getLogger('screenshot_logger')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self.logger = logger
    
    def _cleanup_old_screenshots(self):
        """Supprime les captures les plus anciennes si dépassement."""
        screenshots = sorted(self.screenshot_dir.glob("*.png"))
        
        if len(screenshots) >= self.max_screenshots:
            # Supprime les plus anciennes
            to_remove = len(screenshots) - self.max_screenshots + 1
            for screenshot in screenshots[:to_remove]:
                try:
                    screenshot.unlink()
                    self.logger.info(f"Removed old screenshot: {screenshot.name}")
                except:
                    pass
    
    def _capture_screen(self) -> Optional[str]:
        """Capture l'écran et sauvegarde."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"screen_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            # Capture
            screenshot = ImageGrab.grab()
            screenshot.save(filepath, quality=60)
            
            with self.lock:
                self.capture_count += 1
            
            self.logger.info(f"Screenshot captured: {filename}")
            self._cleanup_old_screenshots()
            
            return filename
        except Exception as e:
            self.logger.error(f"Capture failed: {e}")
            return None
    
    def _capture_worker(self):
        """Worker thread pour captures aléatoires."""
        while self.is_running:
            interval = random.randint(self.interval_min, self.interval_max)
            time.sleep(interval)
            
            if self.is_running:
                self._capture_screen()
    
    def start(self):
        """Démarre les captures aléatoires."""
        if self.is_running:
            self.logger.warning("Screenshot capture already running")
            return
        
        self.is_running = True
        self.thread = Thread(target=self._capture_worker, daemon=True)
        self.thread.start()
        self.logger.info("Screenshot capture started")
    
    def stop(self):
        """Arrête les captures."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        self.logger.info("Screenshot capture stopped")
    
    def get_statistics(self) -> dict:
        """Retourne stats de captures."""
        screenshots = list(self.screenshot_dir.glob("*.png"))
        total_size = sum(f.stat().st_size for f in screenshots) / (1024 * 1024)  # MB
        
        with self.lock:
            return {
                'total_screenshots': self.capture_count,
                'stored_screenshots': len(screenshots),
                'total_size_mb': round(total_size, 2),
                'is_running': self.is_running
            }
    
    def force_capture(self) -> Optional[str]:
        """Force une capture immédiate."""
        return self._capture_screen()


if __name__ == "__main__":
    capturer = ScreenshotCapture(
        interval_min=10,  # Pour test: 10 secondes minimum
        interval_max=30
    )
    capturer.start()
    
    try:
        print("Screenshot capture running... (Ctrl+C to stop)")
        while True:
            time.sleep(5)
            stats = capturer.get_statistics()
            print(f"Captures: {stats['total_screenshots']} | "
                  f"Stored: {stats['stored_screenshots']} | "
                  f"Size: {stats['total_size_mb']}MB")
    except KeyboardInterrupt:
        capturer.stop()
        print("\nScreenshot capture stopped")
