import sqlite3
from datetime import datetime
from typing import List, Dict,Optional

DB_FILE = "markets.db"

def init_db():
    """Initialise the DB with Tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Table for markert snaps
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_snapshots(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        market_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        volume REAL,
        liquidity REAL,
        title TEXT,
        UNIQUE(market_id, timestamp)
    )
""")
    # Index for lookups
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_market_timestamp
    ON market_snapshots(market_id, timestamp DESC)
""")

    conn.commit()
    conn.close()
    print("✓ Database initialized")

def save_snapshot(markets: List[Dict]):
    """Save current market data as a snapshot"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    timestamp = datetime.utcnow().isoformat()

    for market in markets:
        cursor.execute("""
        INSERT OR IGNORE INTO market_snapshots
        (market_id, timestamp, volume, liquidity, title)
        VALUES (?, ?, ?, ?, ?)
    """,( 
        market['id'],
        timestamp,
        market.get('volume', 0),
        market.get('liquidity', 0),
        market.get('title', 'Unknown'),
    ))
            
    conn.commit()
    rows_added = cursor.rowcount
    conn.close()

    return rows_added

def get_previous_snapshot(market_id: str) -> Optional[Dict]:
    """ Get the most recent snapshot for a market"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT volume, liquidity, timestamp
    FROM market_snapshots
    WHERE market_id = ?
    ORDER by timestamp DESC
    LIMIT 1
    """, (market_id,))
     
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            'volume': result[0],
            'liquidity': result[1],
            'timestamp': result[2]
        }
    return None

if __name__ == "__main__":
    init_db()
    print("Database ready")
