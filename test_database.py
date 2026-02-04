import pytest
import time
import os
import database
from database import init_db, save_snapshot, get_previous_snapshot

# Create a test db
TEST_DB = "test_markets.db"

@pytest.fixture
def test_db():
    database.DB_FILE = TEST_DB 
    init_db()

    yield TEST_DB

    # Teardown
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_save_and_retrieve_snapshot(test_db):
    """Test saving a snapshot and retrieving it"""
    markets = [
        {
        'id': 'market_123',
        'title': 'Test market',
        'volume': 50000,
        'liquidity': 10000,
                
        }
    ]
    # Save snapshot
    rows_saved = save_snapshot(markets)
    assert rows_saved == 1

    # Retrieve
    previous = get_previous_snapshot('market_123')
    assert previous is not None
    assert previous['volume'] == 50000
    assert previous['liquidity'] == 10000

def test_get_none_snapshot(test_db):
    """Test that getting a non-existent snapshot returns None"""
    previous = get_previous_snapshot('does_not_exist')
    assert previous is None

def test_multiple_snapshots_returns_latest(test_db):
    """Test that the most recent is used when multiple exist"""
    
    # Save first snapshot
    markets_v1 = [{'id': 'market_123', 'title': 'Test', 'volume': 1000, 'liquidity': 500}]
    save_snapshot(markets_v1)

    time.sleep(0.1)


