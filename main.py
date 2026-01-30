import time
import config
from datetime import datetime
from fetch_data import fetch_all_markets
from database import init_db, save_snapshot
from monitor import detect_change, format_alert_message
from alerts import send_telegram_alert

def run_monitoring_cycle():
    """Run 1 cycle - fetch, compare, alert, save"""
    print(f"\n{'='*60}")
