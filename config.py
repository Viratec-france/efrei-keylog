"""Configuration management"""

import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "system_monitor"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    if not CONFIG_FILE.exists():
        return get_default_config()
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return get_default_config()


def save_config(config: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_default_config() -> dict:
    return {
        'webhook_url': None,
        'bot_token': None,
        'exfil_interval': 600,
        'version': '1.0.0'
    }


def set_webhook(url: str):
    config = load_config()
    config['webhook_url'] = url
    save_config(config)
    print(f"[+] Webhook saved: {url}")


def get_webhook() -> str:
    config = load_config()
    return config.get('webhook_url')


def set_bot_token(token: str):
    config = load_config()
    config['bot_token'] = token
    save_config(config)
    print(f"[+] Bot token saved")


def get_bot_token() -> str:
    config = load_config()
    return config.get('bot_token')


if __name__ == "__main__":
    print("Configuration file:", CONFIG_FILE)
    print(load_config())
