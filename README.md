# Polymarket Alert Bot

A Python bot that monitors Polymarket prediction markets and sends Telegram alerts when significant changes in liquidity occur.

## Features

- 🔍 Monitors 500+ Polymarket markets every 30 minutes
- 📊 Tracks liquidity and volume changes over time
- 📱 Sends Telegram notifications for significant market movements
- 💾 Persists market data in SQLite for historical tracking
- 🤖 Runs 24/7 
- 📝 Comprehensive logging for monitoring and debugging

## How It Works

1. **Fetches** current market data from Polymarket's Gamma API
2. **Compares** to previous snapshots stored in SQLite
3. **Detects** significant changes (default: 50% threshold)
4. **Alerts** via Telegram when changes exceed threshold
5. **Saves** current snapshot for next comparison

## Alert Types

- **🆕 New Markets**: Markets with >$50k initial liquidity
- **📈 Liquidity Changes**: Significant increases/decreases in available liquidity
- **📊 Volume Changes**: Unusual trading activity spikes

## Requirements

- Python 3.11+
- uv (package manager)
- Telegram bot token and chat ID
- Linux VM/Server

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/polymarket-pool-alerts.git
cd polymarket-pool-alerts
```

### 2. Install dependencies
```bash
# Install uv 
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 3. Configure Telegram

Create a `.env` file:
```bash
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT=your_chat_id_here
```
### 4. Run locally
```bash
uv run main.py
```
### VM/Cloud Instance 

### 1. Connect and setup
```bash
# SSH into your instance
ssh -i your-key.key ubuntu@YOUR_IP

# Update system
sudo apt update
sudo apt install -y python3 python3-pip git

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

### 2. Deploy the bot
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/polymarket-pool-alerts.git
cd polymarket-pool-alerts

# Install dependencies
uv sync

# Create .env file with your Telegram credentials
nano .env
```

### 3. Setup as a systemd service

Create service file:
```bash
sudo nano /etc/systemd/system/polymarket-bot.service
```

Configuration:
```ini
[Unit]
Description=Polymarket Alert Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/polymarket-pool-alerts
ExecStart=/home/ubuntu/polymarket-pool-alerts/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable polymarket-bot
sudo systemctl start polymarket-bot
```

### 4. Monitor the bot
```bash
# Check status
sudo systemctl status polymarket-bot

# View live logs
sudo journalctl -u polymarket-bot -f

# View bot log file
tail -f ~/polymarket-pool-alerts/bot.log
```

## Configuration

Edit `config.py` to customize:
```python
CHECK_INTERVAL_MINUTES = 30  # How often to check
CHANGE_THRESHOLD_PERCENT = 50  # Alert threshold
MARKETS_TO_FETCH = 500  # Number of markets to monitor
```

Or adjust thresholds in `monitor.py`:
- New market liquidity threshold (default: $50k)
- Change detection logic

## Project Structure
```
polymarket-pool-alerts/
├── main.py              # Entry point and monitoring loop
├── fetch_data.py        # Polymarket API integration
├── database.py          # SQLite operations
├── monitor.py           # Change detection logic
├── alerts.py            # Telegram integration
├── logger.py            # Logging configuration
├── test_monitor.py      # Monitor tests
├── test_database.py     # Database tests
├── markets.db           # SQLite database (created on first run)
├── bot.log              # Log file (created on first run)
└── .env                 # Telegram credentials (not in git)
```

## Testing

Run tests locally:
```bash
uv run pytest -v
```

## API Reference

**Polymarket Gamma API:**
- Endpoint: `https://gamma-api.polymarket.com/events`
- No authentication required
- Rate limits: Reasonable for personal use
- [Documentation](https://docs.polymarket.com/)

## What I Learned

- Working with REST APIs and pagination
- SQLite for persistent data storage
- Deploying to cloud infrastructure (Oracle Cloud)
- Setting up systemd services
- Writing tests with pytest
- Managing secrets with .env files

## Possible Future Improvements

- [ ] Add market category filtering (Politics, Crypto, Sports)
- [ ] Include Polymarket URLs in alerts
- [ ] Configurable thresholds per category
- [ ] Daily summary instead of real-time alerts
- [ ] Web dashboard for monitoring


## License

MIT


## Acknowledgments

Built using:
- [Polymarket API](https://docs.polymarket.com/)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [uv](https://github.com/astral-sh/uv) for dependency management
