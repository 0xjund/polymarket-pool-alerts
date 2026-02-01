import time
import config
from datetime import datetime
from fetch_data import fetch_all_markets
from database import init_db, save_snapshot
from monitor import detect_changes, format_alert_message
from alerts import send_telegram_alert

def run_monitoring_cycle():
    """Run 1 cycle - fetch, compare, alert, save"""
    print(f"\n{'='*60}")
    print(f"Running monitoring cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    # Fetch market data
    print("\n📡 Fetching market data...")
    markets = fetch_all_markets(limit=config.MARKETS_TO_FETCH)
    print(f"✓ Fetched {len(markets)} markets")

    # Detect changes
    print("\n🔍 Checking for significant changes...")
    alerts = detect_changes(markets, threshold_percent = config.CHANGE_THRESHOLD_PERCENT) 
    print(f"✓ Found {len(alerts)} alerts")

    # Send alerts
    if alerts:
        print("\n📨 Sending alerts...")
        for alert in alerts:
            message = format_alert_message(alert)
            send_telegram_alert(message)
            time.sleep(1) # Rate limit - no spam
            
    else:
        print("\n✓ No significant changes detected")

    # Save snapshot for the next analysis 
    print("\n💾 Saving snapshot to database...")
    rows_saved =save_snapshot(markets)
    print(f"✓ Saved {rows_saved} market snapshots")

    print(f"\n{'='*60}")
    print(f"Cycle complete. Next check in {config.CHECK_INTERVAL_MINUTES} minutes")
    print(f"\n{'='*60}")

def main():
    """ Main entry point - summoning a bot!"""
    print("🤖 Polymarket Alert Bot Starting...")

    # Init DB for the first run
    init_db()

    print("\nConfiguration:")
    print(f" Check interval: {config.CHECK_INTERVALS_MINUTES} minutes")
    print(f" Change threshold: {config.CHANGE_THRESHOLD_PERCENT}%")
    print(f" Markets monitored: {config.MARKETS_TO_FETCH}")
    print("\nPress Ctrl+C to stop\n")

    try:
        while True:
            run_monitoring_cycle()
            # Wait until next check
            time.sleep(config.CHECK_INTERVALS_MINUTES * 60)
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()
            
