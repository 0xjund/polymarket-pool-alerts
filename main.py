import sqlite3
import time
import config
from datetime import datetime
from fetch_data import fetch_all_markets
from database import init_db, save_snapshot
from monitor import detect_changes, format_alert_message
from alerts import send_telegram_alert
from logger import setup_logger

# Logger setup
logger = setup_logger()

def run_monitoring_cycle(skip_alerts=False):
    """Run 1 cycle - fetch, compare, alert, save"""
    logger.info("="*60)
    logger.info(f"Running monitoring cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*60)

    try:

        # Fetch market data
        logger.info("\n Fetching market data...")
        markets = fetch_all_markets(limit=config.MARKETS_TO_FETCH)
        logger.info(f"✓ Fetched {len(markets)} markets")

        # Detect changes
        logger.info("\n🔍 Checking for significant changes...")
        alerts = detect_changes(markets, threshold_percent = config.CHANGE_THRESHOLD_PERCENT) 
        logger.info(f"✓ Found {len(alerts)} alerts")

        # Send alerts
        if alerts and not skip_alerts:
            logger.info("\n📨 Sending alerts...")
            for i, alert in enumerate(alerts, 1):
                message = format_alert_message(alert)
                success = send_telegram_alert(message)
                if success:
                    logger.debug(f"Alert {i}/{len(alerts)} sent: {alert['title'][:50]}...")
                else:
                    logger.warning(f"Failed to send alert {i}/{len(alerts)}")
                time.sleep(1) # Rate limit - no spam
        elif skip_alerts:
            logger.info("\n Skipping alerts (first run - populating database)")
            
        else:
            logger.info("✓ No significant changes detected")

        # Save snapshot for the next analysis 
        logger.info("\n💾 Saving snapshot to database...")
        rows_saved =save_snapshot(markets)
        logger.info(f"✓ Saved {rows_saved} market snapshots")

        logger.info("="*60)
        logger.info(f"Cycle complete. Next check in {config.CHECK_INTERVAL_MINUTES} minutes")
        logger.info("="*60)

    except Exception as e:
        logger.error(f"Error during monitoring cycle: {e}", exc_info=True)
        raise

def main():
    """ Main entry point - summoning a bot!"""
    logger.info("🤖 Polymarket Alert Bot Starting...")

    # Init DB for the first run
    init_db()

    # Check to see if this is the first run - no alerts on the first run
    conn = sqlite3.connect('markets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM market_snapshots")
    snapshot_count = cursor.fetchone()[0]
    conn.close

    is_first_run = (snapshot_count == 0)
    
    if is_first_run:
        logger.info("\n First run - will populate DB without alerts")
    
    logger.info("\nConfiguration:")
    logger.info(f" Check interval: {config.CHECK_INTERVAL_MINUTES} minutes")
    logger.info(f" Change threshold: {config.CHANGE_THRESHOLD_PERCENT}%")
    logger.info(f" Markets monitored: {config.MARKETS_TO_FETCH}")
    logger.info("\nPress Ctrl+C to stop\n")

    try:
        while True:
            run_monitoring_cycle()
            # Wait until next check
            time.sleep(config.CHECK_INTERVAL_MINUTES * 60)
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()
            
